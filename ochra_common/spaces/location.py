from ..base import DataModel


class Location(DataModel):
    """
    Abstract location to correspond to a physical location.

    Attributes:
        name (str): The name of the location.
        map (str): The map associated with the location.
        map_id (int): The identifier for the location on the map.
    """
    name: str
    map: str
    map_id: int

    def __eq__(self, value: "Location") -> bool:
        return value.name == self.name and value.map == self.map and value.map_id == self.map_id
