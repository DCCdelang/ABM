import math

import numpy as np
from mesa import Agent


class Citizen(Agent):
    """
    A member of the general population, may or may not be in active rebellion.
    Summary of rule: If grievance - risk > threshold, rebel.

    Attributes:
        unique_id: unique int
        x, y: Grid coordinates
        hardship: Agent's 'perceived hardship (i.e., physical or economic
            privation).' Exogenous, drawn from U(0,1).
        regime_legitimacy: Agent's perception of regime legitimacy, equal
            across agents.  Exogenous.
        risk_aversion: Exogenous, drawn from U(0,1).
        threshold: if (grievance - (risk_aversion * arrest_probability)) >
            threshold, go/remain Active
        vision: number of cells in each direction (N, S, E and W) that agent
            can inspect
        condition: Can be "Quiescent" or "Active;" deterministic function of
            greivance, perceived risk, and
        grievance: deterministic function of hardship and regime_legitimacy;
            how aggrieved is agent at the regime?
        arrest_probability: agent's assessment of arrest probability, given
            rebellion

    """

    def __init__(
        self,
        unique_id,
        model,
        pos,
        hardship,
        regime_legitimacy,
        risk_aversion,
        threshold,
        vision,
        legitimacy_feedback,
    ):
        """
        Create a new Citizen.
        Args:
            unique_id: unique int
            x, y: Grid coordinates
            hardship: Agent's 'perceived hardship (i.e., physical or economic
                privation).' Exogenous, drawn from U(0,1).
            regime_legitimacy: Agent's perception of regime legitimacy, equal
                across agents.  Exogenous.
            risk_aversion: Exogenous, drawn from U(0,1).
            threshold: if (grievance - (risk_aversion * arrest_probability)) >
                threshold, go/remain Active
            vision: number of cells in each direction (N, S, E and W) that
                agent can inspect. Exogenous.
            model: model instance
        """
        super().__init__(unique_id, model)
        self.breed = "citizen"
        self.pos = pos
        self.hardship = hardship
        self.regime_legitimacy = regime_legitimacy
        self.feedback_legitimacy = regime_legitimacy
        self.risk_aversion = risk_aversion
        self.threshold = threshold
        self.condition = "Quiescent"
        self.vision = vision
        self.jail_sentence = 0
        self.grievance = self.hardship * (1 - self.feedback_legitimacy)
        self.arrest_probability = None
        self.fighting_time_cit = 0

    def step(self):
        """
        Decide whether to activate, then move if applicable.
        """
        if self.fighting_time_cit:
            self.fighting_time_cit -= 1
            if not self.fighting_time_cit:
                self.condition = "Jailed"
            return

        if self.jail_sentence:
            self.jail_sentence -= 1
            # After a jailed agent comes out of jail, her state is set to quiet instead of her previous state before arrest (active).
            if not self.jail_sentence:
                self.condition = "Quiescent"
            return  # No other changes or movements if agent is in jail.

        self.update_neighbors()
        self.update_estimated_arrest_probability()

        if self.model.legitimacy_kind == "Fixed":
            self.regime_legitimacy

        elif self.model.legitimacy_kind == "Global":
            self.feedback_legitimacy = self.model.legitimacy_feedback 

        elif self.model.legitimacy_kind == "Local":
            self.feedback_legitimacy = self.update_legitimacy_feedback() 

        net_risk = self.risk_aversion * self.arrest_probability
        if (
            self.condition == "Quiescent"
            and (self.grievance - net_risk) > self.threshold
        ):
            self.condition = "Active"
        elif (
            self.condition == "Active" and (self.grievance - net_risk) <= self.threshold
        ):
            self.condition = "Quiescent"
        if self.model.movement and self.empty_neighbors:
            new_pos = self.random.choice(self.empty_neighbors)
            self.model.grid.move_agent(self, new_pos)

    def update_neighbors(self):
        """
        Look around and see who my neighbors are
        """
        self.neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=False, radius=self.vision
        )
        self.neighbors = self.model.grid.get_cell_list_contents(self.neighborhood)
        self.empty_neighbors = [
            c for c in self.neighborhood if self.model.grid.is_cell_empty(c)
        ]

    def update_estimated_arrest_probability(self):
        """
        Based on the ratio of cops to actives in my neighborhood, estimate the
        p(Arrest | I go active).

        """
        cops_in_vision = len([c for c in self.neighbors if c.breed == "cop"])
        actives_in_vision = 1.0  # Citizen counts herself
        for c in self.neighbors:
            if (
                c.breed == "citizen"
                and c.condition == "Active"
                and c.jail_sentence == 0
            ):
                actives_in_vision += 1
            if (
                c.breed == "citizen"
                and c.condition == "Fighting"
            ):
                actives_in_vision += 1
                
        # Rounding the actives to cops ratio to min integer (1)
        self.ratio_c_a = int(cops_in_vision/ actives_in_vision)
        
        self.arrest_probability = 1 - math.exp(
            -1 * self.model.arrest_prob_constant * (self.ratio_c_a )
        )

    def update_legitimacy_feedback(self):
        """
        Attempt to simulate a legitimacy feedback loop as discussed in a paper
        by Lomos et al 2014. Returns weighted avarage as based on Gilley.
        """
        self.N_quiet = 0
        self.N_active = 0
        self.N_jailed = 0
        self.N_agents = 0
        self.N_fighting = 0
        for c in self.neighbors:
            if c.breed == "citizen":
                self.N_agents += 1
                if c.condition == "Quiescent":
                    self.N_quiet += 1
                elif c.condition == "Active":
                    self.N_active += 1
                elif c.condition == "Fighting":
                    self.N_fighting += 1
                elif c.condition == "Jailed":
                    self.N_jailed += 1
        
        L_leg = self.N_quiet/self.N_agents
        L_just = 1/2*(1-((self.N_active + self.N_fighting)/self.N_agents)) + 1/2*(1-math.exp(-math.log(2)/2*(self.N_agents/(self.N_active + self.N_jailed + self.N_fighting + 1))))
        L_consent = L_leg

        return self.regime_legitimacy * (1/4*(L_leg+L_consent)+1/2*L_just)

class Cop(Agent):
    """
    A cop for life.  No defection.
    Summary of rule: Inspect local vision and arrest a random active agent.

    Attributes:
        unique_id: unique int
        x, y: Grid coordinates
        vision: number of cells in each direction (N, S, E and W) that cop is
            able to inspect
    """

    def __init__(self, unique_id, model, pos, vision):
        """
        Create a new Cop.
        Args:
            unique_id: unique int
            x, y: Grid coordinates
            vision: number of cells in each direction (N, S, E and W) that
                agent can inspect. Exogenous.
            model: model instance
        """
        super().__init__(unique_id, model)
        self.breed = "cop"
        self.pos = pos
        self.vision = vision
        self.fighting_time_cop = 0
 

    def step(self):
        """
        Inspect local vision and arrest a random active agent. Move if
        applicable.
        """
        self.update_neighbors()
        active_neighbors = []
        if self.fighting_time_cop:
            self.fighting_time_cop -= 1
            return # Stay put till fight is over.

        for agent in self.neighbors:
            if (
                agent.breed == "citizen"
                and agent.condition == "Active"
                and agent.jail_sentence == 0
            ):
                active_neighbors.append(agent)
                
        if active_neighbors:
            arrestee = self.random.choice(active_neighbors)
            # Moving the cop to the arrested agent position (2)
            if self.model.movement:
                self.model.grid.move_agent(self, arrestee.pos)
            sentence = self.random.randint(0, self.model.max_jail_term)
            arrestee.jail_sentence = sentence

            fighttime = self.model.max_fighting_time
            arrestee.fighting_time_cit = fighttime
            self.fighting_time_cop = fighttime
            arrestee.condition = "Fighting"
            
        elif self.model.movement and self.empty_neighbors:
            if self.model.smart_cops:

                utilities = []
                # itterate over available empty spaces for movement
                for pos in self.empty_neighbors:
                    # gets a list of neighbor objects for every empty position
                    neighbors = self.model.grid.get_neighbors(pos, moore = True, radius = self.vision)
                    # if list not empty, itterate over the agent objects and calculate utility, else assign low utility
                    utility = 0
                    if len(neighbors) > 0:
                        for agent in neighbors:
                            if agent.breed == "citizen" and agent.condition == "Active" and agent.jail_sentence == 0:
                                utility += 10
                            elif agent.breed == "citizen" and agent.condition == "Fighting":
                                utility += 10
                            # elif agent.breed == "citizen" and agent.condition == "Quiescent":
                            #     utility -= 2
                            # elif agent.breed == "cop":
                            #     utility += 5    
                        utilities.append(utility)
                    else:
                        utilities.append(-100)

                # choose position with highest utility and move the cop there
                max_utility = np.max(utilities)
                max_utility_ind = utilities.index(max_utility)
                new_pos = self.empty_neighbors[max_utility_ind]
            else:
                new_pos = self.random.choice(self.empty_neighbors)
                self.model.grid.move_agent(self, new_pos)

    def update_neighbors(self):
        """
        Look around and see who my neighbors are.
        """
        self.neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=False, radius=self.vision
        )
        self.neighbors = self.model.grid.get_cell_list_contents(self.neighborhood)
        self.empty_neighbors = [
            c for c in self.neighborhood if self.model.grid.is_cell_empty(c)
        ]
