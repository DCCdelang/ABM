from mesa import Model
from mesa.time import RandomActivation
from mesa.space import Grid
from mesa.datacollection import DataCollector

from .agent import Cop, Citizen

import math

class EpsteinCivilViolence(Model):
    """
    Model 1 from "Modeling civil violence: An agent-based computational
    approach," by Joshua Epstein.
    http://www.pnas.org/content/99/suppl_3/7243.full
    Attributes:
        height: grid height
        width: grid width
        citizen_density: approximate % of cells occupied by citizens.
        cop_density: approximate % of calles occupied by cops.
        citizen_vision: number of cells in each direction (N, S, E and W) that
            citizen can inspect
        cop_vision: number of cells in each direction (N, S, E and W) that cop
            can inspect
        legitimacy:  (L) citizens' perception of regime legitimacy, equal
            across all citizens
        max_jail_term: (J_max)
        active_threshold: if (grievance - (risk_aversion * arrest_probability))
            > threshold, citizen rebels
        arrest_prob_constant: set to ensure agents make plausible arrest
            probability estimates
        movement: binary, whether agents try to move at step end
        max_iters: model may not have a natural stopping point, so we set amodel.arrest_prob_constant
            max.

    """

    def __init__(
        self,
        height=40,
        width=40,
        citizen_density=0.7,
        cop_density=0.04,
        citizen_vision=7,
        cop_vision=7,
        legitimacy=0.82,
        max_jail_term=30,
        active_threshold=0.1,
        arrest_prob_constant=2.3,
        movement=True,
        max_iters=500,
        max_fighting_time=1, 
        smart_cops = False,
        legitimacy_kind = "Global", 
    ):
        super().__init__()
        self.height = height
        self.width = width
        self.citizen_density = citizen_density
        self.cop_density = cop_density
        self.citizen_vision = citizen_vision
        self.cop_vision = cop_vision
        self.legitimacy = legitimacy
        self.max_jail_term = max_jail_term
        self.active_threshold = active_threshold
        self.arrest_prob_constant = arrest_prob_constant
        self.movement = movement
        self.max_iters = max_iters
        self.iteration = 0
        self.schedule = RandomActivation(self)
        self.grid = Grid(height, width, torus=True)
        self.legitimacy_kind = legitimacy_kind
        self.legitimacy_feedback = legitimacy
        self.N_agents = 0
        self.max_fighting_time = max_fighting_time
        self.smart_cops = smart_cops
        model_reporters = {
            "Quiescent": lambda m: self.count_type_citizens(m, "Quiescent"),
            "Active": lambda m: self.count_type_citizens(m, "Active"),
            "Jailed": lambda m: self.count_jailed(m),
            "Fighting": lambda m: self.count_fighting(m),
            "Legitimacy": lambda m: self.legitimacy_feedback,
        }
        agent_reporters = {
            "x": lambda a: a.pos[0],
            "y": lambda a: a.pos[1],
            "breed": lambda a: a.breed,
            "jail_sentence": lambda a: getattr(a, "jail_sentence", None),
            "condition": lambda a: getattr(a, "condition", None),
            "arrest_probability": lambda a: getattr(a, "arrest_probability", None),
            "Legitimacy": lambda a: getattr(a, "feedback_legitimacy", None),   
        }
        self.datacollector = DataCollector(
            model_reporters=model_reporters, agent_reporters=agent_reporters
        )
        unique_id = 0
        if self.cop_density + self.citizen_density > 1:
            raise ValueError("Cop density + citizen density must be less than 1")

        for (_, x, y) in self.grid.coord_iter():
            if self.random.random() < self.cop_density:
                cop = Cop(unique_id, self, (x, y), vision=self.cop_vision)
                unique_id += 1
                self.grid[y][x] = cop
                self.schedule.add(cop)
            elif self.random.random() < (self.cop_density + self.citizen_density):
                citizen = Citizen(
                    unique_id,
                    self,
                    (x, y),
                    hardship=self.random.random(),
                    regime_legitimacy=self.legitimacy,
                    risk_aversion=self.random.random(),
                    threshold=self.active_threshold,
                    vision=self.citizen_vision,
                    legitimacy_feedback=self.legitimacy_feedback, 
                )
                unique_id += 1
                self.grid[y][x] = citizen
                self.schedule.add(citizen)
                self.N_agents += 1

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step and collect data.
        """
        if self.legitimacy_kind == "Global":
            self.legitimacy_feedback = self.update_legitimacy_feedback(self)
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        self.iteration += 1
        if self.iteration > self.max_iters:
            self.running = False
        
        if self.iteration %10 == 0:
            print("step", self.iteration)

    @staticmethod
    def update_legitimacy_feedback(model):
        """
        Attempt to simulate a legitimacy feedback loop as discussed in a paper
        by Lomos et al 2014. Returns weighted avarage as based on Gilley.
        """
        N_quiet = model.count_type_citizens(model, "Quiescent")
        N_active = model.count_type_citizens(model, "Active")
        N_jailed = model.count_jailed(model)
        N_fighting = model.count_fighting(model)

        L_leg = N_quiet/model.N_agents
        L_just = 1/2*(1-((N_active+N_fighting)/model.N_agents)) + 1/2*(1-math.exp(-math.log(2)/2*(model.N_agents/(N_active + N_jailed + N_fighting + 1))))
        L_consent = L_leg

    
        return model.legitimacy * (1/4*(L_leg+L_consent)+1/2*L_just)

    @staticmethod
    def count_type_citizens(model, condition, exclude_jailed=True):
        """
        Helper method to count agents by Quiescent/Active.
        """
        count = 0
        for agent in model.schedule.agents:
            if agent.breed == "cop":
                continue
            if exclude_jailed and agent.jail_sentence:
                continue
            if agent.condition == condition:
                count += 1
        return count

    @staticmethod
    def count_jailed(model):
        """
        Helper method to count jailed agents.
        """
        count = 0
        for agent in model.schedule.agents:
            if agent.breed == "citizen" and agent.jail_sentence and not agent.fighting_time_cit:
                count += 1
        return count

    @staticmethod
    def count_fighting(model):
        """
        Helper method to count fighting agents.
        """
        count = 0
        for agent in model.schedule.agents:
            if agent.breed == "citizen" and agent.fighting_time_cit:
                count += 1
        return count
