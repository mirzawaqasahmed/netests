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
ERROR_HEADER = "Error import [bgp_converters.py]"
HEADER_GET = "[netests - bgp_converters]"

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
    from protocols.bgp import BGPSession, ListBGPSessions, BGPSessionsVRF, ListBGPSessionsVRF, BGP
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.bgp")
    exit(EXIT_FAILURE)
    print(importError)

try:
    import json
except ImportError as importError:
    print(f"{ERROR_HEADER} json")
    exit(EXIT_FAILURE)
    print(importError)

########################################################################################################################
#
# Functions
#

# ----------------------------------------------------------------------------------------------------------------------
#
# NAPALM BGP sessions state converter
#
def _napalm_bgp_status_converter(status:str) -> str:
    """
    This function is used to standardize BGP sessions state.
    Napalm use is_up=True and is_enable=True to simplify BGP state.
    In this project we use "UP/DOWN".

    'is_enabled': True,
    'is_up': True,

    :param status:
    :return str: Standard name of BGP state
    """
    if str(status).upper() == "TRUE":
        return "UP"
    elif str(status).upper() == "FALSE":
        return "DOWN"
    else:
        return status

# ----------------------------------------------------------------------------------------------------------------------
#
# NAPALM global vrf converter
#
def _napalm_bgp_vrf_converter(vrf_name:str) -> str:
    """
    This function is used to standardize Global routing table name (vrf_name).
    Napalm named this routing table "global". Other word is "global", "grt" or "default".
    In this project we use "default".

    :param vrf_name:
    :return str: Global/Default routing table name
    """

    if str(vrf_name).upper() == "GLOBAL" or str(vrf_name).upper() == "GRT":
        return "default"
    else:
        return vrf_name

# ----------------------------------------------------------------------------------------------------------------------
#
# NAPALM BGP converter
#
def _napalm_bgp_converter(hostname:str(), cmd_output:json) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(list())
    local_as = ""

    if 'get_bgp_neighbors' in cmd_output.keys():

        for vrf_name, vrf_facts in cmd_output.get('get_bgp_neighbors').items():

            bgp_sessions_lst = ListBGPSessions(list())

            for peer_ip, facts in vrf_facts.get('peers').items():

                bgp_obj = BGPSession(
                    src_hostname=hostname,
                    peer_ip=peer_ip,
                    peer_hostname=facts.get('hostname', NOT_SET),
                    remote_as=facts.get('remote_as', NOT_SET),
                    state_brief=_napalm_bgp_status_converter(facts.get('is_up', NOT_SET)),
                    session_state=facts.get('session_state', NOT_SET),
                    state_time=facts.get('uptime', NOT_SET),
                    prefix_received=facts.get('address_family').get('ipv4').get('received_prefixes')
                )

                local_as = facts.get('local_as', NOT_SET)

                bgp_sessions_lst.bgp_sessions.append(bgp_obj)

            bgp_session_vrf = BGPSessionsVRF(
                vrf_name=_napalm_bgp_vrf_converter(vrf_name),
                as_number=local_as,
                router_id=vrf_facts.get('router_id'),
                bgp_sessions=bgp_sessions_lst
            )

            bgp_sessions_vrf_lst.bgp_sessions_vrf.append(bgp_session_vrf)

    return BGP(
        hostname=hostname,
        bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
    )

# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus BGP converter
#
def _cumulus_bgp_converter(hostname:str(), cmd_outputs:list) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(list())
    as_number = ""
    router_id = ""
    vrf_name = ""
    state_brief = ""

    for cmd_output in cmd_outputs:
        if "ipv4 unicast" in cmd_output.keys():
            if cmd_output.get('ipv4 unicast', NOT_SET) is NOT_SET:
                return None

            else:

                bgp_sessions_lst = ListBGPSessions(list())

                if cmd_output.get('ipv4 unicast', NOT_SET).get('vrfName', NOT_SET) == "default":

                    as_number = cmd_output.get('ipv4 unicast', NOT_SET).get('as', NOT_SET)
                    router_id = cmd_output.get('ipv4 unicast', NOT_SET).get('routerId', NOT_SET)
                    vrf_name = cmd_output.get('ipv4 unicast', NOT_SET).get('vrfName', NOT_SET)

                    for peer_ip, facts in cmd_output.get('ipv4 unicast', NOT_SET).get('peers', list()).items() :

                        if facts.get('state', NOT_SET) in BGP_STATE_UP_LIST:
                            state_brief = BGP_STATE_BRIEF_UP
                        else:
                            state_brief = BGP_STATE_BRIEF_DOWN

                        bgp_session = BGPSession(
                            src_hostname=hostname,
                            peer_ip=peer_ip,
                            peer_hostname=facts.get('hostname', NOT_SET),
                            remote_as=facts.get('remoteAs', NOT_SET),
                            state_brief=state_brief,
                            session_state=facts.get('state', NOT_SET),
                            state_time=facts.get('peerUptime', NOT_SET),
                            prefix_received=facts.get('prefixReceivedCount', NOT_SET),
                        )

                        bgp_sessions_lst.bgp_sessions.append(bgp_session)

                else:

                    as_number = cmd_output.get('ipv4 unicast', NOT_SET).get('ipv4Unicast', NOT_SET).get('as', NOT_SET)
                    router_id = cmd_output.get('ipv4 unicast', NOT_SET).get('ipv4Unicast', NOT_SET).get('routerId', NOT_SET)
                    vrf_name = cmd_output.get('ipv4 unicast', NOT_SET).get('ipv4Unicast', NOT_SET).get('vrfName',NOT_SET)

                    for peer_ip, facts in cmd_output.get('ipv4 unicast', NOT_SET).get('ipv4Unicast', NOT_SET).get('peers', list()).items():

                        if facts.get('state', NOT_SET) in BGP_STATE_UP_LIST:
                            state_brief = BGP_STATE_BRIEF_UP
                        else:
                            state_brief = BGP_STATE_BRIEF_DOWN

                        bgp_session = BGPSession(
                            src_hostname=hostname,
                            peer_ip=peer_ip,
                            peer_hostname=facts.get('hostname', NOT_SET),
                            remote_as=facts.get('remoteAs', NOT_SET),
                            state_brief=state_brief,
                            session_state=facts.get('state', NOT_SET),
                            state_time=facts.get('peerUptime', NOT_SET),
                            prefix_received=facts.get('prefixReceivedCount', NOT_SET),
                        )

                        bgp_sessions_lst.bgp_sessions.append(bgp_session)

                bgp_session_vrf = BGPSessionsVRF(
                    vrf_name=vrf_name,
                    as_number=as_number,
                    router_id=router_id,
                    bgp_sessions=bgp_sessions_lst
                )

            bgp_sessions_vrf_lst.bgp_sessions_vrf.append(bgp_session_vrf)

    return BGP(
        hostname=hostname,
        bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
    )

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus BGP Converter
#
def _nexus_bgp_converter(hostname:str(), cmd_outputs:list) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(list())
    state_brief = ""

    for cmd_output in cmd_outputs:

        bgp_sessions_lst = ListBGPSessions(list())

        if isinstance(cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor', NOT_SET).get(
                'ROW_neighbor', NOT_SET), list):
            for neighbor in cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor',
                    NOT_SET).get('ROW_neighbor', NOT_SET):

                if neighbor.get('state', NOT_SET) in BGP_STATE_UP_LIST:
                    state_brief = BGP_STATE_BRIEF_UP
                else:
                    state_brief = BGP_STATE_BRIEF_DOWN

                bgp_session = BGPSession(
                    src_hostname=hostname,
                    peer_ip=neighbor.get('neighbor-id', NOT_SET),
                    peer_hostname=neighbor.get('interfaces', NOT_SET),
                    remote_as=neighbor.get('remoteas', NOT_SET),
                    state_brief=state_brief,
                    session_state=neighbor.get('state', NOT_SET),
                    state_time=neighbor.get('LastUpDn', NOT_SET),
                    prefix_received=neighbor.get('prefixReceived', NOT_SET)
                )

                bgp_sessions_lst.bgp_sessions.append(bgp_session)

        elif isinstance(cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor', NOT_SET).get(
                'ROW_neighbor', NOT_SET), dict):

            if cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor', NOT_SET).get(
                    'ROW_neighbor', NOT_SET).get('state', NOT_SET) in BGP_STATE_UP_LIST:
                state_brief = BGP_STATE_BRIEF_UP
            else:
                state_brief = BGP_STATE_BRIEF_DOWN

            bgp_session = BGPSession(
                src_hostname=hostname,
                peer_ip=cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor',NOT_SET).get('ROW_neighbor',NOT_SET).get('neighbor-id', NOT_SET),
                peer_hostname=cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor',NOT_SET).get('ROW_neighbor', NOT_SET).get('interfaces', NOT_SET),
                remote_as=cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor',NOT_SET).get('ROW_neighbor',NOT_SET).get('remoteas', NOT_SET),
                state_brief=state_brief,
                session_state=cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor',NOT_SET).get('ROW_neighbor', NOT_SET).get('state', NOT_SET),
                state_time=cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor',NOT_SET).get('ROW_neighbor',NOT_SET).get('LastUpDn', NOT_SET),
                prefix_received=cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor',NOT_SET).get('ROW_neighbor', NOT_SET).get('prefixReceived', NOT_SET)
            )

            bgp_sessions_lst.bgp_sessions.append(bgp_session)

        bgp_session_vrf = BGPSessionsVRF(
            vrf_name=cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('vrf-name-out', NOT_SET),
            as_number=cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('local-as', NOT_SET),
            router_id=cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('router-id', NOT_SET),
            bgp_sessions=bgp_sessions_lst
        )

        bgp_sessions_vrf_lst.bgp_sessions_vrf.append(bgp_session_vrf)

    return BGP(
        hostname=hostname,
        bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
    )


# ----------------------------------------------------------------------------------------------------------------------
#
# Arista BGP Converter
#
def _arista_bgp_converter(hostname:str(), cmd_outputs:list) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(list())
    state_brief = ""

    for cmd_output in cmd_outputs:

        bgp_sessions_lst = ListBGPSessions(list())

        temp_value = cmd_output.get('vrfs', NOT_SET).keys()
        for key in temp_value:
            vrf_name = key
            break

        for neighbor, facts in cmd_output.get('vrfs', NOT_SET).get(vrf_name, NOT_SET).get('peers', NOT_SET).items():

            if facts.get('peerState', NOT_SET) in BGP_STATE_UP_LIST:
                state_brief = BGP_STATE_BRIEF_UP
            else:
                state_brief = BGP_STATE_BRIEF_DOWN

            bgp_session = BGPSession(
                src_hostname=hostname,
                peer_ip=neighbor,
                peer_hostname=facts.get('hostname', NOT_SET),
                remote_as=facts.get('asn', NOT_SET),
                state_brief=state_brief,
                session_state=facts.get('peerState', NOT_SET),
                state_time=facts.get('upDownTime', NOT_SET),
                prefix_received=facts.get('prefixReceived', NOT_SET)
            )

            bgp_sessions_lst.bgp_sessions.append(bgp_session)

        bgp_session_vrf = BGPSessionsVRF(
            vrf_name=vrf_name,
            as_number=cmd_output.get('vrfs', NOT_SET).get(vrf_name, NOT_SET).get('asn', NOT_SET),
            router_id=cmd_output.get('vrfs', NOT_SET).get(vrf_name, NOT_SET).get('routerId', NOT_SET),
            bgp_sessions=bgp_sessions_lst
        )

        bgp_sessions_vrf_lst.bgp_sessions_vrf.append(bgp_session_vrf)

    return BGP(
        hostname=hostname,
        bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
    )

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper BGP Converter
#
def _juniper_bgp_converter(hostname:str(), cmd_outputs:list) -> BGP:
    pass
