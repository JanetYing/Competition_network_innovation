import mesa
from mesa.visualization.modules import NetworkModule, ChartModule, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider, Choice
from competition.model import InnovationModel, State, calculate_equal_intervals

def network_portrayal(G):
    """
    Define the portrayal of the network.

    """
    def node_color(agent):
        """
        Define the color of the node based on the agent's state and interval.

        Returns:
            str: The color of the node in RGB format.
        """
        if not agent.active:
            return "#D3D3D3"  # Light gray for inactive firms
        interval = agent.interval if agent.interval is not None else 0
        color_intensity = max(64, 255 - (interval * 64))  # Ensure color intensity is within the valid range and not too light
        return f"rgb(0, 0, {color_intensity})"  # Shades of blue

    portrayal = {"nodes": [], "edges": []}
    for node, agents in G.nodes.data("agent"):
        portrayal["nodes"].append({
            "id": node,
            "color": node_color(agents[0]),
            "size": 6,
            "tooltip": f"id: {agents[0].unique_id}<br>state: {agents[0].state.name}<br>tar: {agents[0].tar:.2f}<br>active: {agents[0].active}"
        })

    for source, target in G.edges:
        portrayal["edges"].append({
            "source": source,
            "target": target,
            "color": "#808080",
            "width": 2
        })

    return portrayal

class IntervalText(TextElement):
    """
    Custom text element to display the number of active firms in each interval.
    """
    def render(self, model):
        """
        Render the text element.

        """
        counts = calculate_equal_intervals(model)
        active_firms = sum(counts)
        return (f"Active Firms: {active_firms}<br>"
                f"0-25th Interval: {counts[0]}<br>"
                f"25-50th Interval: {counts[1]}<br>"
                f"50-75th Interval: {counts[2]}<br>"
                f"75-100th Interval: {counts[3]}")

# Define the network and other visualization modules
network = NetworkModule(network_portrayal, 500, 500)
chart = ChartModule([
    {"Label": "Innovating", "Color": "#000000"},
])

skewness_chart = ChartModule([
    {"Label": "TAR Skewness", "Color": "#000000"},
])

class LegendText(TextElement):
    """
    Custom text element for displaying the legend.
    """
    def render(self, model):
        """
        Render the legend text.

        Args:
            model (InnovationModel): The innovation model.

        Returns:
            str: The legend text explaining the node colors.
        """
        return ("<b>Legend:</b><br>"
                "Light Gray: Inactive firms<br>"
                "Shades of Blue: Active firms, darker indicates higher TAR interval<br>"
                "0-25th Interval: Light Blue<br>"
                "25-50th Interval: Medium Blue<br>"
                "50-75th Interval: Darker Blue<br>"
                "75-100th Interval: Dark Blue")

# Create the legend text element
legend_text = LegendText()

# Model parameters
model_params = {
    "num_firms": Slider("Number of firms", 50, 10, 100, 1),
    "avg_node_degree": Slider("Avg Node Degree", 3, 3, 8, 1),
    "baseline_success_prob": Slider("Baseline Success Probability", 0.5, 0.0, 1.0, 0.01),
    "innovation_gap": Slider("Innovation Gap", 30, 1, 60, 1),
    "network_effect": Slider("Network Effect", 0.03, 0.0, 0.05, 0.005),
    "distribution": Choice("Initial TAR Distribution", value="normal", choices=["normal", "left_skewed", "right_skewed"]),
    "tar_gain": Slider("TAR Increment", 5, 1, 10, 1),
    "success_prob_adjustment": Slider("Success Probability Adjustment", 0.08, 0.02, 0.15, 0.001),
}

# Initialize the interval text element
interval_text = IntervalText()

# Create the server
server = ModularServer(InnovationModel, [network, chart, skewness_chart, interval_text, legend_text], "Innovation Model", model_params)
server.port = 8521
