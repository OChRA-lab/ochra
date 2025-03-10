- At the moment the device information is directly taken from the in memory devices on the station
    - I think there's an argument to be made that the station should have a local persistent store like a sqlite database. 
    - It could be the database in the lab but it feels very peculiar to have two servers call one another back and forth

- The question of the day for me is do I
    - Client post to lab 
        --> construct the Operation object 
        --> post to the station and let it start the device 
        --> if response is successful then upload the Operation to the database and redirect SOMEWHERE
    - Client post to lab 
        --> post to the station and let it start the device. 
        --> construct an Operation object and send it in the response to the lab 
        --> let the lab upload the Operation to the database and redirect Somewhere


