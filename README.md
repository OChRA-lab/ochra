# OCHRA MANAGER

  

For the User that interacts with devices and sets up the labs

  
  
  

## [OCHRA MANAGER/LAB](./ochra_manager/ochra_manager/lab)

  

### [Break Down Of Lab Server](./ochra_manager/ochra_manager/lab/lab_server.py)

  

- The lab server is a class that is composed of the fastapi router

- The lab server includes a lot of routers that extend the functionality of the server in to rest like endpoints

- It does not contain a huge amount itself it just runs the server and the scheduler

  

#### The Routers

Each router makes use of the Lab_service class to do the common functionality methods in an attempt to avoid code duplication while still allowing for specific object specific additions

  

##### Lab Router

  

###### Current API Design

- This is a router for lab specific queries

- *get_lab_object*: This is for querying a specific lab object (station, scientist, or robot) from a lab.

- *get_lab_objects*: This is for querying all objects of a specific collection

  
  

##### Device Router

  

###### Current API Design

  

- *construct*: This is for adding a new device entry but it should be post not put. `/devices/construct`

- *get_property*: This is for getting a reading from a device (or its latest reading in the database). has endpoint: `/devices/{_id_}/get_property`

- *modify_property*: This is a patch for a property the device has in the database, e.g. a value of temperature or something like that and has the endpoint of PATCH `/devices/{_id_}/modify_property`

- *call_method*: This is for calling a method on a device, firstly we use the lab_service to create our operation, then we pass it to the scheduler to be executed `/devices/{_id_}/call_method`

- *get_*: This is for getting a specific device and has the endpoint `/devices/get/{_id_}`

  
  

##### Station Router

  

EXACT SAME AS DEVICES BUT FOR STATIONS

  

##### Robot Router

  

EXACT SAME AS DEVICES AND STATIONS BUT FOR ROBOTS

  
  

##### Operation Router

  

###### Current API Design

  

- *construct_op* - This  is for constructing Operations in the database

- *get_op_property* - This is for getting a specific past operation

- *modify_op_property* - This is for modifying an operation already in the database in the event of an error in the data

- *get_op* - This is for getting an operation by a specifc ID

  

##### Operation Result Router

  

###### Current API Design

  

- *construct_result* - This is for constructing Operations in the database

- *get_property* - This is for getting a specific past operation

- *modify_property* - This is for modifying an operation already in the database in the event of an error in the data

- *get_result* - This is for getting an operation by a specifc ID

- *get_data* - For getting a file response for the results

- *put data* - For uploading a file in place of another

  
  

### Break Down Of Lab Service which is used by lots of routers

  

- This service is one of the more complex parts of the ochra_manager library it contains a variety of methods most of which, if not all, are for interacting with the database

    - *patch_object*:  patches properties of a object_id using key value pairs

    - *construct_object*: for creating an object in the database

  

    - *call_on_object*: creates operations based on requests to allow the scheduler to call the objects

  

    - *get_object_property*: this is a function that takes an ID and gets a property from an object type

    - *get_object_by_name*: This gets an object of a certain collection using the name of that object rather than the ID of the collection

    - *get_object_by_id*: This gets an object of a certain collection using ID

    - *get_all_objects*: Get all the ojects of a certain collection

    - *get_object_by_station_and_type*: This is basically get an object type but filtered by the station

  

    - *patch_file*: UPDATE A FILE

    - *get_file*: GET A FILE

  
  

## OCHRA MANAGER/STATION

  
  

The station acts as a proxy for devices connected to it The main point of it is to organize collections of devices in to logical places mapped to real world locations but from a networking point of view it takes HTTP calls and converts those commands in to serial or whatever protocol used by the IoT device

  

It is composed of a fastapi application instance which acts as the main router. It also has the following attributes

  

- name

- location

- type

- ip

- port

- devices

- router

- app

- station_proxy: All proxies are REST proxies for the database

- lab_conn: This is a connection to the lab

  
  

- *setup*: this method sets up the lab which creates the fastapi app adds the routes then connects to the lab using the method.

- *_connect_to_lab*: this function creats a LabConnection class which is assigned to the *lab_conn* variable and then `self._station_proxy` is assigned a Station class which is the the way the station communicates its properties to the lab

- *ping*: this is just a test for an active station it exists on the `/ping` endpoint

- *process_op*:

    - 1. The first thing is we try and get the device from the local station server device dictionary.

    - 2. The id of the device is received in the http request it is a POST/PUT/PATCH method with a json body that contains an Operation object.

    - 3. We get the attribute from the method in the Operation object and try to check if it is on the device object

    - 4. we set the status of the device to BUSY and also the station_proxy status to busy.

    - 5. set the start_time property of the op in the database, then status to IN progress.

    - 6. set a bunch of variables now start the actual operation

    - 7. run the method

    - 8. ones you get the result set the success to true, result data as none and data status as unavailable. if the result is not a file or directory then set the datatype to a string and a result-data to result. and the data_status as available

    - 9. if there is an error set the operation result to that error and success to false

    - 10. finally at the end of the create an operation result and if the instance of result is a pure path and the result is a directory then zip it and save it. if its a file the put the data in to the database. Once it's uploaded then set the property of the file data to available

    - 11. If the lab connection exists then set the end timestamp to timestamp and result to the result id and finally the status of the operation to complete

  
  

## OCHRA MANAGER/CONNECTIONS

  

### [DB_CONNECTION](./ochra_manager/ochra_manager/connections/db_connection.py)

  

This is a database connecton class and SHOULD take an adapter and logger and then details to connect to the database

  

- *create*: This will create a new document in the specified collection

- *read*: This will read documents from the specified collection that matches the query

- *update*: This will update the documents in the specified collection that match the query

- *delete*: This deletes the documents from the specfied collection

- *find*: This will find the first docuemnet using a query

- *find_all*: this will find all of the documents not just the first

  

### [MONGO_ADAPTER](./ochra_manager/ochra_manager/connections/mongo_adapter.py)

  

The methods here have to be the same as the db_connection and purely used for the mongo_adapter

  

### [STATION_CONNECTION](./ochra_manager/ochra_manager/connections/station_connection.py)

  

This class is for executing operations on the server. It's essentially the same as the lab connection but maps to the station functionality

  

## OCHRA MANAGER/PROXY_MODELS

  

All proxy models are for connecting to databases. They are all Mixin class to add rest proxy functionality to a class

  

### [OPERATION_RESULT](./ochra_manager/ochra_manager/proxy_models/equipment/operation_result.py)

A class for operation results that inherits from the RestProxy

  

### [STATION](./ochra_manager/ochra_manager/proxy_models/space/station.py)

A station proxy for station models

  

### [INVENTORY](./ochra_manager/ochra_manager/proxy_models/storage/inventory.py)

A class for inventories

  
  

## Scheduler

  

The Scheduler does a lot of the heavy lifting for passing requests around between the front and back ends, it has a Queue and db connection to allow it to make db entries

  

- *add_operation* adds an operation to the queue

- *run* makes a thread to run the _schedule method in and then starts it

- *_resolve_station_id* using the operation information find out the id we need to make the request to

- *_execute_op* using the id we found before, get the IP of the station to make the request to and use the station connection class to build the request correctly for that station, then request the process_op endpoint which handles the device execution and update the DB as needed

  

- *_schedule* essentially is just a queue for operations to be tried over and over.

    - for each operation in the queue

        - get the station we need to do the request to

        - if station is free

        - if the station is not locked

        - remove the op from the queue

        - create a new thread to make the execute request with the *_execute_op* method

        - update the queue in DB if things have changed (so we can recover maybe)