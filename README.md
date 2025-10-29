# OCHRA DISCOVERY

This functions as a 'front end' in code for controlling devices for use by people who want to use automated devices but dont know or need to know how they actually work or are set up

Nearly everything within this module is designed in such a way to appear as if you are just using the device/station its connected to but in reality just makes http requests for everything

To actually find out how to control devices, Look to the [ochra_examples](https://github.com/OChRA-lab/ochra_examples) repo, readme in devices folder should explain. However the short version is front end proxy object(device) makes request to lab that maps to back end driver(handler) and executes given function then returns back through lab to front end as an operation object 

## UTILS

### LOCK
Lock class and context manager are for calling the lock method to restrict access to a resource so no other users can use it while you are

## STORAGE

Each of these are implementations of the abstract classes in [ochra_common](https://github.com/OChRA-lab/ochra_common), with any functions implemented as their respective http requests

The purpose of these classes is for you in your code to keep track of your experiment, they are stored in the DB and get assigned to whichever things use them if you add/remove from their inventory but mostly just to keep track of what youre doing for yourself. We have some example usages in the [ochra_examples](https://github.com/OChRA-lab/ochra_examples) repo
## SPACES

### LAB
The purpose of this class is to initiate all of the various setups we need to do to attach our program to a given lab, and then act as the director to get your stations

- init with hostname to 'pick' a lab to connect to

- *get_station* returns a station object based on name
- *get_stations* returnes the list of all station objects
- *get_robot* returns robot by name
- *get_robots* returns all robots 

### STATION

Proxy controller for station object

-*get_device* returns device object by name or uuid
-*get_robot* returns robot object by name or uuid
-*lock* locks resource to current user
-*unlock* releases resource(requires user which locked to call)

## SPACES
### OPERATION
Proxy object for operation, has no methods

### OPERATION RESULT
Proxy object for result
- *save_data* locally saves the operation_results data field to some path specified (defaults to file name in db)