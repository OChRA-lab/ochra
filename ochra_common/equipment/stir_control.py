from abc import ABC, abstractmethod


class StirControls(ABC):
    @abstractmethod
    def set_speed(self, speed: int) -> bool:
        pass

    @abstractmethod
    def start_stir(self) -> bool:
        pass

    @abstractmethod
    def stop_stir(self) -> bool:
        pass
