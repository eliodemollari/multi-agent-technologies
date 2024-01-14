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
