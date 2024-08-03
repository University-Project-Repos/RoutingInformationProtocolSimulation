# COSC364 RIP Assignment

Simulates RIP routing protocol. 

Reads _id_, _port_, and _output_ data from `.config` files with multiple example networks provided.

Completed to satisfaction for submission only just in the final moments with a significant bug fix and half an hour remaining to write a report - it was a very hectic and chaotic semester.

### Authors:

* Liam Laing
* Adam Ross

# Instructions

## Requirements

* Python3

## Run

#### Single RIP router .config file

`python3 rip_node.py <single .config file>`

#### Network of multiple RIP router .config files

`python3 rip_network.py <directory containing .config files>`

# Example

RIP routing simulation for router #1 when using a four-node network with router #3 inactived:

```
Welcome to the RIP router program. Awaiting initialization...
Router #1 has initialized successfully

----ROUTER #1 INITIALIZATION CONFIRMATION----
Router #1 ports: [1774, 1040, 1041]
Router #1 sockets and bounded ports: 
(2, <socket.socket fd=5, family=2, type=2, proto=0, laddr=('127.0.0.1', 1774)>)
(3, <socket.socket fd=6, family=2, type=2, proto=0, laddr=('127.0.0.1', 1040)>)
(4, <socket.socket fd=7, family=2, type=2, proto=0, laddr=('127.0.0.1', 1041)>)

 ###########################################
 #|  ROUTER #1 NEIGHBOUR ROUTER(S) STATUS |#
 #|---------------------------------------|#
 #| ID | Port | Metric | Active | Garbage |#
 #|---------------------------------------|#
 #|  2 | 1025 |    1   |  True  |  False  |#
 #|  3 | 1035 |    3   |  True  |  False  |#
 #|  4 | 9035 |    1   |  True  |  False  |#
 ###########################################

 ######################################
 #|     ROUTER #1 ROUTING TABLE      |#
 #|----------------------------------|#
 #| Destination | First Hop | Metric |#
 #|----------------------------------|#
 #|      2      |    2      |    1   |#
 #|      3      |    4      |    2   |#
 #|      4      |    4      |    1   |#
 ######################################

Router #2 is unresponsive for 4s

 ###########################################
 #|  ROUTER #1 NEIGHBOUR ROUTER(S) STATUS |#
 #|---------------------------------------|#
 #| ID | Port | Metric | Active | Garbage |#
 #|---------------------------------------|#
 #|  2 | 1025 |    1   | False  |  False  |#
 #|  3 | 1035 |    3   |  True  |  False  |#
 #|  4 | 9035 |    1   |  True  |  False  |#
 ###########################################

 ######################################
 #|     ROUTER #1 ROUTING TABLE      |#
 #|----------------------------------|#
 #| Destination | First Hop | Metric |#
 #|----------------------------------|#
 #|      2      |    2      |   16   |#
 #|      3      |    4      |    2   |#
 #|      4      |    4      |    1   |#
 ######################################

Triggered routing table updates to all neighbours at 3.16s

Router #3 is unresponsive for 4s

 ###########################################
 #|  ROUTER #1 NEIGHBOUR ROUTER(S) STATUS |#
 #|---------------------------------------|#
 #| ID | Port | Metric | Active | Garbage |#
 #|---------------------------------------|#
 #|  2 | 1025 |    1   | False  |  False  |#
 #|  3 | 1035 |    3   | False  |  False  |#
 #|  4 | 9035 |    1   |  True  |  False  |#
 ###########################################

 ######################################
 #|     ROUTER #1 ROUTING TABLE      |#
 #|----------------------------------|#
 #| Destination | First Hop | Metric |#
 #|----------------------------------|#
 #|      2      |    2      |   16   |#
 #|      3      |    4      |    2   |#
 #|      4      |    4      |    1   |#
 ######################################

Triggered routing table updates to all neighbours at 3.16s

Router #4 is unresponsive for 4s

 ###########################################
 #|  ROUTER #1 NEIGHBOUR ROUTER(S) STATUS |#
 #|---------------------------------------|#
 #| ID | Port | Metric | Active | Garbage |#
 #|---------------------------------------|#
 #|  2 | 1025 |    1   | False  |  False  |#
 #|  3 | 1035 |    3   | False  |  False  |#
 #|  4 | 9035 |    1   | False  |  False  |#
 ###########################################

 ######################################
 #|     ROUTER #1 ROUTING TABLE      |#
 #|----------------------------------|#
 #| Destination | First Hop | Metric |#
 #|----------------------------------|#
 #|      2      |    2      |   16   |#
 #|      3      |    4      |   16   |#
 #|      4      |    4      |   16   |#
 ######################################

Triggered routing table updates to all neighbours at 3.16s

 ###########################################
 #|  ROUTER #1 NEIGHBOUR ROUTER(S) STATUS |#
 #|---------------------------------------|#
 #| ID | Port | Metric | Active | Garbage |#
 #|---------------------------------------|#
 #|  2 | 1025 |    1   |  True  |  False  |#
 #|  3 | 1035 |    3   | False  |  False  |#
 #|  4 | 9035 |    1   | False  |  False  |#
 ###########################################

 ###########################################
 #|  ROUTER #1 NEIGHBOUR ROUTER(S) STATUS |#
 #|---------------------------------------|#
 #| ID | Port | Metric | Active | Garbage |#
 #|---------------------------------------|#
 #|  2 | 1025 |    1   |  True  |  False  |#
 #|  3 | 1035 |    3   |  True  |  False  |#
 #|  4 | 9035 |    1   | False  |  False  |#
 ###########################################

 ###########################################
 #|  ROUTER #1 NEIGHBOUR ROUTER(S) STATUS |#
 #|---------------------------------------|#
 #| ID | Port | Metric | Active | Garbage |#
 #|---------------------------------------|#
 #|  2 | 1025 |    1   |  True  |  False  |#
 #|  3 | 1035 |    3   |  True  |  False  |#
 #|  4 | 9035 |    1   |  True  |  False  |#
 ###########################################

 ######################################
 #|     ROUTER #1 ROUTING TABLE      |#
 #|----------------------------------|#
 #| Destination | First Hop | Metric |#
 #|----------------------------------|#
 #|      2      |    2      |    1   |#
 #|      3      |    4      |    2   |#
 #|      4      |    4      |    1   |#
 ######################################

Router #3 is unresponsive for 4s

 ###########################################
 #|  ROUTER #1 NEIGHBOUR ROUTER(S) STATUS |#
 #|---------------------------------------|#
 #| ID | Port | Metric | Active | Garbage |#
 #|---------------------------------------|#
 #|  2 | 1025 |    1   |  True  |  False  |#
 #|  3 | 1035 |    3   | False  |  False  |#
 #|  4 | 9035 |    1   |  True  |  False  |#
 ###########################################

 ######################################
 #|     ROUTER #1 ROUTING TABLE      |#
 #|----------------------------------|#
 #| Destination | First Hop | Metric |#
 #|----------------------------------|#
 #|      2      |    2      |    1   |#
 #|      3      |    4      |    2   |#
 #|      4      |    4      |    1   |#
 ######################################

Triggered routing table updates to all neighbours at 0.96s

 ######################################
 #|     ROUTER #1 ROUTING TABLE      |#
 #|----------------------------------|#
 #| Destination | First Hop | Metric |#
 #|----------------------------------|#
 #|      2      |    2      |    1   |#
 #|      3      |    3      |   16   |#
 #|      4      |    4      |    1   |#
 ######################################

Router #2 is unresponsive for 4s

 ###########################################
 #|  ROUTER #1 NEIGHBOUR ROUTER(S) STATUS |#
 #|---------------------------------------|#
 #| ID | Port | Metric | Active | Garbage |#
 #|---------------------------------------|#
 #|  2 | 1025 |    1   | False  |  False  |#
 #|  3 | 1035 |    3   | False  |  False  |#
 #|  4 | 9035 |    1   |  True  |  False  |#
 ###########################################

 ######################################
 #|     ROUTER #1 ROUTING TABLE      |#
 #|----------------------------------|#
 #| Destination | First Hop | Metric |#
 #|----------------------------------|#
 #|      2      |    2      |   16   |#
 #|      3      |    3      |   16   |#
 #|      4      |    4      |    1   |#
 ######################################

Triggered routing table updates to all neighbours at 0.92s

 ###########################################
 #|  ROUTER #1 NEIGHBOUR ROUTER(S) STATUS |#
 #|---------------------------------------|#
 #| ID | Port | Metric | Active | Garbage |#
 #|---------------------------------------|#
 #|  2 | 1025 |    1   |  True  |  False  |#
 #|  3 | 1035 |    3   | False  |  False  |#
 #|  4 | 9035 |    1   |  True  |  False  |#
 ###########################################

 ######################################
 #|     ROUTER #1 ROUTING TABLE      |#
 #|----------------------------------|#
 #| Destination | First Hop | Metric |#
 #|----------------------------------|#
 #|      2      |    2      |    1   |#
 #|      3      |    3      |   16   |#
 #|      4      |    4      |    1   |#
 ######################################

Router #3 is unresponsive for 24s

 ###########################################
 #|  ROUTER #1 NEIGHBOUR ROUTER(S) STATUS |#
 #|---------------------------------------|#
 #| ID | Port | Metric | Active | Garbage |#
 #|---------------------------------------|#
 #|  2 | 1025 |    1   |  True  |  False  |#
 #|  3 | 1035 |    3   | False  |   True  |#
 #|  4 | 9035 |    1   |  True  |  False  |#
 ###########################################

 ######################################
 #|     ROUTER #1 ROUTING TABLE      |#
 #|----------------------------------|#
 #| Destination | First Hop | Metric |#
 #|----------------------------------|#
 #|      2      |    2      |    1   |#
 #|      4      |    4      |    1   |#
 ######################################
```
