
import math
import mesa
import networkx as nx
from enum import Enum

class State(Enum):
    LEADER = 0
    FOLLOWER = 1

def number_state(model, state):
    return sum(1 for a in model.schedule.agents if a.state is state)

class InnovationModel(mesa.Model):
    def __init__(self, num_firms=10, avg_node_degree=3, initial_leader_fraction=0.5, 
                 baseline_success_prob=0.05, innovation_gap=20, network_effect=0.5):
        super().__init__()
        self.num_firms = num_firms
        self.baseline_success_prob = baseline_success_prob
        self.innovation_gap = innovation_gap
        self.network_effect = network_effect
        prob = avg_node_degree / self.num_firms
        self.G = nx.erdos_renyi_graph(n=self.num_firms, p=prob)
        self.grid = mesa.space.NetworkGrid(self.G)
        self.schedule = mesa.time.RandomActivation(self)
        
        for i, node in enumerate(self.G.nodes()):
            tar = self.random.uniform(0, 100)
            state = State.LEADER if tar > 50 else State.FOLLOWER
            a = FirmAgent(i, self, state, tar)
            self.schedule.add(a)
            self.grid.place_agent(a, node)
        
        self.datacollector = mesa.DataCollector(
            {
                "Leaders": lambda m: number_state(m, State.LEADER),
                "Followers": lambda m: number_state(m, State.FOLLOWER)
            }
        )
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

class FirmAgent(mesa.Agent):
    def __init__(self, unique_id, model, initial_state, tar):
        super().__init__(unique_id, model)
        self.state = initial_state
        self.tar = tar
        self.success_prob = model.baseline_success_prob

    def step(self):
        self.make_innovation_decision()

    def make_innovation_decision(self):
        if self.state == State.FOLLOWER:
            if self.model.random.random() < self.success_prob:
                self.tar += 1
            self.success_prob *= (1 - 0.005)  # Reduce success probability by 0.5% if failed