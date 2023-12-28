from abc import ABC, abstractmethod
from src.simulation.base.grid import Grid, Agent
from src.simulation.base.intentions import Intention
from src.utils import logging_utils

# setup logger
logger = logging_utils.setup_logger('EnvironmentLogger', 'environment.log')


def _get_intentions(state: Grid) -> list[Intention]:
    list_of_intentions = []
    for agent in state.agents:
        list_of_intentions.append(agent.make_intention(state))
    return list_of_intentions


class Environment(ABC):
    def __init__(self, state: Grid):
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

        new_intentions = _get_intentions(state)

        try:
            self._illegal_intentions(new_intentions, state)
        except Exception as e:
            logger.error(f"Illegal intention detected: {e}")
            raise

        inconsistent_intentions = self._contradicting_intentions(new_intentions, state)
        consistent_intentions = [intention for intention in new_intentions if intention
                                 not in inconsistent_intentions]
        state = self._enact_valid_intentions(consistent_intentions, state)

        return state

    def simulation_step(self) -> Grid:
        self.state = self._process_intentions(self.state)
        self.tick += 1

        logger.info(f"Simulation step completed at tick {self.tick}")

        return self.state
