"""
    COSC364-18S1 Internet Technologies and Engineering
    Assignment 1: RIP

    rip_node.py file

    Authors:
        - Adam Ross
    Date: 27 April 2018
"""

from message import write_packet, read_packet
from rip_network import RipNetwork
from time import time, sleep
from random import uniform
from router import Router
from select import select
import configparser
import sys


class RipNode(RipNetwork):

    BUFFER = 512  # Maximum chars read from file - referenced from COSC264 TCP/UDP project (by self)

    # Constants for periodic and timeout timers

    COLLECT = 24  # Garbage collection timer (default is 180). Must be 6 * PERIOD
    PERIOD = 4  # 4-second period for 'time out'. Dependent on size of network

    # Constants for list positions for each router in neighbour dictionary lists

    ACTIVE = 2  # Pos in neighbour router list for if 'sending msg' boolean
    GARBAGE = 3  # Pos in neighbour router list for if 'router garbage' boolean
    RESPONSE_TIME = 4  # Pos in neighbour router list for response time of router
    TIMER = 2  # Pos for the timer in routing table for when dest has metric = 16
    INF = 16  # The value given for any metric cost considered unreachable in RIP

    IS_GARBAGE_COLLECTION = True  # if garbage collection; if permanently removes inactive router or waits for activity
    IS_DEBUGGING = False

    def __init__(self):
        RipNetwork.__init__(self)

    def configure(self, file):
        """
        Reads a configuration file for the router ids, ports and metrics
        specs, then creates a Router class instance with neighbour router specs
        :param file: The router configuration file
        :return: A class instance for the router with neighbour router specs
        """
        conf = configparser.ConfigParser()
        conf.read(file)  # Reads data from config file, and closes file
        conf = conf["ROUTER"]  # The config file data
        self.node = Router(eval(conf["id"]), eval(conf["ports"]), eval(conf["outputs"]))
        return self.node

    def update_period(self):
        """
        Returns generated random double between 0.5s and 'PERIOD' * 1/3 time
        :return: The time when the next update message will be transmitted
        """
        return time() + uniform(0.5, self.PERIOD * 1/3)

    def set_garbage(self, router):
        """
        Sets a neighbour router as 'GARBAGE' if inactive for the COLLECT period.
        Removes all destinations that 'router' is the next hop to and metric = 16
        :param router: The router not responding for the duration of COLLECT period
        """
        self.node.neighbours[router][self.GARBAGE] = True

        if self.IS_GARBAGE_COLLECTION:
            for dest in list(self.node.table.keys()):
                if self.node.table[dest][0] == router:
                    self.node.table.pop(dest)
        else:
            deleting = {router}

            for dest in self.node.table:
                if self.node.table[dest][0] == router and self.node.table[dest][self.METRIC] == self.INF:
                    if dest in self.node.neighbours and self.node.neighbours[dest][self.ACTIVE]:
                        self.node.table[dest] = [dest, self.node.neighbours[dest][self.METRIC]]
                    elif dest in self.node.neighbours:
                        self.node.neighbours[dest][self.GARBAGE] = True
                if self.is_garbage(self.node.table[dest][self.TIMER]):
                    deleting |= {dest}

            for dest in deleting:
                self.node.table.pop(dest)

        print("\nRouter #" + str(router) + " is unresponsive for " + str(self.COLLECT) + "s")
        self.print_neighbours_status()

        if len(self.node.table) > 0:
            self.print_routing_table()

    def set_inactive(self, router, period_start_time):
        """
        Sets a neighbour router as 'INACTIVE' if unresponsive for the PERIOD time
        Sets 'router', destinations via router metric to 16, sends triggered update
        :param router: The router not responding for the duration of PERIOD time
        :param period_start_time: The time at the start of the period
        """
        self.node.neighbours[router][self.ACTIVE] = False

        if not self.IS_GARBAGE_COLLECTION:
            for neighbour in self.node.neighbours:
                if self.node.table[neighbour][0] == router:
                    self.node.table[neighbour] = [neighbour, self.node.neighbours[neighbour][self.METRIC], 0]

        for dest in self.node.table:
            if self.node.table[dest][0] == router:
                if not self.IS_GARBAGE_COLLECTION and self.node.table[dest][self.TIMER] == 0:
                    self.node.table[dest] = [self.node.table[dest][0], self.INF, time()]
                else:
                    self.node.table[dest] = [router, self.INF, time()]
        if not self.IS_GARBAGE_COLLECTION:
            self.node.table[router] = [router, self.INF, time()]

        print("\nRouter #" + str(router) + " is unresponsive for " + str(self.PERIOD) + "s")
        self.print_neighbours_status()
        self.print_routing_table()

        t = str(round(time() - period_start_time, 2))
        print("\nTriggered routing table updates to all neighbours at " + t + "s")
        self.transmit_updates()  # Triggered updates for the change in routing table

    def is_inactive(self, start_time):
        """
        Checks if a router is not responding within the PERIODIC time
        :param start_time: The time that the response check period started
        :return: True if router not responding within PERIODIC time, or false
        """
        return (time() - start_time) > (self.PERIOD + 1)

    def is_garbage(self, start_time):
        """
        Checks if a router is not responding within the TIMEOUT period of time
        :param start_time: The time that the response check period started
        :return: True if router now responding within TIMEOUT period, or false
        """
        return (time() - start_time) > self.COLLECT

    def set_neighbour_status(self, period_start_time):
        """
        Checks if each router is responding within PERIOD and COLLECTION times
        :param period_start_time: The time at the start of the period
        :return: True when all neighbour /destination router status are updated
        """
        for neighbour in self.node.neighbours:
            response_time = self.node.neighbours[neighbour][self.RESPONSE_TIME]

            if self.is_inactive(response_time) and self.node.neighbours[neighbour][self.ACTIVE]:
                self.set_inactive(neighbour, period_start_time)
            elif self.is_garbage(response_time) and not self.node.neighbours[neighbour][self.GARBAGE]:
                self.set_garbage(neighbour)
        deleting = []

        for dest in self.node.table:
            if self.node.table[dest][self.METRIC] == self.INF and self.node.table[dest][self.TIMER] == 0:
                self.node.table[dest][self.TIMER] = time() - self.COLLECT
            elif self.node.table[dest][self.METRIC] == self.INF and self.is_garbage(self.node.table[dest][self.TIMER]):
                deleting.append(dest)

        if len(deleting) > 0:
            for delete in deleting:
                self.node.table.pop(delete)

            if len(self.node.table) > 0:
                self.print_routing_table()
        return True

    def reset_response_time(self, rtr):
        """
        Resets the response time of the neighbour router dictionary to current time
        :param rtr: The router being updated with the current time
        """
        if self.node.neighbours[rtr][self.GARBAGE]:
            self.node.neighbours[rtr][self.GARBAGE] = False
            self.node.neighbours[rtr][self.ACTIVE] = True
            metric = self.node.neighbours[rtr][self.METRIC]
            self.node.table[rtr][self.METRIC] = metric
            self.print_neighbours_status()
        elif not self.node.neighbours[rtr][self.ACTIVE]:
            self.node.neighbours[rtr][self.ACTIVE] = True
            self.print_neighbours_status()
        self.node.neighbours[rtr][self.RESPONSE_TIME] = time()

    def print_router_specs(self):
        """
        Prints the router specs, such ports, and neighbour IDs, ports and metrics
        """
        print("\n----ROUTER #" + str(self.node.id) + " INITIALIZATION CONFIRMATION----")
        print("Router #" + str(self.node.id) + " ports: " + str(self.node.ports))
        print("Router #" + str(self.node.id) + " sockets and bounded ports: ")

        # Prints each socket, including bound port, designated neighbour router ID
        for in_sock in self.node.socks.items():
            print(in_sock)
        self.print_neighbours_status()

    def print_neighbours_status(self):
        """
        Prints the status of the neighbour routers, with ID, last response time...
        """
        print("\n ###########################################")
        ttl = " #|  ROUTER #" + str(self.node.id) + " NEIGHBOUR ROUTER(S) STATUS |#"

        if self.node.id > 9:
            ttl = " #| ROUTER #" + str(self.node.id) + " NEIGHBOUR ROUTER(S) STATUS |#"
        print(ttl)
        print(" #|---------------------------------------|#")
        print(" #| ID | Port | Metric | Active | Garbage |#")
        print(" #|---------------------------------------|#")

        for router in self.node.neighbours:
            if self.node.neighbours[router][self.ACTIVE]:
                active = "   |  " + str(self.node.neighbours[router][self.ACTIVE])
            else:
                active = "   | " + str(self.node.neighbours[router][self.ACTIVE])

            if self.node.neighbours[router][self.GARBAGE]:
                garbage = "  |   " + str(self.node.neighbours[router][self.GARBAGE])
            else:
                garbage = "  |  " + str(self.node.neighbours[router][self.GARBAGE])

            if router > 9:
                rtr = " #| " + str(router) + " | "  # The neighbour router ID
            else:
                rtr = " #|  " + str(router) + " | "  # The neighbour router ID
            prt = str(self.node.neighbours[router][self.PORT])  # Neighbour router in port

            if self.node.neighbours[router][self.METRIC] > 9:
                metric = " |   " + str(self.node.neighbours[router][self.METRIC])  # Metric
            else:
                metric = " |    " + str(self.node.neighbours[router][self.METRIC])  # Metric
            print(rtr + prt + metric + active + garbage + "  |#")
        print(" ###########################################")

    def print_routing_table(self):
        """
        Prints the status of the routing table, with destination, metric, neighbour
        """
        print("\n ######################################")
        ttl = " #|     ROUTER #" + str(self.node.id) + " ROUTING TABLE      |#"

        if self.node.id > 9:
            ttl = " #|     ROUTER #" + str(self.node.id) + " ROUTING TABLE     |#"
        print(ttl)
        print(" #|----------------------------------|#")
        print(" #| Destination | First Hop | Metric |#")
        print(" #|----------------------------------|#")

        for dest in self.node.table:
            dst = " #|      " + str(dest)  # The destination router ID

            if dest > 9:
                dst = " #|     " + str(dest)
            neighbour = "      |    " + str(self.node.table[dest][0])  # Closest neighbour

            if self.node.table[dest][0] > 9:
                neighbour = "      |   " + str(self.node.table[dest][0])
            metric = "      |    " + str(self.node.table[dest][self.METRIC])  # Metric to dest

            if self.node.table[dest][self.METRIC] > 9:
                metric = "      |   " + str(self.node.table[dest][self.METRIC])  # Metric
            print(dst + neighbour + metric + "   |#")
        print(" ######################################")

    def bellman_ford(self, table_update, rtr_id, updated):
        """
        A variant of the Bellman-Ford algorithm. Calculates the shortest path to
        each provided destination. Compares new message metrics to current metrics
        :param table_update: Table from update message; {dest:[ID, metric], ...}
        :param rtr_id: The router ID of router sending the table message update
        :param updated: A boolean that is set to True if the table is changed
        :return: True if there is a change to the table, False otherwise
        """
        if rtr_id in self.node.table:
            if self.node.neighbours[rtr_id][self.METRIC] < self.node.table[rtr_id][self.METRIC]:
                self.node.table[rtr_id] = [rtr_id, self.node.neighbours[rtr_id][self.METRIC], 0]
                updated = True
        else:
            self.node.table[rtr_id] = [rtr_id, self.node.neighbours[rtr_id][self.METRIC], 0]
            updated = True

        for dest in table_update:
            new_metric = table_update[dest][self.METRIC]  # New metric from update
            # The metric between the router and the neighbour message sent from
            neighbour_metric = self.node.neighbours[rtr_id][self.METRIC]
            # Increment to update table metric the existing neighbour metrics
            metric = new_metric + neighbour_metric

            if not self.in_range(metric, 1, self.MAX_METRIC):
                metric = self.INF  # Sets the metric to infinity / unreachable

            if dest in self.node.neighbours.keys() and self.node.neighbours[dest][self.ACTIVE]:
                if self.node.neighbours[dest][self.METRIC] < metric:
                    if dest in self.node.table:
                        if self.node.neighbours[dest][self.METRIC] < self.node.table[dest][self.METRIC]:
                            self.node.table[dest] = [dest, self.node.neighbours[dest][self.METRIC], 0]
                            updated = True
                            continue
            elif dest in self.node.neighbours.keys() and not self.node.neighbours[dest][self.GARBAGE]:
                if self.node.table[dest][self.METRIC] != self.INF:
                    self.node.table[dest] = [dest, self.INF, time()]
                    updated = True
                    continue
            elif dest in self.node.neighbours.keys():
                continue

            if dest != self.node.id:
                if dest not in self.node.table:
                    self.node.table[dest] = [rtr_id, metric, 0]
                    updated = True
                elif metric < self.node.table[dest][self.METRIC]:
                    if dest in self.node.neighbours.keys():
                        if self.node.neighbours[dest][self.ACTIVE]:
                            self.node.table[dest] = [rtr_id, metric, 0]
                            updated = True
                    else:
                        self.node.table[dest] = [rtr_id, metric, 0]
                        updated = True

                if self.node.table[dest][0] == rtr_id and self.node.table[dest][self.METRIC] != metric:
                    self.node.table[dest] = [self.node.table[dest][0], metric, 0]
                    updated = True
        return updated

    def split_horizon_poison_reverse(self, neighbour_id):
        """
        Creates specific routing table where each entry has the
        neighbour router as the next hop has a metric set to 16
        This is so split horizon with poison reverse is implemented
        :param neighbour_id: The router being sent update table
        :return: The temporary table for sending to specified router
        """
        tables = {}

        for table in self.node.table:
            if self.node.table[table][self.TIMER] == 0 or not self.is_garbage(self.node.table[table][self.TIMER]):
                tables[table] = [self.node.table[table][0], self.node.table[table][self.METRIC]]

                if self.node.table[table][0] == neighbour_id:
                    tables[table][self.METRIC] = self.INF
        return tables

    def transmit_updates(self):
        """
        Sends an update message with table to each neighbour router port
        :return: True after the update messages with routing tables sent
        """
        for router in self.node.neighbours:
            # Checks that each neighbour router is not set as 'GARBAGE' first
            if self.node.neighbours[router][self.ACTIVE]:
                port = self.node.neighbours[router][self.PORT]  # port transmitting to
                table = self.split_horizon_poison_reverse(router)  # update table
                self.sock.sendto(write_packet(table, self.node.id), (self.LOCAL_HOST, port))
        return True

    def route(self):
        """
        Main program for RIP routing
        """
        in_port_sockets = [self.node.socks[neighbour_id] for neighbour_id in self.node.socks]
        status_set = transmit = True  # Initialize boolean for atomicity
        timer = periodic = 0  # Initialize timer and period for atomicity
        rip_time = time()  # For timing the RIP routing in entirety
        updated = False

        while True:
            if (timer + self.PERIOD) < time() and status_set:
                if updated:
                    self.print_routing_table()  # Prints routing table if table has changed

                if self.IS_DEBUGGING:
                    sleep(self.PERIOD * 1/6)  # Offset the start of each period
                    t = str(round(time() - rip_time)) + " second"
                    print("\nNew " + str(self.PERIOD) + "s period has begun at " + t + "s")

                status_set = updated = transmit = False  # Reset booleans
                timer = time()  # Resets timer for checking if within PERIOD
                periodic = self.update_period()  # Resets time for min # msgs per PERIOD

            # For sending min # messages per 'PERIOD' time
            if periodic < time() and not transmit:
                if self.IS_DEBUGGING:
                    t = str(round(time() - rip_time, 2))
                    print("\nPeriodic routing table updates transmitted at " + t + "s")

                transmit = self.transmit_updates()  # Transmits update messages

            if transmit and (timer + self.PERIOD * 1/3) > time():
                msgs, _, _ = select(in_port_sockets, [], [], self.PERIOD * 1/2)

                if msgs:
                    for msg in msgs:
                        rtr_id, msg_table = read_packet(msg.recv(self.BUFFER))

                        if rtr_id:
                            if msg_table:
                                updated = self.bellman_ford(msg_table, rtr_id, updated)
                            self.reset_response_time(rtr_id)

            if (timer + (self.PERIOD * 5/6)) > time() and transmit and not status_set:
                status_set = self.set_neighbour_status(timer)
                # Checks all routers have been flagged as GARBAGE, exits loop if so
                if False not in [self.node.neighbours[neighbour][self.GARBAGE] for neighbour in self.node.neighbours]:
                    print("\nAll routers now unresponsive for " + str(self.COLLECT)+"s")
                    break

        rip_time = str(round(time() - rip_time))
        print("\nThe total period for all RIP routing is: " + rip_time + "s")
        self.terminate("RIP routing demo has completed for router #" + str(self.node.id))


if __name__ == '__main__':
    rip_node = RipNode()

    if len(sys.argv) > 1:
        print("Welcome to the RIP router program. Awaiting initialization...")

        # Reads data from config file, creates a Router instance called node
        try:
            node = rip_node.configure(sys.argv[1])  # Creates router object from file
        except Exception as err:
            rip_node.terminate("Error! Router file configuration failed: " + str(err))

        rip_node.node.initialization()  # Validates data, initializes table, sockets
        print("Router #" + str(rip_node.node.id) + " has initialized successfully")
        rip_node.print_router_specs()  # Prints the router specifications after init.

        rip_node.route()  # Main method for RIP data transmission and processing
    else:
        rip_node.terminate("Error! Enter a valid router configuration file")
