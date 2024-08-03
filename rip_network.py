"""
    COSC364-18S1 Internet Technologies and Engineering
    Assignment 1: RIP

    rip_network.py file

    Takes a directory with RIP configuration files as input, enters
    each file to a separate terminal command for convenient RIP routing.

    Authors:
        - Adam Ross
    Date: 27 April 2018
"""

from socket import socket, AF_INET, SOCK_DGRAM
from collections import Counter
from pathlib import Path
import sys
import os


class RipNetwork:

    LOCAL_HOST = '127.0.0.1'  # The local host IP address

    # Constants for the minimum and maximum ranges for port values

    MIN_PORT = 1024  # The min port range (but not the min id range, which is 1)
    MAX_PORT = 64000  # The max port and router-id range

    # Constants for list positions for each router in neighbour dictionary lists

    PORT = 0  # The position of the ports for each list in the neighbours dictionary
    METRIC = 1  # The pos of the metric for each list in the neighbours dictionary

    MAX_METRIC = 15  # Maximum metric cost applicable to RIP routing, 16 is inf

    def __init__(self):
        self.sock = socket(AF_INET, SOCK_DGRAM)  # socket for transmitting packets
        self.node = None  # router class instance

    def terminate(self, message):
        """
        Terminate the router program after closing resources and printing message
        :param message: The message being printed, whether in error, or otherwise
        """
        if self.node is not None:
            for in_sock in self.node.socks:
                self.node.socks[in_sock].close()
        self.sock.close()
        print("\n" + message)
        print("The RIP router program has terminated, all resources are released")
        sys.exit()

    @staticmethod
    def in_range(num, minimum=MIN_PORT, maximum=MAX_PORT):
        """
        Checks if a single port, ID, or metric is within a given range
        :param num: The port, id or metric being checked
        :param minimum: The minimum range value (either 1 for metric or 1024 for port)
        :param maximum: The maximum range value (either 15 for metric or 64000 for port)
        :return: True if ID, port or metric is within range, false otherwise
        """
        return minimum <= num <= maximum

    def prt_vld(self, port, rtr_ports, neighbour_ports):
        """
        Checks if a single port is a unique int value between 1024 and 64000
        :param port: The port being validated
        :param rtr_ports: All the ports in relation to the router
        :param neighbour_ports: The communication port for each neighbor router
        :return: True if the port is valid, false otherwise
        """
        count = (Counter(rtr_ports)[port] + Counter(neighbour_ports)[port])
        return isinstance(port, int) and self.in_range(port) and count == 1

    def id_vld(self, neighbour_id, other_ids):
        """
        Checks if a single router ID is a unique int between 1 and 64000
        :param neighbour_id: The neighbour router ID being validated
        :param other_ids: All neighbour router IDs
        :return: True if router ID is valid, false otherwise
        """
        count = Counter(other_ids)[neighbour_id]
        return isinstance(neighbour_id, int) and self.in_range(neighbour_id, 1) and count == 1


if __name__ == '__main__':
    if len(sys.argv) > 1:
        config_dir = sys.argv[1]
        path_list = Path(config_dir).glob('**/*.conf')

        for file in path_list:
            command = f"python3 rip_node.py {file}"
            os.system(f"xfce4-terminal --command='{command}' &")
    else:
        print("Error! Enter router configuration directory")
        exit(1)
