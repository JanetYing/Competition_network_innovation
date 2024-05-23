import mesa
from competition.common import calculate_market_median_tar, State

class FirmAgent(mesa.Agent):
    """
    An agent representing a firm in the innovation model.
    
    Attributes:
        unique_id (int): The unique identifier for the agent.
        model (mesa.Model): The model instance in which the agent exists.
        state (State): The state of the agent, either LEADER or FOLLOWER.
        tar (float): The current TAR (Technology Achievement) value of the firm.
        success_prob (float): The probability of successful innovation.
        decides_to_innovate (bool): Indicates if the firm decides to innovate in the current step.
        no_innovation_steps (int): Tracks the number of consecutive steps without innovation.
        active (bool): Indicates if the firm is active or inactive.
        interval (int): The interval category of the firm's TAR value.
    """
    
    def __init__(self, unique_id, model, initial_state, tar):
        """
        Initialize a new FirmAgent.

        Parameters:
            unique_id (int): The unique identifier for the agent.
            model (mesa.Model): The model instance in which the agent exists.
            initial_state (State): The initial state of the agent (LEADER or FOLLOWER).
            tar (float): The initial TAR value of the firm.
        """
        super().__init__(unique_id, model)
        self.state = initial_state
        self.tar = tar
        self.success_prob = model.baseline_success_prob
        self.decides_to_innovate = False
        self.no_innovation_steps = 0
        self.active = True
        self.interval = None

    def step(self):
        """
        Perform one step of the agent's behavior.
        """
        self.make_innovation_decision()

    def make_innovation_decision(self):
        """
        Decide whether to innovate based on the current TAR value market median tar.
        Update the TAR value and success probability accordingly.
        """
        market_median_tar = calculate_market_median_tar(self.model)
        
        if abs(self.tar - market_median_tar) < self.model.innovation_gap:
            self.decides_to_innovate = True

            # Calculate network influence
            network_influence = sum((neighbor.tar - self.tar) / market_median_tar
                                    for neighbor in self.model.grid.get_neighbors(self.pos, include_center=False)
                                    if neighbor.tar > self.tar)

            # Update success probability with network effect
            self.success_prob = self.model.baseline_success_prob * (1 + self.model.network_effect * network_influence)

            # Attempt innovation
            if self.model.random.random() < self.success_prob:
                self.tar += self.model.tar_gain
                self.success_prob *= (1 + self.model.success_prob_adjustment)
                self.no_innovation_steps = 0
            else:
                self.success_prob *= (1 - self.model.success_prob_adjustment)
        else:
            self.decides_to_innovate = False
            self.no_innovation_steps += 1

        # Mark firm as inactive if it hasn't innovated for 5 continuous steps
        if self.no_innovation_steps >= 5:
            self.active = False
