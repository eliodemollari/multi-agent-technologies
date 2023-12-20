from abc import ABC, abstractmethod

from simulation.base.grid import Grid
from simulation.base.intentions import Intention
from utils import logging_utils
# setup logger
logger = logging_utils.setup_logger('EnvironmentLogger', 'environment.log')


class ItemFactory(ABC):
    """Strategy to add items to the grid"""

    @abstractmethod
    def add_items(self, state: Grid, tick: int) -> Grid:
        pass


def _get_intentions(agent_ids: list[int], state: Grid) -> list[Intention]:
    return [state.agents[agent_id].make_intention(state) for agent_id in agent_ids]


class Environment(ABC):
    def __init__(self, item_factory: ItemFactory, state: Grid):
        self._item_factory = item_factory
        self.state = state
        self.tick = 0

    @abstractmethod
    def _illegal_intentions(self, intentions: list[Intention], state: Grid) -> None:
        pass

    @abstractmethod
    def _contradicting_intentions(self, intentions: list[Intention], state: Grid) -> list[Intention]:
        pass

    @abstractmethod
    def _enact_valid_intentions(self, consistent_intentions: list[Intention], state: Grid) -> Grid:
        pass

    def _process_intentions(self, state: Grid) -> Grid:
        """Iteratively process all intentions in the state, until all agents had their Intention enacted. An important
        assumption is that the number of inconsistent operations ALWAYS eventually falls to 0, as in the conflict
        situation, the Environment will always prefer one of them and realise its wish."""
        # Always start with all agents
        agents_not_yet_processed = state.agents.keys()

        # TODO: Check why this optimisation is so effective
        for _ in range(len(state.agents)):
            new_intentions = _get_intentions(agents_not_yet_processed, state)
            try:
                self._illegal_intentions(new_intentions, state)
            except Exception as e:
                logger.error(f"Illegal intention detected: {e}")
                raise
            inconsistent_intentions = self._contradicting_intentions(new_intentions, state)
            consistent_intentions = [intention for intention in new_intentions if intention
                                     not in inconsistent_intentions]
            state = self._enact_valid_intentions(consistent_intentions, state)
            agents_not_yet_processed = [intention.made_by for intention in inconsistent_intentions]

            if len(inconsistent_intentions) == 0:
                break

        return state

    def simulation_step(self) -> Grid:
        # Items are always added in the first step, since we want to have the grid ready at tick 0
        self.state = self._item_factory.add_items(self.state, self.tick)
        self.state = self._process_intentions(self.state)
        self.tick += 1

        logger.info(f"Simulation step completed at tick {self.tick}")

        return self.state
