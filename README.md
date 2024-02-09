# Third Assignment: Multi-agent Technologies
The third assignment of the Multi-agent Technologies, was implemented on top of the second assignment, more specifically
the Brokering technique. The main goal of this assignment was to implement a combinatorial auction protocol between the 
agents and the broker (auctioneer). The combinatorial auction protocol is a type of auction in which bidders can place
bids on combinations of items, or "packages," rather than just individual items. The protocol was implemented in the
`master` branch. 

## Combinatorial Auction Protocol
The protocol is a two-phase protocol, where the first phase is the bidding phase and the second phase is the allocation
of the winning bids to the agents. The broker is responsible for the management of the auction, and the agents are 
responsible for placing bids on the items.

Initially the broker checks in the system for items available for auction, and then it sends a message to all agents
informing them of the items available for auction. The agents then place bids on the items, and the broker collects the 
bids. After the bidding phase is over, the broker then allocates the items to the agents based on the bids placed.

### Bid Determination 
Each participant in the auction submits bids for every potential combination of items. These bids correspond to the minimum 
costs associated with acquiring the specified set of items. For instance, in the case of agent 2, items A and B are 
considered complementary, while items B and D are deemed substitutes due to the disproportionate costs associated with 
acquiring them together (subadditivity principle). It's important to note that in this context, costs are represented as 
negative utilities, where higher values indicate worse outcomes.

### XOR Bids
Participants make XOR bids, meaning that each participant can win at most one bundle. Additionally, there's an option for 
participants to bid zero for an empty bundle, signifying no cost.

### Auctioneer's Role
The auctioneer is responsible for determining the solution that maximizes welfare and allocates one bundle (potentially 
an empty one) to each participant. In the provided example, the optimal solution is ({A,B},{C,D}) with a welfare value 
of C*=8. It's worth noting that the auctioneer acts as a dictator in this scenario, meaning that participants must accept 
the allocation. This setup allows for the implementation of various social choice mechanisms simply by adjusting the optimization criteria.

### Practical Considerations
It's essential to acknowledge the practical challenges associated with solving this and similar problems. The computational 
complexity and communication overhead can be substantial. Specifically, as the number of tasks increases, so does the 
computational burden. Even computing a single bid, which involves planning optimal routes, can be highly complex for 
participants. While this might be more manageable in other problem domains, the auctioneer faces the most significant 
computational challenges, including filtering out dominated bids (a linear-time operation) and subsequently identifying 
the best allocation (an exponential-time task due to the power set of possible assignments). These factors contribute to 
the impracticality of certain approaches for addressing such problems.

## Agents and Bids
Each agent is responsible for placing bids on the items. The bids are placed based on the distance of the agent to the 
pickup station and the capacity of the agent. Each bid is associated with a cost, which is the cost the system is being 
charged for the delivery of the item (or bundle of items).
If an agent has capacity to carry more than one item, it can place bids on multiple items. 
The cost mechanism is based on the distance of the agent to the pickup station and agent's capacity. It costs more units 
if the agent has smaller capacity, as it is considered a quicker and more expensive delivery. 

## Selfish Agents & Non-selfish Agents
Agents can have different strategies when placing bids. Some agents can be selfish, meaning if new items are added to the 
system, they will place bids on the new items, even if they are already carrying an item. Other agents can be non-selfish,
meaning they will not place bids on new items if they are already carrying an item. 


# Second Assignment: Multi-agent Technologies
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

## Viewing Experiment Results
The results of the experiments can be viewed both in the console and in the log files generated by the simulation.

## Console Output
While running the experiments, a significant amount of information is printed in the console. This includes:
- The number of ticks (simulation steps)
- The movements of the agents
- Actions of picking up and delivering items
This real-time output provides a useful way to monitor the simulation as it progresses.

## Log Files
For a more persistent record of the simulation data, we employ a logger package to log various actions and events during the simulation. This includes every move, intention, or action of each class, all logged into separate logger classes.

At the end of each simulation run, several log files are automatically generated in the main part of the repository. These files include:
- `agent.log`
- `item.log`
- `environment.log`
  
Each of these files contains valuable information about the actions taken during the simulation. For example, `agent.log` records the actions of the agents, `item.log` records details about the items being delivered, and `environment.log` keeps track of the overall state of the simulation environment.

These log files provide a comprehensive record of the entire simulation process, making them a valuable resource for in-depth analysis and evaluation of the task-sharing strategies. By examining these logs, you can gain insights into the behavior of the agents, the efficiency of item delivery, and the dynamics of the simulation environment under different initial setups.
