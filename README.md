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


