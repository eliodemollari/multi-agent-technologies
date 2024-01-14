## Multi-agent Technologies

The repository is structured as follows:
- The `master` branch contains the implementation of the initial Basic technique.
- The `brokering` branch builds upon the main branch and implements the Brokering technique.
- The `recommendation` branch, also built upon the main branch, implements the Recommendation technique.


## Techniques
### Basic Technique
The Basic technique is a straightforward task allocation system where agents compete for tasks based on their availability and proximity to the task. The principle is First Come, First Serve. An agent moves towards the nearest pickup station and attempts to pick up an item. This technique serves as the foundational model for our study and is implemented in the main branch.

### Brokering Technique
The Brokering technique represents a comprehensive brokering approach where a broker, having a full view of the grid, actively manages the task-sharing process by assigning tasks to agents. At every step, the broker checks for agents that are not currently carrying an item or moving towards a pickup station. When such agents are found, the broker assigns a specific item to the closest agent. This technique is implemented in the brokering branch.

### Recommendation Technique
The Recommendation technique is a nuanced brokering approach where the broker recommends providers to the initiator, who then selects a provider to complete the task. In this case, the Pickup Station acts as the initiator, while the agents are the providers. When a new item is added, the pickup station contacts the broker, who then selects the top three nearest agents and recommends them to the pickup station. The pickup station then randomly selects one agent from the list and assigns the item to it. This technique is implemented in the recommendation branch.

## Getting Started
To evaluate a specific technique, switch to the relevant branch by using the command `git checkout <branch-name>`. Replace `<branch-name>` with either `master`, `brokering`, or `recommendation` based on the technique you want to evaluate.

After switching to the desired branch, run the simulation using the command python `main.py`. Make sure you have all the necessary dependencies installed.

## Running Experiments
Our codebase supports running different experiments by varying the initial setup for the environment. This is achieved by passing different JSON files as parameters to the `main.py` script.

The `main.py` script expects two parameters: `rounds` and a JSON file path. `rounds` represents the number of rounds the simulation will run, and the JSON file provides the initial setup for the environment.

We've provided several JSON files that represent different experimental setups by varying certain parameters. You can find these files in the `experiments` folder. Here are the available files:
- `10_pickup_stations.json`
- `15_pickup_stations_experiment.json`
- `16_obstacles_experiment.json`
- `20_agent_experiment.json`
- `30_agents_experiment.json`
- `experiment_1.json`

You can choose to run the first experiment, which uses the main setup `experiment_1.json`, or different variations by specifying one of the other JSON files.

### How to Run an Experiment
1. Navigate to the root directory of this repository on your local machine.
2. Run the `main.py` script with the desired number of rounds and the path to the chosen JSON file. For example, to run the main setup (`experiment_1.json`) for `400` rounds, you would use the following command:
   
```
python main.py rounds=400 experiments/experiment_1.json
```

Replace `experiment_1.json` with the name of the desired JSON file to run different variations.

By running different experiments, you can explore how changes in the initial setup affect the efficiency and effectiveness of the task-sharing strategies in the simulation.
