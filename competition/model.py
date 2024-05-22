import math
import mesa
import networkx as nx
from enum import Enum
from scipy.stats import skew, norm
import numpy as np

class State(Enum):
    LEADER = 0
    FOLLOWER = 1

def number_state(model, state):
    return sum(1 for a in model.schedule.agents if a.state is state and a.active)

def number_deciding_to_innovate(model):
    return sum(1 for a in model.schedule.agents if a.decides_to_innovate and a.active)

def calculate_market_median_tar(model):
    active_agents = [agent for agent in model.schedule.agents if agent.active]
    tar_values = [agent.tar for agent in active_agents]
    return np.median(tar_values) if tar_values else 0

def calculate_market_max_tar(model):
    active_agents = [agent for agent in model.schedule.agents if agent.active]
    return max(agent.tar for agent in active_agents) if active_agents else 0

def calculate_equal_intervals(model):
    active_agents = [agent for agent in model.schedule.agents if agent.active]
    tar_values = [agent.tar for agent in active_agents]
    if not tar_values:
        return [0] * 4
    min_tar, max_tar = min(tar_values), max(tar_values)
    bin_size = (max_tar - min_tar) / 4  # Divide the range into 4 equal sections
    thresholds = [min_tar + bin_size * i for i in range(1, 4)]
    counts = [0] * 4
    
    for agent in active_agents:
        if agent.tar <= thresholds[0]:
            counts[0] += 1
        elif agent.tar <= thresholds[1]:
            counts[1] += 1
        elif agent.tar <= thresholds[2]:
            counts[2] += 1
        else:
            counts[3] += 1

    return counts

def calculate_tar_skewness(model):
    active_agents = [agent for agent in model.schedule.agents if agent.active]
    tar_values = [agent.tar for agent in active_agents]
    return skew(tar_values) if tar_values else 0

def get_interval(tar, thresholds):
    if tar <= thresholds[0]:
        return 0
    elif tar <= thresholds[1]:
        return 1
    elif tar <= thresholds[2]:
        return 2
    else:
        return 3

def generate_tar_values(distribution, num_firms):
    if distribution == "left_skewed":
        tar_values = np.random.beta(a=2, b=5, size=num_firms) * 100
    elif distribution == "right_skewed":
        tar_values = np.random.beta(a=5, b=2, size=num_firms) * 100
    else:  # normal
        tar_values = norm.rvs(loc=50, scale=15, size=num_firms)
        tar_values = np.clip(tar_values, 0, 100)  # Ensure values are between 0 and 100
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
        self.step_count = 0  # Initialize step counter
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
        self.step_count += 1  # Increment step counter
        print(f"Step {self.step_count}")
        
        # Update agent states based on current TAR values
        thresholds = self.get_thresholds()
        for agent in self.schedule.agents:
            agent.state = State.LEADER if agent.tar > 50 else State.FOLLOWER
            agent.interval = get_interval(agent.tar, thresholds)
        
        # Stop condition if active firms are less than or equal to 1/5 of total firms
        active_agents = [agent for agent in self.schedule.agents if agent.active]
        if len(active_agents) <= self.num_firms / 5:
            self.running = False
            return
        
        self.schedule.step()
        self.datacollector.collect(self)

class FirmAgent(mesa.Agent):
    def __init__(self, unique_id, model, initial_state, tar):
        super().__init__(unique_id, model)
        self.state = initial_state
        self.tar = tar
        self.success_prob = model.baseline_success_prob
        self.decides_to_innovate = False
        self.no_innovation_steps = 0  # Track consecutive non-innovation steps
        self.active = True  # Track if the firm is active or inactive
        self.interval = None  # Initialize interval attribute

    def step(self):
        self.make_innovation_decision()

    def make_innovation_decision(self):
        market_median_tar = calculate_market_median_tar(self.model)
        print(f"Step {self.model.step_count}, Firm {self.unique_id} TAR: {self.tar}, Median TAR: {market_median_tar}, Innovation Gap: {self.model.innovation_gap}")
        if abs(self.tar - market_median_tar) < self.model.innovation_gap:
            self.decides_to_innovate = True
            print(f"Step {self.model.step_count}, Firm {self.unique_id} decides to innovate")
            
            # Calculate network influence
            network_influence = 0
            for neighbor in self.model.grid.get_neighbors(self.pos, include_center=False):
                if neighbor.tar > self.tar:
                    network_influence += (neighbor.tar - self.tar) / market_median_tar  # divide market median tar to scale the influence
            
            # Update success probability with network effect
            self.success_prob = self.model.baseline_success_prob * (1 + self.model.network_effect * network_influence)
            print(f"Step {self.model.step_count}, Firm {self.unique_id} Network Influence: {network_influence}, Success Probability: {self.success_prob}")
            
            if self.model.random.random() < self.success_prob:
                self.tar += self.model.tar_gain
                self.success_prob *= (1 + self.model.success_prob_adjustment)
                self.no_innovation_steps = 0  # Reset counter if innovating
                print(f"Step {self.model.step_count}, Firm {self.unique_id} successfully innovates, new TAR: {self.tar}")
            else: 
                self.success_prob *= (1 - self.model.success_prob_adjustment)
                print(f"Step {self.model.step_count}, Firm {self.unique_id} fails to innovate, new Success Probability: {self.success_prob}")
        else:
            self.decides_to_innovate = False
            self.no_innovation_steps += 1  # Increment counter if not innovating
            print(f"Step {self.model.step_count}, Firm {self.unique_id} decides not to innovate")

        # Mark firm as inactive if it hasn't innovated for 5 continuous steps
        if self.no_innovation_steps >= 5:
            self.active = False
            print(f"Step {self.model.step_count}, Firm {self.unique_id} becomes inactive")
