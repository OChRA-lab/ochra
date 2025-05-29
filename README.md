# OCHRA COMMON

For the things that're used in both [Discovery](https://github.com/OChRA-lab/ochra_discovery) and [manager](https://github.com/OChRA-lab/ochra_manager)

### base.py

- This contains DataModel class which is the base model for all other dataclasses in the databases
- The DataModel is a subclass of Pydantics BaseModel and contains the following default attributes
    - *id* this is the id of an object
    - *collection* this is the collection that the object belongs to in the database
    - *cls* this is the name of the class which will be stored in the database
    - *module_path* finally should we want to transport an instance of a class over the wire we need to know where to import the class from for creating it dynamically

- get_base_model
    - to be called by children to return just the base information needed to reinstance a class


## UTILS

### enum.py

Collection of ENUM types for various situations that will be used across the system. 

### miscs.py

Misc. useful functions to check various things

### mixins.py

This file contains two main classes RestProxyMixin and RestProxyMixinReadOnly

#### RestProxyMixin

Class that contains methods for use by other classes without having to be the parent class of those other classes. A mixin is a lot like a composition in functional programming but it is not to be instantiated it has functions that can be used by many other classes

`RestProxyMixin` enables a class to act as a **proxy for a remote API**, dynamically linking attributes to API calls via `LabConnection`. It automatically registers objects on the endpoint and replaces attribute access with **getters and setters** that fetch and update remote properties. The `from_id` method reconstructs an instance from the API using its stored data.

- **`_mixin_hook(endpoint, object_id)`**  
  - Establishes a lab connection and registers the object remotely.  
  - Overrides attribute access with **getter and setter methods** that interact with the API.  

- **`from_id(object_id)`** *(Class Method)*  
  - Reconstructs an instance by fetching stored attributes from the API.  
  - Ensures the instance is correctly linked to its remote counterpart.  

`RestProxyMixinReadOnly` is very similar to the former but it only allows read only permission to the object. It does not allow write permissions

### singleton_meta.py

This implementation defines a **thread-safe singleton metaclass** (`SingletonMeta`), ensuring that only one instance of a class exists across multiple threads. It maintains a dictionary of instances and uses a **thread lock** to prevent race conditions when creating a new instance. When a class with this metaclass is instantiated, the `__call__` method checks if an instance already exists; if not, it creates and stores one. Subsequent instantiations return the existing instance, making it ideal for scenarios like logging, configuration management, or database connections where a single shared instance is needed.

This is mostly used to allow a shared LabConnection while only having to define the IP of the lab we connect to each time we instance it.


## STORAGE

Module that contains a variety of classes for different types of storage objects that exist in reality. The current docstrings contain enough information for these simple classes. I have added these below for the sake of brevity. The Storage classes are all inheritents of DataModel

The majority of these classes are implemented in [discovery](https://github.com/OChRA-lab/ochra_discovery) for usage by a user

### consumable.py
**Abstract class** for lab consumables (caps, needles, etc.).

**Attributes**  
- `name` (str): The name of the consumable item.  
- `quantity` (int): The current quantity available.

**Methods**  
- **change_quantity(amount: int):** Adjusts the consumable quantity by the specified amount.

**Usage**  
- Track disposable items in the lab’s inventory.  
- Update the quantity as items are used up.

*Example subclass:*  
```python
class Syringe(Consumable):
    def __init__(self, name, quantity):
        super().__init__(name=name, quantity=quantity)
```

### container.py:
**Abstract class** for containers, anything that can hold something
**Attributes**
- `type` (str): The type of the container.
- `max_capacity` (int|float): The maximum capacity of the container.
- `physical_id` (int): The physical identifier of the container. Defaults to None.
- `is_used` (bool): Indicates whether the container has been used. Defaults to False.

**Methods**
- *get_used_capacity*: Get the used capacity of the container at present
- *get_avalable_capacity*: Gets the available capacity of the container at present

**Usage**
- To represent physical objects like racks.

*Example subclass*
Look to vessel or holder

### holder.py
**Abstract class** that represents any container that can hold another container
**Attributes**
- containers: (List[Type[Container]]): list of containers inside the holder

**Methods**
- *add_container*: Method for adding containers to the Holder
- *remove_containers*: Method for removing containers from a holder

**Usage**
- Organise how your containers are stored

*Example Subclass*
```python
class Rack(Holder):
    def __init__(self):
        super().__init__()
```

### inventory.py
**Abstract class** for inventory, contains containers and consumables.

**Attributes**
- `owner` (DataModel): The owner of the inventory.
- `containers_max_capacity` (int): The maximum capacity of containers in the inventory.
- `containers` (List[Container]): A list of containers in the inventory. Defaults to an empty list.
- `consumables` (List[Consumable]): A list of consumables in the inventory. Defaults to an empty list.

**Methods**
- *add_container* : Add a container to the inventory
- *remove_container* : Remove a container from the inventory
- *add_consumable* : Add a consumable to the inventory
- *remove_consumable* : Remove the consumable from the inventory


### reagent.py
**Abstract** Reagent class to represent any chemicals used
- `name` (str): The name of the reagent.
- `amount` (float): The amount of the reagent.
- `unit` (str): The unit of measurement for the amount.
- `physical_state` (Enum): The physical state of the reagent (e.g., solid, liquid, gas). Defaults to UNKNOWN.
- `properties` (Dict[str, Any]): A dictionary of additional properties of the reagent.

**Methods**
- *add_property*:  Add a property to the reagent
- *remove_property*: Remove a property of the reagent
- *change_amount*: Change the amount of the reagent

**Usage**
- Represent our chemicals used in workflows

*Example Subclass*
```python
class Alcohol(Reagent):
    def __init__(self, amount=100.0):
        super().__init__(properties={}, amount=amount)
```

### vessel.py
Vessel **Abstract class**, any container that can hold reagents

**Attributes**
- `capacity_unit` (str): The unit of measurement for the vessel's capacity.
- `reagents` (List[Reagent]): A list of reagents contained in the vessel. Defaults to an empty list.

**Methods**
- *add_reagent*(reagent: Reagent): Place a reagent in the vessel.
- *remove_reagent*(reagent_id: UUID): Remove a reagent by ID.

**Usage**
- store combinations of reagents so you know whats in what vial etc

*Example Subclass*
```python
class Flask(Vessel):
    def __init__(self):
        super().__init__()
```

## SPACES

This module are for classes that represent physical spaces in the real setting. Similar to storage there is not much business logic that has actually been implemented and so I have just provided a small excerpt below for explaining what these classes are meant to be.

### lab.py
**Abstract class** representing a laboratory.

**Attributes**  
- `stations` (List[Station]): A list of Station objects within the lab.  
- `robots` (List[Robot]): A list of Robot objects supervised by the lab.  

**Methods**  
- **get_stations():** Retrieve all Station objects in the lab.  
- **get_station(station_id: str):** Retrieve a specific station by its identifier.  
- **get_robots():** Retrieve all Robot objects in the lab.  
- **get_robot(robot_id: str):** Retrieve a specific robot by its identifier.

**Usage**  
- Acts as a high-level controller that manages stations and orchestrates operations.  
- Provides an entry point for discovering and accessing lab resources.

*Example subclass:*  
```python
class MyLab(Lab):
    def custom_method(self):
        pass
```

### location.py: 
**Abstract class** location to correspond to a physical location.

**Attributes**
- `lab` (str): The name of the lab this location belongs to
- `room` (str): The room name
- `place` (str): Description of where in the room it is

**Methods**
None

**Usage**
- Used to describe to someone how to get to the physical location of some device/lab/station

*Example Subclass*:
```python
class CustomLocation(Location):
    def detailed_description(self) -> str:
        return f"Lab: {self.lab}, Room: {self.room}, Place: {self.place}"
```

### station.py: 
**Abstract Class** station that contains information all stations will have.

**Attributes**
- name: str : name of station
- location: Location: location of station
- type: StationType: enum for station type
- status: ActivityStatus: current status. defaults to IDLE
- inventory: Inventory: stations inventory. Defaults to none
- devices: List[Type[Device]]: list of devices connected to station
- operation_record: List[Operation] : history of operations performed by the station.
- locked: Optional[UUID]: ID of the station currently locking the station. None if not locked

**Methods**
- *get_device*: Retrieve a device from the station.
- *get_robot*: Retrieve a robot from the station.

**Usage**
- Interacts with the lab for higher-level coordination of tasks.
- Manages and supervises local devices or robots.

*Example subclass*
```python
class MyStation(Station):
    def perform_maintenance(self):
        # Custom logic for station maintenance
        pass
```

## CONNECTIONS

### rest_adapter.py

This file contains the following classes:

#### LabEngineException


#### Result

This class is responsible for converting json to python instances. 

#### RestAdapter

RestAPI adapter class and has the following set up. It contains `url`, `_api_key`, `ssl_verify` and `logger`. Disable the warning if there is no ssll certificates for https. It consist of 6 functions, 5 public and 1 private, The four public functions are *post*, *put*, *patch*, *get* and *delete*. These functions all map directly to the standard http methods. Each of these methods will take the endpoint, parameters and data as arguments.

The private function of *_do* is the private method used in all the others. The steps of the function are as follows:
1. create URL, Headers
2. Log the request to the logger then try perform a request using the requests library
3. If there's an exception raise a LabEngineException
4. Return the raw response if jsonify is set to false
5. Otherwise deserialise the response in to a python object by extracting the json, and creating a Result object, then return this so the client is left with a python object.


### lab_connection.py

The purpose of the lab connection is to allow requests to be made with function calls instead of building the requests manually each time and maps 1-1 for the endpoints of the lab server.

This is a lab adapter built composed with a RestAdapter heavily couples to the lab engine API. The lab connection is a singleton that is built using a hostname, an api_key, an ssl_verify and a logger. The RestAdapter is a variable known as rest_adapter.

When instanced creates a Session id that's used to add an identifier to requests.

The lab connection contains a few different methods

- *load_from_data_model*:  Takes a DataModel which has a UUID, cls and module_path and creates that class instance by fetching the module. Then instantiating that class object by fetching the data from the database associated with that class using the RestProxyMixin.from_id function to make sure it is tied to the database. Returns the class object.
- *construct_object*: Constructs an ObjectConstructionRequest and make a put request to the /cls/construct endpoint. Returns the id of the object.
- *get_object*: Takes an id and gets the object from the database and then constructs it using the *load_from_data_model* function mentioned before.
- *get_all_objects*: Returns a list of objects
- *delete_object*: Takes a UUID and deletes the object in the database
- *call_on_object*: Makes a request to the lab to send a request to a station to call a function on an object, then waits for the associated operation to be completed before returning the result of that operation
- *get_property*: get a property off the object with a certain id
- *set_property*: set a property off the object with a certain id
- *get_object_id*: get object id from lab given name
- *get_data*: get the data from a results data object
- *put_data*: put data into a results data object

### api_models.py

Just contains some common Data classes for use in the apis. 

- *ObjectCallRequest*
    - method: str
    - caller_id: UUID
    - args: Union[Dict, None] = None
- *ObjectCallResponse*
    - return_data: Any
    - warnings: str = Field(default=None)
- *ObjectQueryResponse*
    - id: UUID
    - cls: str
    - module_path: str
- *ObjectPropertySetRequest*
    - property: str
    - property_value: Any
    - patch_type: PatchType = Field(default=PatchType.SET)
    - patch_args: Optional[Dict[str, Any]] = Field(default=None)
- *ObjectPropertyGetRequest*
    - property: str
- *ObjectConstructionRequest*
    - object_json: str

## EQUIPMENT

### operation.py

Class representing actions performed by agents/devices.

**Attributes**  
- `caller_id` (UUID): Caller identifier  
- `method` (str): Method invoked  
- `args` (Dict): Arguments passed  
- `status` (OperationStatus): Current state. Default: `CREATED`  
- `start_timestamp` (datetime): Start time  
- `end_timestamp` (datetime): End time  
- `result` (OperationResult): Operation outcome. Default: `None`  

**Class Variable**  
- `_endpoint` (str): API endpoint (`"operations"`)  

**Usage**  
- Track operation lifecycle via timestamps/status  
- Attach results using `OperationResult`  

*Example subclass:*  
`class CustomOperation(Operation): ...`

### operation_result.py

**Abstract class** to standardize operation results. Inherit and implement methods.

**Attributes**  
- `success` (bool): Operation outcome  
- `error` (str): Failure message. Default: `""`  
- `result_data` (Any): Payload. Default: `None`  
- `data_file_name` (str): Source filename with extension. Default: `""`  
- `data_type` (str): Python data type descriptor. Default: `""`  
- `data_status` (ResultDataStatus): Data state. Default: `UNAVAILABLE`  

**Methods to be implemented by child classes**  
- `put_data() -> bool`: Convert/upload data  
- `get_data() -> Any`: Retrieve processed data  
- `save_data(path: str = None) -> bool`: Save data locally  

**Usage**  
- Track data state via `ResultDataStatus` enum
- Use `data_file_name` OR `data_type` for format info  

*Example subclass:*  
`class CustomResult(OperationResult): ...`


### robot.py

An abstract class to represent a generic robot. It contains an execute function which should be implemented for a class to be considered a robot and has an endpoint and available_tasks list

### mobile_robot.py 

An abstract class to represent a mobile robot platform which inherits from Robot, It has a go_to method as part of its contract. It contains an execute function which should be implemented for a class to be considered a robot and has an endpoinyt and available_tasks list


### device.py

**Abstract class** to standardize device attributes across all different devices. It inherits from the DataModel

**Attributes**  
- `name` (str): The name of the device.
- `inventory` (DeviceInventory): The inventory associated with the device.
- `status` (ActiveStatus): The current active status of the device. Defaults to IDLE.
- `operation_history` (List[Operation]): A list of operations performed by the device.
- `owner_station` (str): ID of the station which the device belongs to.