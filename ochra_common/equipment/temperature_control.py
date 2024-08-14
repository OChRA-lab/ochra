from abc import ABC, abstractmethod


class TemperatureControls(ABC):
    """
    Abstract class for temperature control devices.

    This class defines the methods that a temperature control device should implement.
    """

    @abstractmethod
    def set_temperature(self, temperature: int) -> bool:
        """
        Set the temperature of the device.

        Args:
            temperature (int): The desired temperature to set.

        Returns:
            bool: True if the temperature was set successfully
        """
        pass

    @abstractmethod
    def start_heat(self) -> bool:
        """
        Start the heating process.

        Returns:
            bool: True if the heating process started successfully
        """
        pass

    @abstractmethod
    def stop_heat(self) -> bool:
        """
        Stop the heating process.

        Returns:
            bool: True if the heating process stopped successfully
        """
        pass
