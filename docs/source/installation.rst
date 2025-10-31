Installation
=================

There are two ways to install ochra depending on your goals.

Lab User Installation
-----------------------------------

Using your favorite environment manager, set up your workspace and clone `ochra` repository into your desired location using the following command::
    
    git clone https://github.com/OChRA-lab/ochra.git

then using your environment install the package::

    pip install ./ochra


Lab Admin Installation
--------------------------------------
Similarly, use your favorite environment manager, set up your workspace and clone `ochra` repository into your desired location.

You need to install extra dependencies to be able to run the lab and station servers.

First, we need to install [mongoDB](https://www.mongodb.com/docs/manual/installation/).
Then using your environment install the package::

    pip install ./ochra[manager]

To control a piece of equipment, check our organization page for the equipment package and install it as well.