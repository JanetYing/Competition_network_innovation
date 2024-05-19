
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

# def calculate_tar_thresholds(model):
#     tar_values = [agent.tar for agent in model.schedule.agents]
#     tar_values.sort()
#     n = len(tar_values)
#     lower_third_threshold = tar_values[int(n / 3)]
#     upper_third_threshold = tar_values[int(2 * n / 3)]
#     return lower_third_threshold, upper_third_threshold

# def count_tar_segments(model):
#     lower_third_threshold, upper_third_threshold = calculate_tar_thresholds(model)
#     top_1_3 = sum(1 for agent in model.schedule.agents if agent.tar > upper_third_threshold)
#     middle_1_3 = sum(1 for agent in model.schedule.agents if lower_third_threshold < agent.tar <= upper_third_threshold)
#     bottom_1_3 = sum(1 for agent in model.schedule.agents if agent.tar <= lower_third_threshold)
#     return top_1_3, middle_1_3, bottom_1_3

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
                # "Leaders": lambda m: number_state(m, State.LEADER),
                # "Followers": lambda m: number_state(m, State.FOLLOWER),
                "Innovating": number_deciding_to_innovate,
                # "Top 1/3": lambda m: count_tar_segments(m)[0],
                # "Middle 1/3": lambda m: count_tar_segments(m)[1],
                # "Bottom 1/3": lambda m: count_tar_segments(m)[2],
                "TAR Skewness": calculate_tar_skewness,
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
                self.tar += 1
                self.success_prob *= (1 + 0.005)
            else:
                self.success_prob *= (1 - 0.005)  # Reduce success probability by 0.5% if failed
        else:
            self.decides_to_innovate = False