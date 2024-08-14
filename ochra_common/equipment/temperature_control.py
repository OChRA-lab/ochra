from abc import ABC, abstractmethod


class TemperatureControls(ABC):
    """The methods that a temperature control device should implement"""
    @abstractmethod
    def set_temperature(self, temperature: int) -> bool:
        pass

    @abstractmethod
    def start_heat(self) -> bool:
        pass

    @abstractmethod
    def stop_heat(self) -> bool:
        pass
