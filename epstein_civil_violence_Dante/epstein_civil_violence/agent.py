import math

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
        polit_pref,
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
        self.risk_aversion = risk_aversion
        self.threshold = threshold
        self.condition = "Quiescent"
        self.vision = vision
        self.jail_sentence = 0
        self.grievance = self.hardship * (1 - self.regime_legitimacy)
        self.arrest_probability = None
        self.polit_pref = polit_pref # ADDED parameter
        self.fighting_time = 0

    def step(self):
        """
        Decide whether to activate, then move if applicable.
        """
        if self.fighting_time:
            self.fighting_time -= 1
            return # no other changes or movements if agent is in jail.
        if self.jail_sentence:
            self.jail_sentence -= 1
            return  # no other changes or movements if agent is in jail.
        self.update_neighbors()
        self.update_estimated_arrest_probability()

        self.regime_legitimacy = self.model.legitimacy_feedback # Change of legitimacy calculation

        # if self.model.iteration > 0:
        #     self.update_legitimacy_feedback() # Addition of legitimacy feedback
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
            self.pos, moore=False, radius=1
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
        actives_in_vision = 1.0  # citizen counts herself
        for c in self.neighbors:
            if (
                c.breed == "citizen"
                and c.condition == "Active"
                and c.jail_sentence == 0
            ):
                actives_in_vision += 1
        self.arrest_probability = 1 - math.exp(
            -1 * self.model.arrest_prob_constant * (cops_in_vision / (actives_in_vision+1)) # Changed with added A+1 instead of A
        )
    
    # def update_legitimacy_feedback(self):
    #     """
    #     Attempt to simulate a legitimacy feedback loop as discussed in a paper
    #     by Lomos et al 2014. Returns weighted avarage as based on Gilley.
    #     """
    #     N_quiet = self.model.count_type_citizens(self.model, "Quiescent")
    #     N_active = self.model.count_type_citizens(self.model, "Active")
    #     N_jailed = self.model.count_type_citizens(self.model, "Jailed")

    #     L_leg = N_quiet/self.model.N_agents
    #     # Zero needs to be replaced by N_fighting --> Still has to be implemented in model/agent
    #     L_just = 1/2*(1-N_active + 0) + 1/2*(1-math.exp(-math.log(2)/2*(self.model.N_agents/(N_active + N_jailed + 0 + 1))))
    #     L_consent = L_leg

    #     self.legitimacy_feedback = self.regime_legitimacy * (1/4*(L_leg+L_consent)+1/2*L_just)
    #     self.grievance = self.hardship * (1 - self.legitimacy_feedback)

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
        self.fighting = 0

    def step(self):
        """
        Inspect local vision and arrest a random active agent. Move if
        applicable.
        """
        if self.fighting > 0:
            self.fighting -= 1
            return

        self.update_neighbors()
        active_neighbors = []
        for agent in self.neighbors:
            if (
                agent.breed == "citizen"
                and agent.condition == "Active"
                and agent.jail_sentence == 0
            ):
                active_neighbors.append(agent)
        if active_neighbors:
            arrestee = self.random.choice(active_neighbors)
            if arrestee.condition == "Active" and arrestee.fighting_time == 0:
                arrestee.fighting_time = self.random.randint(0,self.model.max_fighting_time)
                arrestee.condition = "Fighting"
                self.fighting = arrestee.fighting_time
                return

            elif arrestee.condition == "Fighting" and arrestee.fighting_time == 0:
                sentence = self.random.randint(0, self.model.max_jail_term)
                arrestee.jail_sentence = sentence
                arrestee.condition == "Jailed"

        if self.model.movement and self.empty_neighbors:
            new_pos = self.random.choice(self.empty_neighbors)
            self.model.grid.move_agent(self, new_pos)

    def update_neighbors(self):
        """
        Look around and see who my neighbors are.
        """
        self.neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=False, radius=1
        )
        self.neighbors = self.model.grid.get_cell_list_contents(self.neighborhood)
        self.empty_neighbors = [
            c for c in self.neighborhood if self.model.grid.is_cell_empty(c)
        ]
