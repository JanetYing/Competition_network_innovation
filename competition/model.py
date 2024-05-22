import math
import mesa
import networkx as nx
import numpy as np
from scipy.stats import norm
from competition.agent import FirmAgent
from competition.common import State, calculate_market_median_tar, calculate_equal_intervals, calculate_tar_skewness, get_interval, number_deciding_to_innovate

def generate_tar_values(distribution, num_firms):
    if distribution == "left_skewed":
        tar_values = np.random.beta(a=2, b=5, size=num_firms) * 100
    elif distribution == "right_skewed":
        tar_values = np.random.beta(a=5, b=2, size=num_firms) * 100
    else:  # normal
        tar_values = np.clip(norm.rvs(loc=50, scale=15, size=num_firms), 0, 100)
    return tar_values

class InnovationModel(mesa.Model):
    def __init__(self, num_firms=10, avg_node_degree=3, initial_leader_fraction=0.5,
                 baseline_success_prob=0.05, innovation_gap=20, network_effect=0.5, distribution="normal",
                 tar_gain=5, success_prob_adjustment=0.005):
        super().__init__()
        self.num_firms = num_firms
        self.baseline_success_prob = baseline_success_prob
        self.innovation_gap = innovation_gap
        self.network_effect = network_effect
        self.distribution = distribution
        self.tar_gain = tar_gain
        self.success_prob_adjustment = success_prob_adjustment
        self.step_count = 0
        prob = avg_node_degree / self.num_firms
        self.G = nx.erdos_renyi_graph(n=self.num_firms, p=prob)
        self.grid = mesa.space.NetworkGrid(self.G)
        self.schedule = mesa.time.RandomActivation(self)

        tar_values = generate_tar_values(self.distribution, self.num_firms)
        for i, (node, tar) in enumerate(zip(self.G.nodes(), tar_values)):
            state = State.LEADER if tar > 50 else State.FOLLOWER
            a = FirmAgent(i, self, state, tar)
            self.schedule.add(a)
            self.grid.place_agent(a, node)

        self.datacollector = mesa.DataCollector(
            {
                "Innovating": number_deciding_to_innovate,
                "TAR Skewness": calculate_tar_skewness,
                "0-25th Interval": lambda m: calculate_equal_intervals(m)[0],
                "25-50th Interval": lambda m: calculate_equal_intervals(m)[1],
                "50-75th Interval": lambda m: calculate_equal_intervals(m)[2],
                "75-100th Interval": lambda m: calculate_equal_intervals(m)[3],
            },
            agent_reporters={"TAR": "tar", "Interval": "interval"}
        )
        self.running = True
        self.datacollector.collect(self)

    def get_thresholds(self):
        active_agents = [agent for agent in self.schedule.agents if agent.active]
        tar_values = [agent.tar for agent in active_agents]
        if not tar_values:
            return [0] * 3
        min_tar, max_tar = min(tar_values), max(tar_values)
        bin_size = (max_tar - min_tar) / 4  # Divide the range into 4 equal sections
        thresholds = [min_tar + bin_size * i for i in range(1, 4)]
        return thresholds

    def step(self):
        self.step_count += 1
        thresholds = self.get_thresholds()
        for agent in self.schedule.agents:
            agent.state = State.LEADER if agent.tar > 50 else State.FOLLOWER
            agent.interval = get_interval(agent.tar, thresholds)

        active_agents = [agent for agent in self.schedule.agents if agent.active]
        if len(active_agents) <= self.num_firms / 5:
            self.running = False
            return

        self.schedule.step()
        self.datacollector.collect(self)
