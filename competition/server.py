import mesa
from mesa.visualization.modules import NetworkModule, ChartModule, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider, Choice
from competition.model import InnovationModel, State, calculate_equal_intervals

def network_portrayal(G):
    def node_color(agent):
        if not agent.active:
            return "#D3D3D3"  # Light gray for inactive firms
        interval = agent.interval if agent.interval is not None else 0
        color_intensity = max(64, 255 - (interval * 64))  # Ensure color intensity is within the valid range and not too light
        # Create shades of blue that don't turn white
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
    def render(self, model):
        counts = calculate_equal_intervals(model)
        return f"0-25th Interval: {counts[0]}<br>25-50th Interval: {counts[1]}<br>50-75th Interval: {counts[2]}<br>75-100th Interval: {counts[3]}"

network = NetworkModule(network_portrayal, 500, 500)
chart = ChartModule([
    {"Label": "Innovating", "Color": "#000000"},
])

interval_chart = ChartModule([
    {"Label": "0-25th Interval", "Color": "#000000"},
    {"Label": "25-50th Interval", "Color": "#666666"},
    {"Label": "50-75th Interval", "Color": "#999999"},
    {"Label": "75-100th Interval", "Color": "#CCCCCC"},
])

skewness_chart = ChartModule([
    {"Label": "TAR Skewness", "Color": "#000000"},
])

model_params = {
    "num_firms": Slider("Number of firms", 50, 10, 100, 1),
    "avg_node_degree": Slider("Avg Node Degree", 3, 3, 8, 1),
    "baseline_success_prob": Slider("Baseline Success Probability", 0.5, 0.0, 1.0, 0.01),
    "innovation_gap": Slider("Innovation Gap", 30, 1, 60, 1),
    "network_effect": Slider("Network Effect", 0.03, 0.0, 0.05, 0.005),
    "distribution": Choice("Initial TAR Distribution", value="normal", choices=["normal", "left_skewed", "right_skewed"]),
    "tar_gain": Slider("TAR Increment", 5, 1, 10, 1),
    "success_prob_adjustment": Slider("Success Probability Change", 0.08, 0.02, 0.15, 0.001),
}

interval_text = IntervalText()

server = ModularServer(InnovationModel, [network, chart, skewness_chart, interval_chart, interval_text], "Innovation Model", model_params)
server.port = 8521
