"""
    COSC364-18S1 Internet Technologies and Engineering
    Assignment 1: RIP

    router.py file

    Authors:
        - Adam Ross
    Date: 27 April 2018
"""

from socket import socket, AF_INET, SOCK_DGRAM
from rip_network import RipNetwork
from time import time


class Router(RipNetwork):

    def __init__(self, router_id, input_ports, neighbour_specs):
        super().__init__()
        self.id = router_id  # eg: 1, 2, 3...
        self.ports = input_ports  # eg: [portA, portB, portC, ... ]
        self.neighbours = neighbour_specs  # eg: {neighbour_id: [PORT, METRIC], ... }
        self.socks = {}  # eg. {neighbour_id_a: socket for neighbour_a, ... }
        self.table = {}  # eg. {dest: [neighbour, metric]}

    def set_sockets(self):
        """
        Creates, binds sockets for each port, sets to dict (key = neighbour ID)
        """
        try:
            for neighbour_id in self.neighbours:
                pos = list(self.neighbours.keys()).index(neighbour_id)
                self.socks[neighbour_id] = socket(AF_INET, SOCK_DGRAM)
                self.socks[neighbour_id].bind((self.LOCAL_HOST, self.ports[pos]))
        except OSError as err:
            self.terminate("Error! Failed to create and bind sockets to ports: " + str(err))

        # Checks if no sockets are created to determine if no neighbour routers
        if len(self.socks) == 0:
            self.terminate("Error! No neighbour routers are available for routing")

    def metric_validation(self):
        """
        Checks if a metric is int between 1 and 15, terminates program if not
        """
        for dest in self.table:
            cost = self.table[dest][self.METRIC]  # The metric for focused router

            # Checks metric is integer
            if not isinstance(cost, int) or not self.in_range(cost, 1, self.MAX_METRIC):
                self.terminate("Error! Router #" + str(self.id) + " metric '" +
                               self.table[dest][self.METRIC] + "' to neighbour router #"
                               + str(dest) + " is invalid")

    def initialization(self):
        """
        Checks if each ID, port and metric ar valid, initializes table, sockets
        """
        # Validates the router ID
        if not (isinstance(self.id, int) and self.in_range(self.id, 1)):
            self.terminate("Error! Router ID '" + str(self.id) + "' is invalid")

        # Validates the router IDs for all neighbour routers
        for neighbour in self.neighbours:
            if not self.id_vld(neighbour, list(self.neighbours.keys())) or neighbour == self.id:
                self.terminate("Error! Neighbour router ID '" + str(neighbour) + "' is invalid")

        # Checks if there are enough number of ports for neighbour routers
        if not (len(self.ports) >= len(self.neighbours)):
            self.terminate("Error! Inconsistent port connections between routers")
        neighbour_ports = [self.neighbours[router][self.PORT] for router in self.neighbours]

        # Validates the port numbers for the router
        for port in self.ports:
            if not self.prt_vld(port, self.ports, neighbour_ports):
                self.terminate("Error! Router #" + str(self.id) + " port '" + str(port) + "' is invalid")
            self.ports[self.ports.index(port)] = int(port)

        # Validates the port numbers for all the neighbour routers
        for neighbour in self.neighbours:
            if not self.prt_vld(self.neighbours[neighbour][self.PORT], self.ports, neighbour_ports):
                self.terminate("Error! Router #" + str(neighbour) + " port '" +
                               str(self.neighbours[neighbour][self.PORT]) + "' is invalid")
            port = int(self.neighbours[neighbour][self.PORT])  # Converts the port to integer
            t = time()  # The current time for checking response rates
            self.neighbours[neighbour] = [port, self.neighbours[neighbour][self.METRIC], True, False, t]

        # Initializes the routing table
        for neighbour in self.neighbours:
            self.table[neighbour] = [neighbour, self.neighbours[neighbour][self.METRIC], 0]
        Router.metric_validation(self)  # Validates the metrics for each dest.
        Router.set_sockets(self)  # # Sets, binds sockets for each router port
