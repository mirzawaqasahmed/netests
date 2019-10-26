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
# Default value used for exit()
#
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

########################################################################################################################
#
# CONSTANTES
#

###### NORNIR INIT ######
NORNIR_DEBUG_MODE = 'debug'

PATH_TO_VERITY_FILES = "./verity/"
PATH_TO_INVENTORY_FILES = "./inventory/"

###### INVENTORY ######
ANSIBLE_INVENTORY = "hosts"
ANSIBLE_INVENTORY_VIRTUAL = "hosts"

JUNOS_PLATEFORM_NAME = 'junos'
CUMULUS_PLATEFORM_NAME = 'linux'
NEXUS_PLATEFORM_NAME = 'cisco_nxos'
CISCO_PLATEFORM_NAME = 'cisco_ios'
ARISTA_PLATEFORM_NAME = 'arista_eos'

###### TESTS TO EXECUTE FILE ######
TEST_TO_EXECUTE_FILENAME = "_test_to_execute.yml"
TO_EXECUTE_FILE_VALUE = ['INFO', 'TRUE', 'FALSE']
BGP_SRC_FILENAME = "bgp.yml"
TEST_TO_EXC_BGP_KEY = 'bgp'


###### CUMULUS COMMANDS
CUMULUS_GET_BGP = 'net show bgp summary'
