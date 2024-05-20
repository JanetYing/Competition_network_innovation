import mesa
from mesa.visualization.modules import NetworkModule, ChartModule, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from competition.model import InnovationModel, State, calculate_equal_intervals  # Import the function

def network_portrayal(G):
    def node_color(agent):
        return {State.LEADER: "#FF0000", State.FOLLOWER: "#008000"}.get(agent.state, "#808080")

    portrayal = {"nodes": [], "edges": []}
    for node, agents in G.nodes.data("agent"):
        portrayal["nodes"].append({
            "id": node,
            "color": node_color(agents[0]),
            "size": 6,
            "tooltip": f"id: {agents[0].unique_id}<br>state: {agents[0].state.name}<br>tar: {agents[0].tar:.2f}"
        })

    for source, target in G.edges:
        portrayal["edges"].append({
            "source": source,
            "target": target,
            "color": "#e8e8e8",
            "width": 2
        })

    return portrayal

class IntervalText(TextElement):
    def render(self, model):
        counts = calculate_equal_intervals(model)
        return f"0-20th Interval: {counts[0]}<br>20-40th Interval: {counts[1]}<br>40-60th Interval: {counts[2]}<br>60-80th Interval: {counts[3]}<br>80-100th Interval: {counts[4]}"

network = NetworkModule(network_portrayal, 500, 500)
chart = ChartModule([
    {"Label": "Innovating", "Color": "#0000FF"},
])

interval_chart = ChartModule([
    {"Label": "0-20th Interval", "Color": "#FFD700"},
    {"Label": "20-40th Interval", "Color": "#87CEEB"},
    {"Label": "40-60th Interval", "Color": "#32CD32"},
    {"Label": "60-80th Interval", "Color": "#FF69B4"},
    {"Label": "80-100th Interval", "Color": "#8A2BE2"},
])

skewness_chart = ChartModule([
    {"Label": "TAR Skewness", "Color": "#FFA500"},
])

model_params = {
    "num_firms": mesa.visualization.Slider("Number of firms", 10, 10, 100, 1),
    "avg_node_degree": mesa.visualization.Slider("Avg Node Degree", 3, 3, 8, 1),
    "baseline_success_prob": mesa.visualization.Slider("Baseline Success Probability", 0.05, 0.0, 1.0, 0.01),
    "innovation_gap": mesa.visualization.Slider("Innovation Gap", 20, 1, 100, 1),
    "network_effect": mesa.visualization.Slider("Network Effect", 0.5, 0.0, 1.0, 0.1),
}

interval_text = IntervalText()

server = ModularServer(InnovationModel, [network, chart, skewness_chart, interval_chart, interval_text], "Innovation Model", model_params)
server.port = 8521
