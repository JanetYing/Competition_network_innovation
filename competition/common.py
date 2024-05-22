import numpy as np
from enum import Enum
from scipy.stats import skew

class State(Enum):
    LEADER = 0
    FOLLOWER = 1

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
        interval = np.digitize(agent.tar, thresholds)
        counts[interval] += 1

    return counts

def calculate_tar_skewness(model):
    active_agents = [agent for agent in model.schedule.agents if agent.active]
    tar_values = [agent.tar for agent in active_agents]
    return skew(tar_values) if tar_values else 0

def get_interval(tar, thresholds):
    return np.digitize(tar, thresholds)
