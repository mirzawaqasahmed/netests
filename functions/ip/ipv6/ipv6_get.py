#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
Add a description ....

"""

__author__ = "Dylan Hamel"
__maintainer__ = "Dylan Hamel"
__version__ = "1.0"
__email__ = "dylan.hamel@protonmail.com"
__status__ = "Prototype"
__copyright__ = "Copyright 2019"

########################################################################################################################
#
# HEADERS
#

ERROR_HEADER = "Error import [ipv6_gets.py]"
HEADER_GET = "[netests - get_ipv6]"

########################################################################################################################
#
# Import Library
#

try:
    from const.constants import *
except ImportError as importError:
    print(f"{ERROR_HEADER} const.constants")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from functions.ip.ipv6.ipv6_converters import _napalm_ipv6_converter
    from functions.ip.ipv6.ipv6_converters import _cumulus_ipv6_converter
    from functions.ip.ipv6.ipv6_converters import _nexus_ipv6_converter
    from functions.ip.ipv6.ipv6_converters import _ios_ipv6_converter
    from functions.ip.ipv6.ipv6_converters import _iosxr_ipv6_converter
    from functions.ip.ipv6.ipv6_converters import _arista_ipv6_converter
    from functions.ip.ipv6.ipv6_converters import _juniper_ipv6_converter
    from functions.ip.ipv6.ipv6_converters import _extreme_vsp_ipv6_converter
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.ip.ipv6.ipv6_converters")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from nornir.core import Nornir
    # To use advanced filters
    from nornir.core.filter import F
    # To execute netmiko commands
    from nornir.plugins.tasks.networking import netmiko_send_command
    # To execute napalm get config
    from nornir.plugins.tasks.networking import napalm_get
    # To print task results
    from nornir.plugins.functions.text import print_result
except ImportError as importError:
    print(f"{ERROR_HEADER} nornir")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.vrf.vrf_get import get_vrf_name_list
    from functions.vrf.vrf_get import get_vrf
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.vrf")
    print(importError)
    exit(EXIT_FAILURE)

try:
    import json
except ImportError as importError:
    print(f"{ERROR_HEADER} json")
    exit(EXIT_FAILURE)
    print(importError)

try:
    import textfsm
except ImportError as importError:
    print(f"{ERROR_HEADER} textfsm")
    exit(EXIT_FAILURE)
    print(importError)

########################################################################################################################
#
# Functions
#
def get_ipv6(nr: Nornir, *, get_vlan=True, get_loopback=True, get_peerlink=True, get_vni=False, get_physical=True):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    get_vrf_name_list(nr)

    data = devices.run(
        task=generic_ipv6_get,
        get_vlan=get_vlan,
        get_loopback=get_loopback,
        get_peerlink=get_peerlink,
        get_vni=get_vni,
        get_physical=get_physical,
        on_failed=True,
        num_workers=10
    )
    #print_result(data)

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic function
#
def generic_ipv6_get(task, *, get_vlan=True, get_loopback=True, get_peerlink=True, get_vni=False, get_physical=True):

    use_ssh = False

    if NEXUS_PLATEFORM_NAME in task.host.platform or ARISTA_PLATEFORM_NAME in task.host.platform or \
            CISCO_IOSXR_PLATEFORM_NAME in task.host.platform or CISCO_IOS_PLATEFORM_NAME in task.host.platform or \
            JUNOS_PLATEFORM_NAME in task.host.platform:
        if 'connexion' in task.host.keys():
            if task.host.data.get('connexion', NOT_SET) == 'ssh' or task.host.get('connexion', NOT_SET) == 'ssh':
                use_ssh = True

    if task.host.platform == CUMULUS_PLATEFORM_NAME:
        _cumulus_get_ipv6(task, get_vlan=get_vlan, get_loopback=get_loopback, get_peerlink=get_peerlink, get_vni=get_vni, get_physical=get_physical)

    elif task.host.platform == EXTREME_PLATEFORM_NAME:
        _extreme_vsp_get_ipv6(task, get_vlan=get_vlan, get_loopback=get_loopback, get_peerlink=get_peerlink, get_vni=get_vni, get_physical=get_physical)

    elif task.host.platform in NAPALM_COMPATIBLE_PLATEFORM :
        if use_ssh and NEXUS_PLATEFORM_NAME == task.host.platform:
            _nexus_get_ipv6(task, get_vlan=get_vlan, get_loopback=get_loopback, get_peerlink=get_peerlink, get_vni=get_vni, get_physical=get_physical)

        elif use_ssh and CISCO_IOS_PLATEFORM_NAME == task.host.platform:
            _ios_get_ipv6(task, get_vlan=get_vlan, get_loopback=get_loopback, get_peerlink=get_peerlink, get_vni=get_vni, get_physical=get_physical)

        elif use_ssh and CISCO_IOSXR_PLATEFORM_NAME == task.host.platform:
            _iosxr_get_ipv6(task, get_vlan=get_vlan, get_loopback=get_loopback, get_peerlink=get_peerlink, get_vni=get_vni, get_physical=get_physical)

        elif use_ssh and ARISTA_PLATEFORM_NAME == task.host.platform:
            _arista_get_ipv6(task, get_vlan=get_vlan, get_loopback=get_loopback, get_peerlink=get_peerlink, get_vni=get_vni, get_physical=get_physical)
        
        elif use_ssh and JUNOS_PLATEFORM_NAME == task.host.platform:
            _juniper_get_ipv6(task, get_vlan=get_vlan, get_loopback=get_loopback, get_peerlink=get_peerlink, get_vni=get_vni, get_physical=get_physical)

        else:
            _generic_ipv6_napalm(task,
                                 get_vlan=get_vlan,
                                 get_loopback=get_loopback,
                                 get_peerlink=get_peerlink,
                                 get_vni=get_vni,
                                 get_physical=get_physical
            )

    else:
        # RAISE EXCEPTIONS
        print(f"{HEADER_GET} No plateform selected for {task.host.name}...")

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic ipv6 Napalm
#
def _generic_ipv6_napalm(task, *, get_vlan=True, get_loopback=True, get_peerlink=True, get_vni=False, get_physical=True):
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus Networks
#
def _cumulus_get_ipv6(task, *, get_vlan=True, get_loopback=True, get_peerlink=True, get_vni=False, get_physical=True):

    output = task.run(
        name=f"{CUMULUS_GET_IPV6}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_IPV6
    )
    # print_result(output)

    ipv6_addresses = _cumulus_ipv6_converter(
        hostname=task.host.name,
        plateform=task.host.platform,
        cmd_output=json.loads(output.result),
        get_vlan=get_vlan,
        get_loopback=get_loopback,
        get_peerlink=get_peerlink,
        get_vni=get_vni,
        get_physical=get_physical
    )

    task.host[IPV6_DATA_HOST_KEY] = ipv6_addresses

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus (NXOS)
#
def _nexus_get_ipv6(task, *, get_vlan=True, get_loopback=True, get_peerlink=True, get_vni=False, get_physical=True):
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS
#
def _ios_get_ipv6(task, *, get_vlan=True, get_loopback=True, get_peerlink=True, get_vni=False, get_physical=True):
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOSXR
#
def _iosxr_get_ipv6(task, *, get_vlan=True, get_loopback=True, get_peerlink=True, get_vni=False, get_physical=True):
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista vEOS
#
def _arista_get_ipv6(task, *, get_vlan=True, get_loopback=True, get_peerlink=True, get_vni=False, get_physical=True):
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper Networks
#
def _juniper_get_ipv6(task, *, get_vlan=True, get_loopback=True, get_peerlink=True, get_vni=False, get_physical=True):
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Networks
#
def _extreme_vsp_get_ipv6(task, *, get_vlan=True, get_loopback=True, get_peerlink=True, get_vni=False, get_physical=True):
    pass
    
# ----------------------------------------------------------------------------------------------------------------------
#
# Next Device
#