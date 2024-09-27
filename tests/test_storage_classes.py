from ochra_common.storage.stock import Stock
from ochra_common.storage.inventory import Inventory
from ochra_common.storage.device_inventory import DeviceInventory
from ochra_common.storage.consumable import Consumable
from ochra_common.storage.container import Container
from ochra_common.storage.holder import Holder
from ochra_common.storage.vessel import Vessel
from ochra_common.storage.reagent import Reagent

import uuid


def test_stock():
    # test construction of the stock
    station_id = uuid.uuid4()
    stock = Stock(station_id=station_id)

    # test stock attributes
    assert stock.station_id == station_id
    assert stock.inventories == []

    # test stock methods
    assert stock.to_json() == '{"id":"' + str(stock.id) + \
        '","cls":"ochra_common.storage.stock.Stock","station_id":"' + \
        str(station_id) + '","inventories":[]}'

    assert stock.to_dict() == {"id": stock.id,
                               "cls": "ochra_common.storage.stock.Stock",
                               "station_id": station_id,
                               "inventories": []}


def test_inventory():
    # test construction of the inventory
    inventory = Inventory(containers_max_capacity=100)

    # test inventory attributes
    assert inventory.containers == []
    assert inventory.consumables == []
    assert inventory.containers_max_capacity == 100

    # test inventory methods
    assert inventory.to_json() == '{"id":"' + str(inventory.id) + \
        '","cls":"ochra_common.storage.inventory.Inventory","containers_max_capacity":100' + \
        ',"containers":[],"consumables":[]}'

    assert inventory.to_dict() == {"id": inventory.id,
                                   "cls": "ochra_common.storage.inventory.Inventory",
                                   "containers": [],
                                   "consumables": [],
                                   "containers_max_capacity": 100}


def test_device_inventory():
    # test construction of the device inventory
    device_id = uuid.uuid4()
    inventory = DeviceInventory(
        containers_max_capacity=100, device_id=device_id)

    # test device inventory attributes
    assert inventory.containers == []
    assert inventory.consumables == []
    assert inventory.containers_max_capacity == 100
    assert inventory.device_id == device_id

    # test device inventory methods
    assert inventory.to_json() == '{"id":"' + str(inventory.id) + \
        '","cls":"ochra_common.storage.device_inventory.DeviceInventory","containers_max_capacity":100' + \
        ',"containers":[],"consumables":[],"device_id":"' + \
        str(device_id) + '"}'

    assert inventory.to_dict() == {"id": inventory.id,
                                   "cls": "ochra_common.storage.device_inventory.DeviceInventory",
                                   "containers": [],
                                   "consumables": [],
                                   "containers_max_capacity": 100,
                                   "device_id": device_id}


def test_consumables():
    # test construction of the consumable
    consumable = Consumable(type="cap", quantity=10)

    # test consumable attributes
    assert consumable.type == "cap"
    assert consumable.quantity == 10

    # test consumable methods
    assert consumable.to_json() == '{"id":"' + str(consumable.id) + \
        '","cls":"ochra_common.storage.consumable.Consumable","type":"cap","quantity":10}'

    assert consumable.to_dict() == {"id": consumable.id,
                                    "cls": "ochra_common.storage.consumable.Consumable",
                                    "type": "cap",
                                    "quantity": 10}


def test_container():
    # test construction of the container
    container = Container(type="box", max_capacity=100, physical_id=1)

    # test container attributes
    assert container.type == "box"
    assert container.max_capacity == 100
    assert container.physical_id == 1
    assert container.is_used == False

    # test container methods
    assert container.to_json() == '{"id":"' + str(container.id) + \
        '","cls":"ochra_common.storage.container.Container","type":"box"' + \
        ',"max_capacity":100,"physical_id":1,"is_used":false}'

    assert container.to_dict() == {"id": container.id,
                                   "cls": "ochra_common.storage.container.Container",
                                   "type": "box",
                                   "physical_id": 1,
                                   "max_capacity": 100,
                                   "is_used": False}


def test_holder():
    # test construction of the holder
    holder = Holder(type="rack", max_capacity=16, physical_id=1)

    # test holder attributes
    assert holder.type == "rack"
    assert holder.max_capacity == 16
    assert holder.physical_id == 1
    assert holder.is_used == False

    # test holder methods
    assert holder.to_json() == '{"id":"' + str(holder.id) + \
        '","cls":"ochra_common.storage.holder.Holder","type":"rack"' + \
        ',"max_capacity":16,"physical_id":1,"is_used":false,"containers":[]}'

    assert holder.to_dict() == {"id": holder.id,
                                "cls": "ochra_common.storage.holder.Holder",
                                "type": "rack",
                                "physical_id": 1,
                                "max_capacity": 16,
                                "is_used": False,
                                "containers": []}


def test_vessel():
    # test construction of the vessel
    vessel = Vessel(type="vial", max_capacity=5.0,
                    capacity_unit="ml", physical_id=1)

    # test vessel attributes
    assert vessel.type == "vial"
    assert vessel.max_capacity == 5.0
    assert vessel.physical_id == 1
    assert vessel.is_used == False

    # test vessel methods
    assert vessel.to_json() == '{"id":"' + str(vessel.id) + \
        '","cls":"ochra_common.storage.vessel.Vessel","type":"vial"' + \
        ',"max_capacity":5.0,"physical_id":1,"is_used":false,"capacity_unit":"ml"' + \
        ',"reagents":[]}'

    assert vessel.to_dict() == {"id": vessel.id,
                                "cls": "ochra_common.storage.vessel.Vessel",
                                "type": "vial",
                                "physical_id": 1,
                                "max_capacity": 5.0,
                                "is_used": False,
                                "capacity_unit": "ml",
                                "reagents": []}


def test_reagent():
    # test construction of the reagent
    reagent = Reagent(name="water", amount=100.0, unit="ml")

    # test reagent attributes
    assert reagent.name == "water"
    assert reagent.amount == 100.0
    assert reagent.unit == "ml"
    assert reagent.physical_state == -1
    assert reagent.properties == {}

    # test reagent methods
    assert reagent.to_json() == '{"id":"' + str(reagent.id) + \
        '","cls":"ochra_common.storage.reagent.Reagent","name":"water","amount":100.0' + \
        ',"unit":"ml","physical_state":-1,"properties":{}}'

    assert reagent.to_dict() == {"id": reagent.id,
                                 "cls": "ochra_common.storage.reagent.Reagent",
                                 "name": "water",
                                 "amount": 100.0,
                                 "unit": "ml",
                                 "physical_state": -1,
                                 "properties": {}}
