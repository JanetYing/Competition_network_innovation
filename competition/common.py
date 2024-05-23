import numpy as np
from enum import Enum
from scipy.stats import skew

class State(Enum):
    """Enum for representing the state of a firm agent."""
    LEADER = 0
    FOLLOWER = 1


def number_deciding_to_innovate(model):
    """
    Calculate the number of active agents deciding to innovate.

    """
    return sum(1 for a in model.schedule.agents if a.decides_to_innovate and a.active)


def calculate_market_median_tar(model):
    """
    TAR: Tech Advancement
    Calculate the median TAR of active agents in the market.

    """
    active_agents = [agent for agent in model.schedule.agents if agent.active]
    tar_values = [agent.tar for agent in active_agents]
    return np.median(tar_values) if tar_values else 0


def calculate_market_max_tar(model):
    """
    Calculate the maximum TAR of active agents in the market.

    """
    active_agents = [agent for agent in model.schedule.agents if agent.active]
    return max(agent.tar for agent in active_agents) if active_agents else 0


def calculate_equal_intervals(model):
    """
    Calculate the number of active agents in each of four equal TAR intervals.

    """
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
    """
    Calculate the skewness of TAR values of active agents.

    """
    active_agents = [agent for agent in model.schedule.agents if agent.active]
    tar_values = [agent.tar for agent in active_agents]
    return skew(tar_values) if tar_values else 0


def get_interval(tar, thresholds):
    """
    Determine the interval index for a given TAR based on the provided thresholds.

    """
    return np.digitize(tar, thresholds)
