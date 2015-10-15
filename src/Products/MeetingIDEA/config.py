# -*- coding: utf-8 -*-
#
# File: MeetingIDEA.py
#
# Copyright (c) 2015 by IMIO
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Andre Nuyens <andre.nuyens@imio.be>"""
__docformat__ = 'plaintext'


# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. The items in there
# will be included (by importing) in this file if found.

from Products.CMFCore.permissions import setDefaultRoles
##code-section config-head #fill in your manual code here
from collections import OrderedDict
##/code-section config-head


PROJECTNAME = "MeetingIDEA"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner', 'Contributor'))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

##code-section config-bottom #fill in your manual code here
from Products.PloneMeeting import config as PMconfig
IDEAROLES = {}
IDEAROLES['departmentheads'] = 'MeetingDepartmentHead'
PMconfig.MEETINGROLES.update(IDEAROLES)
PMconfig.MEETING_GROUP_SUFFIXES = PMconfig.MEETINGROLES.keys()

from Products.PloneMeeting.model import adaptations
MIDEA_RETURN_TO_PROPOSING_GROUP_MAPPINGS = {'backTo_presented_from_returned_to_proposing_group':
                                            ['created', ],
                                            'backTo_validated_by_cd_from_returned_to_proposing_group':
                                            ['validated_by_cd', ],
                                            'backTo_itemfrozen_from_returned_to_proposing_group':
                                            ['frozen', 'decided', ],
                                            'NO_MORE_RETURNABLE_STATES': ['closed', 'archived', ], }
adaptations.RETURN_TO_PROPOSING_GROUP_MAPPINGS.update(MIDEA_RETURN_TO_PROPOSING_GROUP_MAPPINGS)

IDEAMEETINGREVIEWERS = OrderedDict([('reviewers',  'proposed_to_director'),
                                    ('departmentheads', 'proposed_to_departmenthead'), ])
PMconfig.MEETINGREVIEWERS = IDEAMEETINGREVIEWERS
##/code-section config-bottom


# Load custom configuration not managed by archgenxml
try:
    from Products.MeetingIDEA.AppConfig import *
except ImportError:
    pass
