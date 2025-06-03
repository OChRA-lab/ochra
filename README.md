# OCHRA COMMON

This repo includes base classes and shared utilitlies used in both [Discovery](https://github.com/OChRA-lab/ochra_discovery) and [manager](https://github.com/OChRA-lab/ochra_manager)

### base.py

- This contains DataModel class which is the base model for all other dataclasses in OChRA
- The DataModel is a subclass of Pydantics BaseModel

**Attributes** 
- `id` (uuid): this is the uuid of the object instance
- `collection` (str): this is the collection name where the object is stored in the database
- `cls` (str): this is the name of the class which will be stored in the database
- `module_path` (str): this is the module path for the class so it can be created dynamically and transported acorss the wire

**Methods**
- *get_base_model*: to be called by children to return only the base information needed to reinstance the class


## UTILS

### enum.py

Collection of various enumration types used acorss other OChRA packages

### misc.py

Useful miscellaneous functions used acorss other OChRA packages

### mixins.py

This file contains two main classes RestProxyMixin and RestProxyMixinReadOnly

#### RestProxyMixin

A mixin class (this class provides methods for use by other classes without it having to be the parent of those classes. Check [Python mixin design pattern](https://stackoverflow.com/questions/533631/what-is-a-mixin-and-why-is-it-useful))

This mixin enables other classes to act as a **proxy for a remote API**, dynamically linking attributes to API calls via `LabConnection`. It automatically registers objects on the endpoint and replaces attribute access with **custom getters and setters** that fetch and update remote properties.

**Methods**
- `_mixin_hook(endpoint: str, object_id: str)` 
  - Establishes a lab connection and registers the object remotely.  
  - Overrides attribute access with **getter and setter methods** that interact with the API.  

- `from_id(object_id: str)`
    - This is a class method.
    - Reconstructs an instance by fetching stored attributes from the API.
    - Ensures the instance is correctly linked to its remote counterpart.
 
#### RestProxyMixinReadOnly

This mixin is identical to the former with the only difference is that it allows read only access to the object attributes without giving write permission.

### singleton_meta.py

`SingletonMeta` class is defined here, which is *thread-safe singleton metaclass*. It ensures that only one instance of a class exists across multiple threads. It maintains a dictionary of instances and uses a *thread lock* to prevent race conditions when creating a new instance. When a class with this metaclass is instantiated, the `__call__` method checks if an instance already exists; if not, it creates and stores one. Subsequent instantiations return the existing instance, making it ideal for scenarios like logging, configuration management or database connections where a single shared instance is needed.

This is mostly used to allow a shared LabConnection while only having to define the IP of the lab we connect to each time we instance it.


## STORAGE

Module that contains a variety of classes for different types of storage objects that exist in reality. The current docstrings contain enough information for these simple classes. I have added these below for the sake of brevity. The Storage classes are all inheritents of DataModel.

The majority of these classes are implemented in [discovery](https://github.com/OChRA-lab/ochra_discovery) to be used by the scientist

### consumable.py

#### Consumable
*Abstract class* representing lab consumables (caps, needles, etc.).

**Attributes**  
- `name` (str): The name of the consumable item.  
- `quantity` (int): The current quantity available.

**Methods**  
- *change_quantity(amount: int)*: Adjusts the consumable quantity by the specified amount.

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


#### Container
*Abstract class* for representing containers. This includes anything that can hold either other containers or reagents.

**Attributes**
- `type` (str): The type of the container.
- `max_capacity` (int|float): The maximum capacity of the container.
- `physical_id` (int): The physical identifier of the container. Defaults to None.
- `is_used` (bool): Indicates whether the container has been used. Defaults to False.

**Methods**
- *get_used_capacity()*: Get the used capacity of the container at present
- *get_avalable_capacity()*: Gets the available capacity of the container at present

### holder.py

#### Holder
*Abstract class* that represents any container that can hold other containers such as a rack for holding vials

**Attributes**
- `containers`: (List[Type[Container]]): list of containers inside the holder

**Methods**
- *add_container(container: Type[Container])*: Method for adding containers to the Holder
- *remove_containers(container: Type[Container])*: Method for removing containers from a holder

**Usage**
- Organise how your containers are stored

*Example Subclass*
```python
class Rack(Holder):
    def __init__(self):
        super().__init__()
```

### vessel.py

#### Vessel
*Abstract class* representing a vessel which is a container that can hold reagents

**Attributes**
- `capacity_unit` (str): The unit of measurement for the vessel's capacity.
- `reagents` (List[Reagent]): A list of reagents contained in the vessel. Defaults to an empty list.

**Methods**
- *add_reagent*(reagent: Reagent): Place a reagent in the vessel.
- *remove_reagent*(reagent_id: UUID): Remove a reagent by ID.

**Usage**
- store combinations of reagents so you know whats in the vial for example.

*Example Subclass*
```python
class Flask(Vessel):
    def __init__(self):
        super().__init__()
```

### reagent.py

#### Reagent
*Abstract class* representing chemicals used in experiments

**Attributes**
- `name` (str): The name of the reagent.
- `amount` (float): The amount of the reagent.
- `unit` (str): The unit of measurement for the amount.
- `physical_state` (Enum): The physical state of the reagent (e.g., solid, liquid, gas). Defaults to UNKNOWN.
- `properties` (Dict[str, Any]): A dictionary of additional properties of the reagent.

**Methods**
- *add_property(property: dict)*:  Add a property to the reagent
- *remove_property(property_name: str)*: Remove a property of the reagent
- *change_amount(amount: float)*: Change the amount of the reagent

*Example Subclass*
```python
class Alcohol(Reagent):
    def __init__(self, amount=100.0):
        super().__init__(properties={}, amount=amount)
```

### inventory.py

#### Inventory
*Abstract class* representing inventory that holds containers and consumables.

**Attributes**
- `owner` (DataModel): The owner of the inventory.
- `containers_max_capacity` (int): The maximum capacity of containers in the inventory.
- `containers` (List[Container]): A list of containers in the inventory. Defaults to an empty list.
- `consumables` (List[Consumable]): A list of consumables in the inventory. Defaults to an empty list.

**Methods**
- *add_container(container: Type[Container])* : Add a container to the inventory
- *remove_container(container: Type[Container])* : Remove a container from the inventory
- *add_consumable(consumable: Type[Consumable])* : Add a consumable to the inventory
- *remove_consumable(consumable: Type[Consumable])* : Remove the consumable from the inventory

## SPACES

This module contains classes for representing physical spaces in the lab.

### lab.py

#### Lab
*Abstract class* representing a laboratory.

**Attributes**  
- `stations` (List[Station]): A list of Station objects within the lab.  
- `robots` (List[Robot]): A list of Robot objects supervised by the lab.  

**Methods**  
- *get_stations():* Retrieve all Station objects in the lab.  
- *get_station(station_id: str):* Retrieve a specific station by its identifier.  
- *get_robots():* Retrieve all Robot objects in the lab.  
- *get_robot(robot_id: str):* Retrieve a specific robot by its identifier.

**Usage**  
- Acts as a high-level interface for managing stations and orchestrating operations.  
- Provides an entry point for accessing and utilising lab resources.

*Example subclass:*  
```python
class MyLab(Lab):
    def custom_method(self):
        pass
```

### location.py: 

#### Location
*Abstract class* used as a descriptor for a physical location.

**Attributes**
- `lab` (str): The name of the lab this location belongs to
- `room` (str): The room name
- `place` (str): Description of where in the room it is

**Methods**
None

**Usage**
- Used to describe the physical location of some device/station within the lab

*Example Subclass*:
```python
class CustomLocation(Location):
    def detailed_description(self) -> str:
        return f"Lab: {self.lab}, Room: {self.room}, Place: {self.place}"
```

### station.py:

#### Station
*Abstract Class* representing a station that has devices and robots attached to.

**Attributes**
- `name` (str) : name of station
- `location` (Location): location of station
- `type` (StationType): enum for station type
- `status` (ActivityStatus): current status. defaults to IDLE
- `inventory` (Inventory): stations inventory. Defaults to none
- `devices` (List[Type[Device]]): list of devices connected to station
- `operation_record` (List[Operation]) : history of operations performed by the station.
- `locked` (Optional[UUID]): ID of the user currently locking the station. None if not locked

**Methods**
- *get_device(device_identifier: str|UUID)*: Retrieve a device from the station.
- *get_robot(robot_identifier: str|UUID)*: Retrieve a robot from the station.

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

## EQUIPMENT

### operation.py

#### Operation
Class representing actions performed by agents/devices.

**Attributes**  
- `caller_id` (UUID): Caller identifier  
- `method` (str): Method invoked  
- `args` (Dict): Arguments passed  
- `status` (OperationStatus): Current state. Default: `CREATED`  
- `start_timestamp` (datetime): Start time  
- `end_timestamp` (datetime): End time  
- `result` (OperationResult): Operation outcome. Default: `None`  

**Usage**  
- Track operation lifecycle via timestamps/status  
- Attach results using `OperationResult`  

*Example subclass:*  
`class CustomOperation(Operation): ...`

### operation_result.py

#### OperationResult
*Abstract class* for standardizing operation results.

**Attributes**  
- `success` (bool): Operation outcome  
- `error` (str): Failure message. Default: `""`  
- `result_data` (Any): Payload. Default: `None`  
- `data_file_name` (str): Source filename with extension. Default: `""`  
- `data_type` (str): Python data type descriptor. Default: `""`  
- `data_status` (ResultDataStatus): Data state. Default: `UNAVAILABLE`  

**Methods to be implemented by child classes**  
- *put_data() -> bool*: Convert/upload data  
- *get_data() -> Any*: Retrieve processed data  
- *save_data(path: str = None) -> bool*: Save data locally  

**Usage**  
- Track data state via `ResultDataStatus` enum
- Use `data_file_name` OR `data_type` for format info  

*Example subclass:*  
`class CustomResult(OperationResult): ...`

### device.py

#### Device
*Abstract class* representing a generic device lab. All lab devices should inherent from this.

**Attributes**  
- `name` (str): The name of the device.
- `inventory` (DeviceInventory): The inventory associated with the device.
- `status` (ActiveStatus): The current active status of the device. Defaults to IDLE.
- `operation_history` (List[Operation]): A list of operations performed by the device.
- `owner_station` (str): ID of the station which the device belongs to.

### robot.py

#### Robot
*Abstract class* representing a generic robot. It inherits from Device.

**Attributes**
- `available_tasks` (List[str]): list of all the available tasks for execution by the robot.

**Methods to be implemented by child classes**  
- *execute(task_name: str, args: dict)*: executes the given task with the given arguments.  

### mobile_robot.py 

#### MobileRobot
*Abstract class* representing a mobile robot platform. It inherits from Robot.

**Methods to be implemented by child classes**  
- *go_to(args: dict)*: commands the mobile robot to navigate to a given location using the provided arguments.

## CONNECTIONS

### rest_adapter.py

This file contains the following classes:

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

#### LabConnection

The purpose of this class is to allow requests to be made with function calls instead of each time building requests manually to lab server endpoints.

This is adapter is built on top of RestAdapter that couples with the lab engine API. The class employes the singleton pattern, which is when instanced, it creates a session id that's used to add an identifier to requests ensuring no other connectin instance exists.

**Methods**

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

Contains Data classes for use when making API requests. 

#### ObjectCallRequest

**Attributes** 
- `method`: str
- `caller_id`: UUID
- `args`: Union[Dict, None] = None

#### ObjectCallResponse

**Attributes** 
- return_data: Any
- warnings: str = Field(default=None)

#### ObjectQueryResponse

**Attributes** 
- `id` (UUID): object id
- `cls` (str): class of the object
- `module_path` (str): module path to reconstruct the object instance dynamically

#### ObjectPropertySetRequest

**Attributes** 
- `property` (str): property name
- `property_value` (Any): value of the property
- `patch_type` (PatchType): type of property change. Defaults to PatchType.SET
- `patch_args` (Optional[Dict[str, Any]]): any arguments needed for setting the property

#### ObjectPropertyGetRequest

**Attributes** 
- `property` (str): name of the property to be retreived
  
#### ObjectConstructionRequest

**Attributes** 
- `object_json` (str): json representation for the object to be constructed in the database
