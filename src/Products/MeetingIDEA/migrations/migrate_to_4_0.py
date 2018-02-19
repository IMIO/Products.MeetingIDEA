# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger('MeetingIDEA')

from plone import api
from Products.PloneMeeting.migrations.migrate_to_4_0 import Migrate_To_4_0 as PMMigrate_To_4_0


# The migration class ----------------------------------------------------------
class Migrate_To_4_0(PMMigrate_To_4_0):
    wfs_to_delete = []

    def _cleanCDLD(self):
        """We removed things related to 'CDLD' finance advice, so:
           - remove the 'cdld-document-generate' from document_actions;
           - remove the MeetingConfig.CdldProposingGroup attribute.
        """
        logger.info('Removing CDLD related things...')
        doc_actions = self.portal.portal_actions.document_actions
        # remove the action from document_actions
        if 'cdld-document-generate' in doc_actions:
            doc_actions.manage_delObjects(ids=['cdld-document-generate', ])
        # clean the MeetingConfigs
        for cfg in self.tool.objectValues('MeetingConfig'):
            if hasattr(cfg, 'cdldProposingGroup'):
                delattr(cfg, 'cdldProposingGroup')
        logger.info('Done.')

    def _migrateItemPositiveDecidedStates(self):
        """Before, the states in which an item was auto sent to
           selected other meetingConfig was defined in a method
           'itemPositiveDecidedStates' now it is stored in MeetingConfig.itemAutoSentToOtherMCStates.
           We store these states in the MeetingConfig.itemPositiveDecidedStates, it is used
           to display the 'sent from' leading icon on items sent from another MeetingConfig."""
        logger.info('Defining values for MeetingConfig.itemAutoSentToOtherMCStates...')
        for cfg in self.tool.objectValues('MeetingConfig'):
            cfg.setItemAutoSentToOtherMCStates(('accepted', 'accepted_but_modified',))
            cfg.setItemPositiveDecidedStates(('accepted', 'accepted_but_modified',))
        logger.info('Done.')

    def _after_reinstall(self):
        """Use that hook that is called just after the profile has been reinstalled by
           PloneMeeting, this way, we may launch some steps before PloneMeeting ones.
           Here we will update used workflows before letting PM do his job."""
        logger.info('Replacing old no more existing workflows...')
        PMMigrate_To_4_0._after_reinstall(self)
        # delete old unused workflows, aka every workflows containing 'college' or 'council'
        self.wfs_to_delete = []
        logger.info('Done.')

    def _deleteUselessWorkflows(self):
        """Finally, remove useless workflows."""
        logger.info('Removing useless workflows...')
        if self.wfs_to_delete:
            wfTool = api.portal.get_tool('portal_workflow')
            wfTool.manage_delObjects(self.wfs_to_delete)
        logger.info('Done.')

    def _updateConfig(self):
        logger.info('Updating specific config for IDEA...')

        for cfg in self.tool.objectValues('MeetingConfig'):
            # item
            cfg.setUsedItemAttributes((
                'detailedDescription', 'budgetInfos', 'observations', 'toDiscuss', 'itemAssembly',
                'internalCommunication', 'strategicAxis',))
            # meeting
            cfg.setUsedMeetingAttributes(('startDate', 'endDate', 'signatures', 'assembly', 'assemblyExcused',
                                          'assemblyAbsents', 'assemblyProxies', 'observations',))
            # dashboard list items
            cfg.setItemColumns('Creator', 'ModificationDate', 'review_state', 'proposing_group_acronym', 'advices',
                                'toDiscuss', 'linkedMeetingDate', 'getPreferredMeetingDate', 'actions')
            # dashboard list available items for meeting
            cfg.setAvailableItemsListVisibleColumns('Creator', 'ModificationDate', 'review_state',
                                                    'proposing_group_acronym', 'advices',
                                                    'toDiscuss', 'linkedMeetingDate', 'getPreferredMeetingDate',
                                                    'actions')
            cfg.setMaxShownAvailableItems('20')
            # dashboard list presented items in meeting
            cfg.itemsListVisibleColumns('item_reference', 'Creator', 'ModificationDate', 'review_state',
                                        'proposing_group_acronym', 'advices',
                                        'toDiscuss', 'actions')
            cfg.setMaxShownMeetingItems('40')

    def _migrateAssemblies(self):
        logger.info('Updating meeting assemblies for IDEA...')

        brains = self.portal.portal_catalog(meta_type='Meeting')

        for brain in brains:
            meeting = brain.getObject()

            meeting.setAssemblyExcused('<p>' + self._getAssemblyPart(meeting.getAssembly(), 'absentee') + '</p>')
            meeting.setAssemblyAbsents('<p>' + self._getAssemblyPart(meeting.getAssembly(), 'procuration') + '</p>')
            meeting.setAssemblyProxies('<p>' + self._getAssemblyPart(meeting.getAssembly(), 'excused') + '</p>')
            meeting.setAssembly('<p>' + self._getAssemblyPart(meeting.getAssembly(), 'present') + '</p>')

    def _getAssemblyPart(self, assembly, filter=''):
        # suppress paragraph
        assembly = assembly.replace('<p>', '').replace('</p>', '')
        assembly = assembly.split('<br />')
        res = []
        status = 'present'
        for ass in assembly:
            # ass line "Excusé:" is used for define list of persons who are excused
            if ass.find('xcus') >= 0:
                status = 'excused'
                continue
            # ass line "Procurations:" is used for defined list of persons who recieve a procuration
            if ass.upper().find('PROCURATION') >= 0:
                status = 'procuration'
                continue
            # ass line "Absents:" is used for define list of persons who are excused
            if ass.upper().find('ABSENT') >= 0:
                status = 'absentee'
                continue
            if filter == '*' or status == filter:
                res.append(ass)
        return "".join(res)

    def run(self, step=None):
        # change self.profile_name that is reinstalled at the beginning of the PM migration
        self.profile_name = u'profile-Products.MeetingIDEA:default'

        # call steps from Products.PloneMeeting
        PMMigrate_To_4_0.run(self, step=step)

        if step == 3:
            # now MeetingIDEA specific steps
            logger.info('Migrating to MeetingIDEA 4.0...')
            self._cleanCDLD()
            self._migrateItemPositiveDecidedStates()
            # self._addSampleAnnexTypeForMeetings()
            self._deleteUselessWorkflows()
            self._updateConfig()
            self._migrateAssemblies()

# The migration function -------------------------------------------------------
def migrate(context):
    '''This migration function:

       1) Reinstall Products.MeetingIDEA and execute the Products.PloneMeeting migration;
       2) Clean CDLD attributes;
       3) Add an annex type for Meetings;
       4) Remove useless workflows;
       5) Migrate positive decided states.
    '''
    migrator = Migrate_To_4_0(context)
    migrator.run()
    migrator.finish()


def migrate_step1(context):
    '''This migration function:

       1) Reinstall Products.MeetingIDEA and execute the Products.PloneMeeting migration.
    '''
    migrator = Migrate_To_4_0(context)
    migrator.run(step=1)
    migrator.finish()


def migrate_step2(context):
    '''This migration function:

       1) Execute step2 of Products.PloneMeeting migration profile (imio.annex).
    '''
    migrator = Migrate_To_4_0(context)
    migrator.run(step=2)
    migrator.finish()


def migrate_step3(context):
    '''This migration function:

       1) Execute step3 of Products.PloneMeeting migration profile.
       2) Clean CDLD attributes;
       3) Add an annex type for Meetings;
       4) Remove useless workflows;
       5) Migrate positive decided states.
    '''
    migrator = Migrate_To_4_0(context)
    migrator.run(step=3)
    migrator.finish()
