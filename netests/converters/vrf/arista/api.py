#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.constants import NOT_SET
from netests.protocols.vrf import VRF, ListVRF


def _arista_vrf_api_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> ListVRF:

    if not isinstance(cmd_output['result'][0], dict):
        cmd_output = json.loads(cmd_output['result'][0])
    else:
        cmd_output = cmd_output['result'][0]

    vrf_list = ListVRF(list())
    for vrf_name, facts in cmd_output.get('vrfs').items():
        if (
            facts.get('routeDistinguisher', NOT_SET) == NOT_SET or
            facts.get('routeDistinguisher', NOT_SET) == ''
        ):
            rd = NOT_SET
        else:
            rd = facts.get('routeDistinguisher', NOT_SET)

        vrf_list.vrf_lst.append(
            VRF(
                vrf_name=vrf_name,
                vrf_id=NOT_SET,
                vrf_type=NOT_SET,
                l3_vni=NOT_SET,
                rd=rd,
                rt_imp=NOT_SET,
                rt_exp=NOT_SET,
                imp_targ=NOT_SET,
                exp_targ=NOT_SET,
                options=options
            )
        )

    return vrf_list
