import math
import mesa
import networkx as nx
from enum import Enum
from scipy.stats import skew

class State(Enum):
    LEADER = 0
    FOLLOWER = 1

def number_state(model, state):
    return sum(1 for a in model.schedule.agents if a.state is state)

def number_deciding_to_innovate(model):
    return sum(1 for a in model.schedule.agents if a.decides_to_innovate)

def calculate_market_average_tar(model):
    total_tar = sum(agent.tar for agent in model.schedule.agents)
    return total_tar / len(model.schedule.agents)

def calculate_equal_intervals(model):
    tar_values = [agent.tar for agent in model.schedule.agents]
    min_tar, max_tar = min(tar_values), max(tar_values)
    bin_size = (max_tar - min_tar) / 5  # Divide the range into 5 equal sections
    thresholds = [min_tar + bin_size * i for i in range(1, 5)]
    counts = [0] * 5
    
    for agent in model.schedule.agents:
        if agent.tar <= thresholds[0]:
            counts[0] += 1
        elif agent.tar <= thresholds[1]:
            counts[1] += 1
        elif agent.tar <= thresholds[2]:
            counts[2] += 1
        elif agent.tar <= thresholds[3]:
            counts[3] += 1
        else:
            counts[4] += 1

    return counts

def calculate_tar_skewness(model):
    tar_values = [agent.tar for agent in model.schedule.agents]
    return skew(tar_values)

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
                "Innovating": number_deciding_to_innovate,
                "TAR Skewness": calculate_tar_skewness,
                "0-20th Interval": lambda m: calculate_equal_intervals(m)[0],
                "20-40th Interval": lambda m: calculate_equal_intervals(m)[1],
                "40-60th Interval": lambda m: calculate_equal_intervals(m)[2],
                "60-80th Interval": lambda m: calculate_equal_intervals(m)[3],
                "80-100th Interval": lambda m: calculate_equal_intervals(m)[4],
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
        self.decides_to_innovate = False

    def step(self):
        self.make_innovation_decision()

    def make_innovation_decision(self):
        market_avg_tar = calculate_market_average_tar(self.model)
        if abs(self.tar - market_avg_tar) < self.model.innovation_gap:
            self.decides_to_innovate = True
            if self.model.random.random() < self.success_prob:
                self.tar += 5
                self.success_prob *= (1 + 0.005)
            else:
                self.success_prob *= (1 - 0.005)
        else:
            self.decides_to_innovate = False
