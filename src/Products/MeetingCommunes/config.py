# -*- coding: utf-8 -*-
#
# File: MeetingCommunes.py
#
# Copyright (c) 2013 by CommunesPlone
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier Bastien <g.bastien@imio.be>, Stephan Geulette <s.geulette@imio.be>"""
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
##/code-section config-head


PROJECTNAME = "MeetingCommunes"

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
# Define PloneMeeting-specific permissions
AddAnnex = 'PloneMeeting: Add annex'
setDefaultRoles(AddAnnex, ('Manager', 'Owner'))
# We need 'AddAnnex', which is a more specific permission than
# 'PloneMeeting: Add MeetingFile', because decision-related annexes, which are
# also MeetingFile instances, must be secured differently.
# There is no permission linked to annex deletion. Deletion of annexes is allowed
# if one has the permission 'Modify portal content' on the corresponding item.
ReadDecision = 'PloneMeeting: Read decision'
WriteDecision = 'PloneMeeting: Write decision'
setDefaultRoles(ReadDecision, ('Manager',))
setDefaultRoles(WriteDecision, ('Manager',))

STYLESHEETS = [{'id': 'meetingcommunes.css',
                'title': 'MeetingCommunes CSS styles'}]

# define some more value in MeetingConfig.topicsInfo so extra topics are created for each MeetingConfig
from Products.PloneMeeting.MeetingConfig import MeetingConfig
topicsInfo = (
    # Items in state 'proposed'
    ('searchproposeditems',
    (('Type', 'ATPortalTypeCriterion', 'MeetingItem'),),
     'created',
     '',
     "python: not here.portal_plonemeeting.userIsAmong('reviewers')",
     ('proposed', ),
     ),
    # Items that need to be validated
    ('searchitemstovalidate',
    (('Type', 'ATPortalTypeCriterion', 'MeetingItem'),),
     'created',
     'searchItemsToValidate',
     "python: here.portal_plonemeeting.userIsAmong('reviewers')",
     ('proposed', ),
     ),
    # Items in state 'validated'
    ('searchvalidateditems',
    (('Type', 'ATPortalTypeCriterion', 'MeetingItem'),),
     'created',
     '',
     '',
     ('validated', ),
     ),
    # All 'decided' items
    ('searchdecideditems',
    (('Type', 'ATPortalTypeCriterion', 'MeetingItem'),),
     'created',
     '',
     '',
     ('accepted', 'refused', 'delayed', 'accepted_but_modified',),
     ),
)
existingTopicsInfo = MeetingConfig.topicsInfo
existingTopicsInfo = list(existingTopicsInfo)
existingTopicsInfo.extend(topicsInfo)
MeetingConfig.topicsInfo = tuple(existingTopicsInfo)

# override states mappings for the 'return_to_proposing_group' wfAdaptation
##code-section config-bottom #fill in your manual code here
from Products.PloneMeeting import config as PMconfig
MC_RETURN_TO_PROPOSING_GROUP_MAPPINGS = {'backTo_presented_from_returned_to_proposing_group':
                                         ['created', ],
                                         'backTo_itempublished_from_returned_to_proposing_group':
                                         ['published', ],
                                         'backTo_itemfrozen_from_returned_to_proposing_group':
                                         ['frozen', 'decided', 'decisions_published', ],
                                         'NO_MORE_RETURNABLE_STATES': ['closed', 'archived', ], }
PMconfig.RETURN_TO_PROPOSING_GROUP_MAPPINGS.update(MC_RETURN_TO_PROPOSING_GROUP_MAPPINGS)
##/code-section config-bottom


# Load custom configuration not managed by archgenxml
try:
    from Products.MeetingCommunes.AppConfig import *
except ImportError:
    pass
