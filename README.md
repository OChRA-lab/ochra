# OCHRA MANAGER

## [OCHRA MANAGER/LAB](./ochra_manager/ochra_manager/lab)

### [Break Down Of Lab Server](./ochra_manager/ochra_manager/lab/lab_server.py)

- The lab server is a class that is composed of the fastapi router
- The lab server includes a lot of routers that extend the functionality of the server in to rest like endpoints
- It does not contain a huge amount itself it just runs the server. 

#### The Routers

##### Lab Router

###### Current API Design
- This is a router for lab specific queries, it does not follow any real RESTful API designs. it is however a http endpoint returning JSON
- *get_lab_object*: This is for querying a specific lab object (station, scientist, or robot) from a lab. There is a better way to expose these resources in an endpoint which is have shown below:
- *get_lab_objects*: This is for querying all objects of a specific collection

###### Proposition for better API design

- `/stations/{station_id}` - Get a specific station
- `/robots/{robot_id}` - Gte a specific robot
- `/scientists/{scientist_id}` - Get a specific scientis
- `/stations` - Get all statiobs
- `/robots` - Get all robots
- `/scientists` - Get all scientists

##### Decice Router

###### Current API Design

- *construct_device*: This is for adding a new device entry but I personally think it should be post not put. Post is for a new resource in a collection but put is for replacing a resource with a new one in its place but it has to already exist. `/devices/construct`
- *get_device_property*: This is for getting a reading from a device (or its latest reading in the database). has endpoint: `/devices/{_id_}/get_property`
- *modify_device_property*: This is a patch for a property the device has in the database, eg a value of temperature or something like that and has the endpoint of PATCH `/devices/{_id_}/modify_property`
- *call_device*: This is for querying a property of the device from the database or is it for calling a function on a device. I think it might be the latter because its a POST? `/devices/{_id_}/call_method`
- *get_device*: This is for getting a specific device and has the endpoint `/devices/get/{_id_}`

###### Propsition for better API design

- `/stations/{station_id}/devices` GET all devices
- `/stations/{station_id}/devices` - POST to this for a new device
- `/stations/{station_id}/devices/{device_id}` GET specific device
- `/stations/{station_id}/devices/{device_id}/properties` - GET all properties
- `/stations/{station_id}/devices/{device_id}/properties/{property_name}` - GET specific property
- `/stations/{station_id}/devices/{device_id}/properties/{property_name}` - PATCH update specific property
- `/stations/{station_id}/devices/{device_id}/operations` - POST with name="operation" and then the other required properties to start an operation


##### Station Router

EXACT SAME AS DEVICES BUT FOR STATIONS

###### Current API Design

- *construct_station*: This is for adding a new station entry but I personally think it should be post not put. Post is for a new resource in a collection but put is for replacing a resource with a new one in its place but it has to already exist. `/stations/construct`
- *get_station_property*: This is for getting a reading from a station (or its latest reading in the database). has endpoint: `/stations/{_id_}/get_property`
- *modify_station_property*: This is a patch for a property the station has in the database, eg a value of temperature or something like that and has the endpoint of PATCH `/stations/{_id_}/modify_property`
- *call_station*: This is for querying a property of the station from the database or is it for calling a function on a station. I think it might be the latter because its a POST? `/stations/{_id_}/call_method`. This does not seem like a neccessary at all thing to have. What methods to stations have that can not be an endpoint? They're not variable really.
- *get_station*: This is for getting a specific station and has the endpoint `/stations/get/{_id_}`

###### Propsition for better API design

- `/stations` GET all stations
- `/stations` - POST to this for a new stations
- `/stations/{station_id}` GET specific stations
- `/stations/{station_id}/properties` - GET all properties of a station
- `/stations/{station_id}/properties/{property_name}` - GET specific property of a station
- `/stations/{station_id}/properties/{property_name}` - PATCH update specific property on a station


##### Robot Router

EXACT SAME AS DEVICES AND STATIONS BUT FOR ROBOTS
WHY IS ROBOT DIFFERENT TO DEVICE?

###### Current API Design

- *construct_robot*: This is for adding a new robot entry but I personally think it should be post not put. Post is for a new resource in a collection but put is for replacing a resource with a new one in its place but it has to already exist. `/robots/construct`
- *get_property*: This is for getting a reading from a robot (or its latest reading in the database). has endpoint: `/robots/{_id_}/get_property`
- *modify_property*: This is a patch for a property the robot has in the database, eg a value of temperature or something like that and has the endpoint of PATCH `/robots/{_id_}/modify_property`
- *call_robot*: This is for querying a property of the robot from the database or is it for calling a function on a robot. I think it might be the latter because its a POST? `/robots/{_id_}/call_method`. This does not seem like a neccessary at all thing to have. What methods to robots have that can not be an endpoint? They're not variable really.
- *get_robot*: This is for getting a specific robot and has the endpoint `/robots/get/{_id_}`

###### Propsition for better API design

- `/robots` GET all robots
- `/robots` - POST to this for a new robots
- `/robots/{robot_id}` GET specific robots
- `/robots/{robot_id}/properties` - GET all properties of a robot
- `/robots/{robot_id}/properties/{property_name}` - GET specific property of a robot
- `/robots/{robot_id}/properties/{property_name}` - PATCH update specific property on a robot


##### Operation Router

###### Current API Design

- *construct_op* - This should be post and is for constructing Operations in the database
- *get_op_property* - This is for getting a specific past operation
- *modify_op_property* - This is for modifying an operation already in the database in the event of an error in the data
- *get_op* - This is for getting an operation by a specifc ID

###### Proposition for better API design

Operations are audit trails of device interactions. RESTful design treats them as first-class resources

- `/operations` POST a new operation to the collection
- `/operations` GET all operations
- `/operations/{operation_id}` GET to get ane existing operation by ID
- `/operations/{operation_id}` PUT to modify existing operation


##### Operation Result Router

###### Current API Design

- *construct_result* - This should be post and is for constructing Operations in the database
- *get_property* - This is for getting a specific past operation
- *modify_property* - This is for modifying an operation already in the database in the event of an error in the data
- *get_result* - This is for getting an operation by a specifc ID
- *get_data* - For getting a file response for the results
- *put data* - For uploading a file in place of another

###### Proposition for better API design

Operations are audit trails of device interactions. RESTful design treats them as first-class resources. I do not think its a good idea to have operation_results api. Why not just have operations and you can have ongoing operations that are still being updated. But here is an api for operation results if its needed

- `/operations` POST a new operation to the collection
- `/operations` GET all operations
- `/operations/{operation_id}` GET to get ane existing operation by ID
- `/operations/{operation_id}` PUT to modify existing operation

##### Storage Router

I don't need to go through this step by step. Essentially it is the same as the other APIs with basic crud operations but it is designed for 'Storage' Items which are 'consumables', 'containers', 'inventories' and 'reagents. Not sure yet how to better order these URIs because realistically they all fall under similar categories. There are other endpoints like 'scientists' that should be there too

TODO: CREATE URI LAYOUT FOR 'scientists', 'consumables', 'containers', 'inventories', and 'reagents'

Two Routers I added were the  *WebAppRouter* and *HATEOASRouter* but these two are unimportant for the purpose of documentation since I am the one responsible for them

#### Proposition for addition to servers

- An addiional function we could add to some resources on the server is to be able to subscribe to a /stream or of a resource or collection which would be live updates of that data.

### Break Down Of Lab Service which is used by lots of routers

- This service is one of the more complex parts of the ochra_manager library it contains a variety of methods most of which, if not all, are for interacting with the database
    - *patch_object*:  patches properties of a object_id using key value pairs
    - *construct_object*: for creating an object in the database

    - *call_on_object*: This is an important one 

    - *get_object_property*: this is a function that takes an ID and gets a property from an object type
    - *get_object_by_name*: This gets an object of a certain collection using the name of that object rather than the ID of the collection
    - *get_object_by_id*: This gets an object of a certain collection using ID
    - *get_all_objects*: Get all the ojects of a certain collection
    - *get_object_by_station_and_type*: This is basically get an object type but filtered by the station 

    - *patch_file*: UPDATE A FILE
    - *get_file*: GET A FILE

### DATA SERVER 

I do not really understand the point of this. The seeming use for this file server is to achieve something that can be done with a router or static mount in the main lab server

## OCHRA MANAGER/STATION



The station acts as a proxy for devices connected to it The main point of it is to organise collections of devices in to logical places mapped to real world locations but from a networking point of view it takes HTTP calls andconverts those commands in to serial or whatever protocol used by the IoT device

It is composed of a fastapi application instance which acts as the main router. It also has the follwoing attributes

- name
- location 
- type
- ip
- port
- devices
- router
- app
- station_proxy: All proxys are REST proxys for the database
- lab_conn: This is a connection to the lab

For th epurpose of this exploration I am going to ignore the routes and functionality I added and just focus on the preexisting implementation by Adam.

- *setup*: this method sets up the lab which creates the fastapi app adds the routes, Sets the Jinja templates by getting the module directory and then connects to the lab using the method.
- *_connect_to_lab*: this function creats a LabConnection class which is assigned to the *lab_conn* variable and then `self._station_proxy` is assigned a Station class whcih at a current guess would be the the way the station communicates with the devices
- *ping*: this is just a test for an active station it exists on the `/ping` endpoint
- *process_device_op*: Okay this is a seriously large method so lets look at whats happening. 
    - 1. The first thing is we try and get the device from the local station server device dictionary. 
    - 2. The id of the device is received in the http request it is a POST/PUT/PATCH method with a json body that contains an Operation object. We looked at these earlier in the Operation router. 
    - 3. We get the attribute from the method in the Operation object and try to check if it is on the device object
    - 4. we set the status of the device to BUSY and also the station_proxy status to busy. I am still not sure what the station proxy is 
    - 5. if there is a lab connection which is a Proxy for the lab..I think, Then set  the start_time property of the op in the database, then staus to IN progress. 
    - 6. set a bunch of variables now start the actual operation
    - 7. run the method 
    - 8. ones you get the resuly set the sueccess to true, result data as none and data status as unavailable. if the result is not a file or directory then set the datatype to a string and a result-data to result. and the data_status as available
    - 9. if theres an error.........
    - 10. finally at the end of the create an operation result and if the instance of result is a pure path and the result is a directory then zip it and save it. if its a fle the put the data in to the dstabase. Once it's uploaded then set the property of the file data to available
    - 11. If the lab conection exists thenm set the end timestamp to timestamp and result to the result id and finally the status of the operation to complete
- *process_robot_op*: This process robot op is essentially the exact same as the device just uses a different namespace...

## OCHRA MANAGER/CONNECTIONS

### [DB_CONNECTION](./ochra_manager/ochra_manager/connections/db_connection.py)

This is a database connecton class and SHOULD take an adapter and logger and then details to connect to the database

- *create*: This will create a new document in the specified collection
- *read*: This will read documents from teh specified collection that matches the query
- *update*: This will update the documents in the specified collection that match the query
- *delete*: This deletes the documents from the specfied collection
- *find*: This will find the first docuemnet using a query
- *find_all*: this will find all of the documents not just the first

### [MONGO_ADAPTER](./ochra_manager/ochra_manager/connections/mongo_adapter.py)

The methods here have to be the same as the db_connection and purely used for the mongo_adapter

### [STATION_CONNECTION](./ochra_manager/ochra_manager/connections/station_connection.py)

This class is for executing operationson the server. I am not really sure yet where or what this is used for

## OCHRA MANAGER/PROXY_MODELS

All proxy models are for connecting to databases. They are all Mixin class to add rest proxy functionality to a class

### [OPERATION_RESULT](./ochra_manager/ochra_manager/proxy_models/equipment/operation_result.py)
A class for operation results that inherits from the RestProxy

### [STATION](./ochra_manager/ochra_manager/proxy_models/space/station.py)
A station proxy for station models

### [INVENTORY](./ochra_manager/ochra_manager/proxy_models/storage/inventory.py)
A class for inventories


# OCHRA COMMON

### base.py

- This contains DataModel class which is th ebase model for al lother dataclasses in the databases
- The DataModel is a subclass of Pydantics BaseModel and contains the following default attributes
    - *id* this is the id of an object
    - *collection* this is the collection that the object belongs to in the database
    - *cls* this is the name of the class which will be stored in the database
    - *module_path* finally should we want to transport an instance of a class over the wire we need to know where to import the class from for creating it dynamically


## UTILS

### enum.py

This just contains a collection of ENUM types for various situations that will be used across the system. In terms of good system design I feel as though these Enums should be located where they are meant to be used since it "violates" (subjective) the locality of behavior principle

### miscs.py

This just contains one function which is a validator for wether something is a valid UUID

### mixins.py

This file contains two main classes RestProxyMixin and RestProxyMixinReadOnly

#### RestProxyMixin

a class that contains methods for use by other classes without having to be the parent class of those other classes. A mixin is a lot like a composition in fucntional programming but it is not to be instantiated it has functions that can be used by many other classes

`RestProxyMixin` enables a class to act as a **proxy for a remote API**, dynamically linking attributes to API calls via `LabConnection`. It automatically registers objects on the endpoint and replaces attribute access with **getters and setters** that fetch and update remote properties. The `from_id` method reconstructs an instance from the API using its stored data.

- **`_mixin_hook(endpoint, object_id)`**  
  - Establishes a lab connection and registers the object remotely.  
  - Overrides attribute access with **getter and setter methods** that interact with the API.  

- **`from_id(object_id)`** *(Class Method)*  
  - Reconstructs an instance by fetching stored attributes from the API.  
  - Ensures the instance is correctly linked to its remote counterpart.  

`RestProxyMixinReadOnly` Is very similar to the former but it only allows read only permission to the object. It does not allow write permissions

### singleton_meta.py

This implementation defines a **thread-safe singleton metaclass** (`SingletonMeta`), ensuring that only one instance of a class exists across multiple threads. It maintains a dictionary of instances and uses a **thread lock** to prevent race conditions when creating a new instance. When a class with this metaclass is instantiated, the `__call__` method checks if an instance already exists; if not, it creates and stores one. Subsequent instantiations return the existing instance, making it ideal for scenarios like logging, configuration management, or database connections where a single shared instance is needed.


## STORAGE

Storage is a module that contains a variety of classes for different types of storage objects that exist in reality. The current doc strings contain enough information for these simple classes. I have added these below for the sake of brevity. The Storage classes are all inheritents of DaraModel

- consumable.py: Abstract class for lab consumables such as caps, needles, etc. This is the abstract class for the rest of the classes in the module. it has one method. *change_quantity* which will be used changing the quantity of the consumable.

- container.py: Abstract class for containers, anything that can hold somehting
    - *get_used_capacity*: will get the used capacity of the container at present
    - *get_avalable_capacity*: This gets the availabel capacity of the container at present

- holder.py: This is an abstract class that represents any container that can hold another container it has two methods
    - *add_container*: a method for adding containers to the Holder
    - *remove_containers*: a method for removing containers from a holder

- inventory.py: This is an abstract class for inventory, contains containers and consumables.
    - *add_container* : Add a container to the inventory
    - *remove_container* : Remove a container from the inventory
    - *add_consumable* :Add a consumable to the inventory
    - *remove_consumable* : Remove the consumable from the inventory

- reagent.py: Abstract Reagent class to represent any chemicals used
    - *add_property*:  Add a property to the reagent
    - *remove_property*: Remove a property of the reagent
    - *change_amount*: Change the amount of the reagent

- vessel.py: Vessel Abstract class, any container that can hold reagents
    - *add_reagent* 
    - *remove_reagent*

## SPACES

This module are for classes that represent physical spaces in the real setting. Similar to storage there is notmuch business logic that has actually been implemented and so I have just provided a small excerpt below for explaining what these classes are meant to be.

- lab.py: Abstract Lab class that represents a laboratory.
    - *get_stations*: Retrive all station in the lab
    - *get_station*: Retrieve all stations in the lab.
    - *get_robots*: Retrieve all robots in the lab.
    - *get_robot*: Retrieve a specific robot from the lab.

- location.py: Abstract location to correspond to a physical location.

- station.py: Abstract station class that contains information all stations will have.
    - *get_device*: Retrieve a device from the workstation.
    - *get_robot*: Retrieve a robot from the workstation.


## CONNECTIONS

### rest_adapter.py

This file ocntains the followinh classes

#### LabEngineException


#### Result

This class is responsible for converting json to python instances. I do not think it is fully implemented but it contains status code message and data

#### RestAdapter

The RestAPI adapter class and has the following set up. It contains `url`, `_api_key`, `ssl_verify` and `logger`. Disable the warning if there is no ssll certificates for https. It consist of 5 functions, 4 public and 1 private, The four public functions are *post*, *put*, *patch*, *get* and *delete*. These functions all map directly to the same http methods you would expect. Each of these methods will take the endpint, parameters and data as arguments.

The private function of *_do* is the private method used in all the others. The steps of the function are as followed
    - 1. create URL, Headers
    - 2. Log the request to the logger then try perform a request using the requests library
    - 3. if theres an excepion raise a LabEngineException
    - 4. Return the raw response if jsonify is set to false
    - 5. Otherwise desrialise the response in to a python object by extracting the json, and creating a Result object, then return this so the client is left with a python object.

### api_models.py

Just contains some commmon Data classes for use in the apis. I have included the classes, they're data and the types of their data

- *ObjectCallRequest*
    - method: str
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
- *ObjectPropertyGetRequest*
    - property: str
- *ObjectConstructionRequest*
    - object_json: str

### lab_connection.py

This is a lab adapter built composed with a RestAdapterheavily couples to the lab engine API. The lab connection is a singleton that is built using a hostname, an api_key, an ssl_verify and a logger. The RestAdapter is a variable known as rest_adapter.

The lab connection contains a few differnet methods

- *load_from_response*: This functiin takes an ObjectQueryResponse which has a UUID, cls and module_path and creates that clas sinstance by fetching the module (Which is an object). Then the object and finally instantiating that object by fetching the data from the database associated with that class using the RestProxyMixin.from_id function to make sure it is tied to the database

- *construct_object*: This function constructs an ObjectConstructionResult and then makes a put request to the /cls/construct endpoint. It will then return the id of the object.
- *get_object*: This function takes an id and gets the obejct from the database and then constructs it using the *load_from_response* function mentioned before. I feel as though load_from_response should be private so I changed it to that
    - *get_all_objects*: This does the same as above just returns a list of objects
- *delete_object*: Takes a UUID and deletes the object in the database
- *call_on_object*: This function calls a method on a device or robot (device and robot are the saem tho....) but it basically calls the lab and asks it to get the obejct from the database run the method on the device which will change the object in physcial reality and the python object and then to load the object and return it
- *get_property*: get a property off the object with a certain id
- *set_property*: set a property off the object with a certain id
- *_convert_to_object_query_response_possibility*: convert data to ObjectQueryResponse if possible
- *get_object_id*: get object id from lab given name
- *get_data*: get the data from a results data object
- *put_data*: put data into a results data object



## CONNECTIONS

### operation.py

**Abstract class** representing actions performed by agents/devices.

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

**Methods to Implement**  
- `put_data() -> bool`: Convert/upload data  
- `get_data() -> Any`: Retrieve processed data  
- `save_data(path: str = None) -> bool`: Save data locally  

**Usage**  
- Track data state via `ResultDataStatus` enum  
- Use `data_file_name` OR `data_type` for format info  

*Example subclass:*  
`class CustomResult(OperationResult): ...`


### robot.py

An abstarct class to represent a generic robot. It contains an execute function which should be implemented for a class to be considered a robot and has an endpoinyt and available_tasks list

### mobile_robot.py

An abstarct class to represent a mobile robot platform which inherits from Robot, It has a go_to method as part of its contract. It contains an execute function which should be implemented for a class to be considered a robot and has an endpoinyt and available_tasks list


### device.py


**Abstract class** to standardize device attributes across all different devices. It inherits from the DataModl

**Attributes**  
- `name` (str): The name of the device.
- `inventory` (DeviceInventory): The inventory associated with the device.
- `status` (ActiveStatus): The current active status of the device. Defaults to IDLE.
- `operation_history` (List[Operation]): A list of operations performed by the device.
- `owner_station` (str): ID of the station which the device belongs to.

**Methods to Implement**  
- `__init_subclass__`: this means that any subclass of Device will be initialised and then a list will be created called _ui_states and _ui_forms which will add all of the methods with `_form_metadata` and attributes annotated with `_display_metadata` to ui_froms and ui_states respectively. The metadata is acquired in Concrete subclasses by annotating attributes with functions in the uigenerators.py file
- `to_html`: This method returns a html string by using HypermediaBuilder from the uigenerators.py file

### uigenerators.py

#### FormMetaData
**Data class** 

#### DisplayMetadata
**Data class** 

#### HTMLFormMetadata
**Decorator** 

#### HTMLStateMetadata
**Decorator**

#### HypermediaBuilder
**Concrete class** 
