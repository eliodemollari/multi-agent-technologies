# Multi-agent Technologies
Agent architectures, frameworks, autonomous systems engineering &amp; testing tools.

### Experiments
#### Initial Distribution
In the experiment_1.json and experiment_2.json files, the strategy used for item distribution is InitialDistribution. This strategy uses a predefined distribution of items between pickup and delivery stations. The distribution field in the JSON file specifies which delivery stations each pickup station is associated with. For example, "pickup_station_1": ["delivery_station_1", "delivery_station_2"] means that items from pickup_station_1 are destined for delivery_station_1 and delivery_station_2.

#### Weighted Distribution
On the other hand, in the experiment_3.json file, the strategy used is WeightedDistribution. This strategy uses a probabilistic approach to distribute items. The pickup_distribution field specifies the probability of each pickup station generating an item, and the delivery_weights field specifies the weight of each delivery station as a destination for the items. For example, "pickup_station_1": 0.3 means that pickup_station_1 has a 30% chance of generating an item, and "delivery_station_1": 3 means that delivery_station_1 has a weight of 3 when deciding where an item should be delivered. The steps_per_tick field specifies the number of simulation steps that occur per tick.