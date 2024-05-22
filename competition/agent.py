import mesa
from competition.common import calculate_market_median_tar, State

class FirmAgent(mesa.Agent):
    def __init__(self, unique_id, model, initial_state, tar):
        super().__init__(unique_id, model)
        self.state = initial_state
        self.tar = tar
        self.success_prob = model.baseline_success_prob
        self.decides_to_innovate = False
        self.no_innovation_steps = 0
        self.active = True
        self.interval = None

    def step(self):
        self.make_innovation_decision()

    def make_innovation_decision(self):
        market_median_tar = calculate_market_median_tar(self.model)
        print(f"Step {self.model.step_count}, Firm {self.unique_id} TAR: {self.tar}, Median TAR: {market_median_tar}, Innovation Gap: {self.model.innovation_gap}")
        if abs(self.tar - market_median_tar) < self.model.innovation_gap:
            self.decides_to_innovate = True


            network_influence = sum((neighbor.tar - self.tar) / market_median_tar
                                    for neighbor in self.model.grid.get_neighbors(self.pos, include_center=False)
                                    if neighbor.tar > self.tar)

            self.success_prob = self.model.baseline_success_prob * (1 + self.model.network_effect * network_influence)


            if self.model.random.random() < self.success_prob:
                self.tar += self.model.tar_gain
                self.success_prob *= (1 + self.model.success_prob_adjustment)
                self.no_innovation_steps = 0
       
            else:
                self.success_prob *= (1 - self.model.success_prob_adjustment)

        else:
            self.decides_to_innovate = False
            self.no_innovation_steps += 1


        if self.no_innovation_steps >= 5:
            self.active = False

