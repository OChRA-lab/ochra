from abc import ABC, abstractmethod


class StirControls(ABC):
    """
    Abstract class for stir control devices.

    This class defines the methods that a stir control device should implement.
    """

    @abstractmethod
    def set_speed(self, speed: int) -> bool:
        """
        Set the stirring speed of the device.

        Args:
            speed (int): The desired stirring speed to set.

        Returns:
            bool: True if the speed was set successfully, False otherwise.
        """
        pass

    @abstractmethod
    def start_stir(self) -> bool:
        """
        Start the stirring process.

        Returns:
            bool: True if the stirring process started successfully, False otherwise.
        """
        pass

    @abstractmethod
    def stop_stir(self) -> bool:
        """
        Stop the stirring process.

        Returns:
            bool: True if the stirring process stopped successfully, False otherwise.
        """
        pass
