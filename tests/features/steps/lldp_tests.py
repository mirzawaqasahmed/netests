#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from behave import given, when, then
from protocols.lldp import LLDP, ListLLDP
from functions.global_tools import printline
from functions.lldp.lldp_compare import _compare_lldp
from functions.global_tools import open_json_file, open_txt_file
from functions.lldp.arista.api.converter import _arista_lldp_api_converter
from functions.lldp.arista.ssh.converter import _arista_lldp_ssh_converter
from functions.lldp.extreme_vsp.api.converter import (
    _extreme_vsp_lldp_api_converter
)
from functions.lldp.extreme_vsp.ssh.converter import (
    _extreme_vsp_lldp_ssh_converter
)
from const.constants import NOT_SET, FEATURES_SRC_PATH, LLDP_DATA_HOST_KEY


@given(u'A network protocols named LLDP defined in protocols/lldp.py')
def step_impl(context):
    context.test_not_implemented = list()


@given(u'I create a LLDP object equals to Arista manually named o0001')
def step_impl(context):
    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    lldp_neighbors_lst.lldp_neighbors_lst.append(
        LLDP(
            local_name="leaf03",
            local_port="Ethernet2",
            neighbor_port="1/2",
            neighbor_name="spine02",
            neighbor_os="VSP-8284XSQ (8.1.0.0)",
            neighbor_mgmt_ip="192.168.1.202",
            neighbor_type=['Bridge', 'Router']
        )
    )

    lldp_neighbors_lst.lldp_neighbors_lst.append(
        LLDP(
            local_name="leaf03",
            local_port="Ethernet1",
            neighbor_port="swp1",
            neighbor_name="cumulus",
            neighbor_os="Cumulus Linux version 4.0.0 running on QEMU Standard PC(i440FX + PIIX, 1996)",
            neighbor_mgmt_ip="192.168.1.148",
            neighbor_type=['Bridge', 'Router']
        )
    )

    context.o0001 = lldp_neighbors_lst



@given(u'I create a LLDP object from a Arista API output named o0002')
def step_impl(context):
    context.o0002 = _arista_lldp_api_converter(
        hostname="leaf03",
        cmd_output=open_json_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/lldp/arista/api/"
                "arista_api_show_lldp_neighbors.json"
            )
        ),
        options={}
    )


@given(u'I create a LLDP object from a Arista Netconf named o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object from a Arista SSH output named o0004')
def step_impl(context):
    context.o0004 = _arista_lldp_ssh_converter(
        hostname="leaf03",
        cmd_output=open_json_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/lldp/arista/ssh/"
                "arista_cli_show_lldp_neighbors.json"
            )
        ),
        options={}
    )


@given(u'I create a LLDP object equals to Cumulus manually named o0101')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object from a Cumulus API output named o0102')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object from a Cumulus Netconf named o0103')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object from a Cumulus SSH output named o0104')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object equals to Extreme VSP manually named o0201')
def step_impl(context):
    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    lldp_neighbors_lst.lldp_neighbors_lst.append(
        LLDP(
            local_name="spine02",
            local_port="1/2",
            neighbor_port="Ethernet2",
            neighbor_name="leaf03.dh.local",
            neighbor_os="",
            neighbor_mgmt_ip="192.168.1.199",
            neighbor_type=['Bridge', 'Router']
        )
    )

    context.o0201 = lldp_neighbors_lst


@given(u'I create a LLDP object from a Extreme VSP API output named o0202')
def step_impl(context):
    context.o0202 = _extreme_vsp_lldp_api_converter(
        hostname="spine02",
        cmd_output=open_json_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/lldp/extreme_vsp/api/"
                "extreme_vsp_api_get_lldp_neighbors.json"
            )
        ),
        options={}
    )


@given(u'I create a LLDP object from a Extreme VSP Netconf output named o0203')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object from a Extreme VSP SSH output named o0204')
def step_impl(context):
    context.o0204 = _extreme_vsp_lldp_ssh_converter(
        hostname="spine02",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/lldp/extreme_vsp/ssh/"
                "extreme_vsp_show_lldp_neighbors.txt"
            )
        ),
        options={}
    )



@given(u'I create a LLDP object equals to IOS manually named o0301')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object from a IOS API output named o0302')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object from a IOS Netconf named o0303')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object from a IOS SSH named o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object equals to IOS-XR manually named o0401')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object from a IOS-XR API output named o0402')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object from a IOS-XR Netconf output named o403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object from a IOS-XR SSH output named o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object equals IOS-XR multi manually output named o0405')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object from a IOS-XR multi Netconf output named o0406')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object equals to Juniper manually named o0501')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object from a Juniper API output named o0502')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object from a Juniper Netconf output named o0503')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object from a Juniper SSH output named o0504')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object equals to NAPALM manually named o0601')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object from a NAPALM output named o0602')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object equals to NXOS manually named o0701')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object from a NXOS API output named o0702')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object from a NXOS Netconf output named o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a LLDP object from a NXOS SSH output named o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0001 should be equal to o0002')
def step_impl(context):
    assert context.o0001 == context.o0002


@given(u'LLDP o0001 should be equal to o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0001 should be equal to o0004')
def step_impl(context):
    assert context.o0001 == context.o0004


@given(u'LLDP o0002 should be equal to o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0002 should be equal to o0004')
def step_impl(context):
    assert context.o0002 == context.o0004


@given(u'LLDP o0003 should be equal to o0004')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP YAML file should be equal to o0002')
def step_impl(context):
    assert _compare_lldp(
        host_keys=LLDP_DATA_HOST_KEY,
        hostname="leaf03",
        groups=['eos'],
        lldp_host_data=context.o0002,
        test=True
    )


@given(u'LLDP YAML file should be equal to o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP YAML file should be equal to o0004')
def step_impl(context):
    assert _compare_lldp(
        host_keys=LLDP_DATA_HOST_KEY,
        hostname="leaf03",
        groups=['eos'],
        lldp_host_data=context.o0004,
        test=True
    )


@given(u'LLDP o0101 should be equal to o0102')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0101 should be equal to o0103')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0101 should be equal to o0104')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0102 should be equal to o0103')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0102 should be equal to o0104')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0103 should be equal to o0104')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP YAML file should be equal to o0102')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP YAML file should be equal to o0103')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP YAML file should be equal to o0104')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0201 should be equal to o0202')
def step_impl(context):
    assert context.o0201 == context.o0202


@given(u'LLDP o0201 should be equal to o0203')
def step_impl(context):
    print("Extreme VSP VRF with API has no endpoint -> Not tested")


@given(u'LLDP o0201 should be equal to o0204')
def step_impl(context):
    assert context.o0201 == context.o0204


@given(u'LLDP o0202 should be equal to o0203')
def step_impl(context):
    print("Extreme VSP VRF with API has no endpoint -> Not tested")


@given(u'LLDP o0202 should be equal to o0204')
def step_impl(context):
    assert context.o0202 == context.o0204


@given(u'LLDP o0203 should be equal to o0204')
def step_impl(context):
    print("Extreme VSP VRF with API has no endpoint -> Not tested")


@given(u'LLDP YAML file should be equal to o0202')
def step_impl(context):
    assert _compare_lldp(
        host_keys=LLDP_DATA_HOST_KEY,
        hostname="spine02",
        groups=['extreme_vsp'],
        lldp_host_data=context.o0202,
        test=True
    )


@given(u'LLDP YAML file should be equal to o0203')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP YAML file should be equal to o0204')
def step_impl(context):
    assert _compare_lldp(
        host_keys=LLDP_DATA_HOST_KEY,
        hostname="spine02",
        groups=['extreme_vsp'],
        lldp_host_data=context.o0204,
        test=True
    )


@given(u'LLDP o0301 should be equal to o0302')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0301 should be equal to o0303')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0301 should be equal to o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0302 should be equal to o0303')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0302 should be equal to o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0303 should be equal to o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP YAML file should be equal to o0302')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP YAML file should be equal to o0303')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP YAML file should be equal to o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0401 should be equal to o0402')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0401 should be equal to o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0401 should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0402 should be equal to o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0402 should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0403 should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP YAML file should be equal to o0402')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP YAML file should be equal to o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP YAML file should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0501 should be equal to o0502')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0501 should be equal to o0503')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0501 should be equal to o0504')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0502 should be equal to o0503')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0502 should be equal to o0504')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0503 should be equal to o0504')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP YAML file should be equal to o0502')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP YAML file should be equal to o0503')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP YAML file should be equal to o0504')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0601 should be equal to o0602')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0701 should be equal to o0702')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0701 should be equal to o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0701 should be equal to o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0702 should be equal to o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0702 should be equal to o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP o0703 should be equal to o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP YAML file should be equal to o0702')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP YAML file should be equal to o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'LLDP YAML file should be equal to o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I Finish my LLDP tests and list tests not implemented')
def step_impl(context):
    printline()
    print("| The following tests are not implemented :")
    printline()
    for test in context.test_not_implemented:
        print(f"| {test}")
    printline()
