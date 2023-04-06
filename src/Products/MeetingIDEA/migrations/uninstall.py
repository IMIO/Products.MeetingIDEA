# -*- coding: utf-8 -*-
import copy

from DateTime import DateTime
from Products.MeetingIDEA.config import IDEA_ITEM_WF_VALIDATION_LEVELS
from plone import api
from Products.PloneMeeting.migrations import Migrator
import logging

logger = logging.getLogger('MeetingIDEA')


class Migrate_To_MC(Migrator):

    def _adaptWFHistoryForItemsAndMeetings(self):
        """We use PM default WFs, no more meeting(item)_workflow..."""
        logger.info('Updating WF history items and meetings to use new WF id...')
        catalog = api.portal.get_tool('portal_catalog')
        wtool = api.portal.get_tool('portal_workflow')
        for cfg in self.tool.objectValues('MeetingConfig'):
            # this will call especially part where we duplicate WF and apply WFAdaptations
            cfg.registerPortalTypes()
            for brain in catalog(portal_type=(cfg.getItemTypeName(), cfg.getMeetingTypeName())):
                itemOrMeeting = brain.getObject()
                itemOrMeetingWFId = self.wfTool.getWorkflowsFor(itemOrMeeting)[0].getId()
                history = copy.deepcopy(itemOrMeeting.workflow_history[itemOrMeetingWFId])
                for action in history:
                    if "action" in action:
                        if action["action"] == "proposeToDepartmentHead":
                            action["action"] = "proposeToValidationLevel1"
                        if action["action"] == "proposeToDirector":
                            action["action"] = "proposeToValidationLevel2"
                    if "review_state" in action:
                        if action["review_state"] == "proposed_to_departmenthead":
                            action["review_state"] = "proposedToValidationLevel1"
                        if action["review_state"] == "proposed_to_director":
                            action["review_state"] = "proposedToValidationLevel2"
                # do this so change is persisted
                itemOrMeeting.workflow_history[itemOrMeetingWFId] = history
                itemOrMeeting.reindexObjectSecurity()
        logger.info('Done.')

    def run(self,
            profile_name=u'profile-Products.MeetingIDEA:default',
            extra_omitted=[]):
        self._adaptWFHistoryForItemsAndMeetings()
        logger.info('Done migrating to MeetingCommunes...')


# The migration function -------------------------------------------------------
def migrate(context):
    '''This migration function:

       1) Change MeetingConfig workflows to use meeting_workflow/meetingitem_workflow;
       2) Call PloneMeeting migration to 4200 and 4201;
       3) In _after_reinstall hook, adapt items and meetings workflow_history
          to reflect new defined workflow done in 1);
    '''
    migrator = Migrate_To_MC(context)
    migrator.run()
    migrator.finish()
