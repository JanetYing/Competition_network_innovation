# Competition, Networks, and Innovation

**Author**: Janet Cao  

## Description
This project aims to simulate and analyze technological advancement/innovation within a competitive network of firms. Using an Agent-Based Model (ABM), the simulation explores the dynamics of network effects, innovation gaps, and other factors influencing firms' technological advancements.

## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Configuration](#configuration)


## Installation
To set up the project, follow these steps:

### Prerequisites
- Python 3.8 or higher
- Recommended: Virtual environment for package management

### Installation Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/Competition_network_innovation.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Competition_network_innovation
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. **Read the Paper**: Start by reading the `Final Paper.pdf` to gain a comprehensive understanding of the project's goals, methodologies, and findings.

2. **Run the ABM Model**: 
    - Use the `run.py` script to launch the Agent-Based Model (ABM) in a web-based interface.
    - This will allow you to see how each simulation proceeds and understand the role of different parameters.
    ```bash
    python run.py
    ```

3. **Batch Run Analysis**:
    - Use the `batch_run.ipynb` notebook to conduct batch runs of the simulation.
    - This notebook demonstrates how to collect and analyze data from single typical runs and batch runs.
    - The outputs, including plots and regression analyses, are stored in the `output pic` folder.

## Features
- Simulate technological advancement within a network of competitive firms.
- Analyze the impact of network effects, innovation gaps, and other factors.
- Visualize simulation outcomes through interactive web interfaces.
- Perform batch runs for extensive data collection and analysis.

## Configuration
Main Configuration options are defined within the simulation scripts and notebooks. Key parameters include:
- `avg_node_degree`: Average number of connections each firm has.
- `network_effect`: Intensity of the network effect.
- `innovation_gap`: Tolerance for the innovation gap.
- `tar_gain`: Increment in TAR after a successful innovation.
- `success_prob_adjustment`: Adjustment to success probability based on previous outcomes.
