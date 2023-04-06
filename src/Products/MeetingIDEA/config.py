# -*- coding: utf-8 -*-
#
# File: config.py
#
# Copyright (c) 2016 by Imio.be
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Andre Nuyens <andre.nuyens@imio.be>"""
__docformat__ = "plaintext"


# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. The items in there
# will be included (by importing) in this file if found.

from Products.CMFCore.permissions import setDefaultRoles
from collections import OrderedDict

PROJECTNAME = "MeetingIDEA"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ("Manager", "Owner", "Contributor"))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

from Products.PloneMeeting import config as PMconfig

PMconfig.EXTRA_GROUP_SUFFIXES = [
    {
        "fct_title": u"departmentheads",
        "fct_id": u"departmentheads",
        "fct_orgs": [],
        "fct_management": False,
        "enabled": True,
    },
]


IDEA_ITEM_WF_VALIDATION_LEVELS = (
    {
        "state": "itemcreated",
        "state_title": "itemcreated",
        "leading_transition": "-",
        "leading_transition_title": "-",
        "back_transition": "backToItemCreated",
        "back_transition_title": "backToItemCreated",
        "suffix": "creators",
        # only creators may manage itemcreated item
        "extra_suffixes": [],
        "enabled": "1",
    },
    {
        "state": "proposedToValidationLevel1",
        "state_title": "Proposé au chef de service",
        "leading_transition": "proposeToValidationLevel1",
        "leading_transition_title": "Proposer au chef de service",
        "back_transition": "backToProposedToValidationLevel1",
        "back_transition_title": "Renvoyer au chef de Service",
        "suffix": "departmentheads",
        "extra_suffixes": [],
        "enabled": "1",
    },
    {
        "state": " proposedToValidationLevel2",
        "state_title": "Proposé au directeur",
        "leading_transition": "proposeToValidationLevel2",
        "leading_transition_title": "Proposer au directeur",
        "back_transition": "backToProposedToValidationLevel2",
        "back_transition_title": "Renvoyer au directeur",
        "suffix": "reviewers",
        "enabled": "1",
        "extra_suffixes": [],
    }
)

# import at the bottom so monkeypatches are done because PMconfig is imported in MCconfig
from Products.MeetingCommunes import config as MCconfig
