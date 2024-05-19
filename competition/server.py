import mesa
from mesa.visualization.modules import NetworkModule, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from competition.model import InnovationModel, State

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

network = NetworkModule(network_portrayal, 500, 500)
chart = ChartModule([
    # {"Label": "Leaders", "Color": "#FF0000"},
    # {"Label": "Followers", "Color": "#008000"},
    {"Label": "Innovating", "Color": "#0000FF"},
    # {"Label": "Top 1/3", "Color": "#FFD700"},
    # {"Label": "Middle 1/3", "Color": "#87CEEB"},
    # {"Label": "Bottom 1/3", "Color": "#D3D3D3"},

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

server = ModularServer(InnovationModel, [network, chart, skewness_chart], "Innovation Model", model_params)
server.port = 8521

