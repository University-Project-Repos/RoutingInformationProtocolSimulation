"""
    COSC364-18S1 Internet Technologies and Engineering
    Assignment 1: RIP

    message.py file

    Authors:
        - Liam Laing (and/or tutor(s))
        - Adam Ross
    Date: 27 April 2018
"""

from rip_network import RipNetwork
from collections import namedtuple
from struct import pack, unpack

HEADER_FORMAT = "BBH"
ENTRY_FORMAT = "HB"
HEADER_SIZE = 4
ENTRY_SIZE = 3
VERSION = 2
COMMAND = 2

Header = namedtuple("Header", "command version id")
Entry = namedtuple("RIP_Entry", "id metric")


def write_header(hdr):
    """
    Writes a header for the packet being transmitted
        - command: holds at least 2 states (1 byte B)
        - version: states that it holds at least 2 states (1 byte B)
        - id: needs to be at least 16 bits (2 byte H)
        - checksum: --
    :param hdr: The header being packed
    :return: The header packed
    """
    return pack(HEADER_FORMAT, hdr.command, hdr.version, hdr.id)


def write_rip_entry(rip_entry):
    """
    Writes an individual entry for the packet being transmitted
        - id: needs to be the 16 bits  (2 byte H)
        - metric: metric needs 0 -> 16 (1 byte)
    :param rip_entry: The RIP entry being packed
    :return: The RIP entry packed
    """
    return pack(ENTRY_FORMAT, rip_entry.id, rip_entry.metric)


def write_packet(table_update, sender_id):
    """
    Generates the packet string
    :param table_update: The table update being packed for transmission
    :param sender_id: The router ID of the router transmitting an update
    :return: The update packet for transmitting
    """
    entries = []

    for dest in table_update:
        entries.append(Entry(dest, table_update[dest][RipNetwork.METRIC]))
    header = Header(COMMAND, VERSION, sender_id)
    packet = write_header(header)

    for entry in entries:
        packet += write_rip_entry(entry)
    return packet


def read_packet(packet):
    """
    Extract the contents from a received update table packet, checks validity
    :param packet: The packed update table for extracting
    :return: The extracted sender ID, and the update table, or False if invalid
    """
    header, payload = packet[:HEADER_SIZE], packet[HEADER_SIZE:]
    hdr_tuple = Header._make(unpack(HEADER_FORMAT, header))
    entries = {}

    for i in range(0, len(payload), ENTRY_SIZE):
        entry = (Entry._make(unpack(ENTRY_FORMAT, payload[i: i + ENTRY_SIZE])))

        if not isinstance(hdr_tuple.id, int) and RipNetwork.in_range(hdr_tuple.id, 1):
            print("Received update packet is invalid and has been dropped")
            return False, False
        elif not isinstance(entry.id, int) and RipNetwork.in_range(entry.id, 1) or \
                not isinstance(entry.metric, int) or \
                not RipNetwork.in_range(entry.metric, 1, RipNetwork.MAX_METRIC + 1):
            print("Received update packet is invalid and has been dropped")
            return hdr_tuple.id, False

        entries[entry.id] = [hdr_tuple.id, entry.metric]
    return hdr_tuple.id, entries
