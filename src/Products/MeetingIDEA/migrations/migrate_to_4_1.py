
# -*- coding: utf-8 -*-

from Products.GenericSetup.tool import DEPENDENCY_STRATEGY_NEW
from Products.MeetingCommunes.migrations.migrate_to_4_1 import Migrate_To_4_1 as MCMigrate_To_4_1

import logging

from plone import api

logger = logging.getLogger('MeetingIDEA')


class Migrate_To_4_1(MCMigrate_To_4_1):

    def run(self):
        self._migrateInternalCommunicationAttribute()
        # reapply the actions.xml of collective.iconifiedcategory
        self.ps.runImportStepFromProfile('profile-collective.iconifiedcategory:default', 'actions')
        super(Migrate_To_4_1, self).run(extra_omitted=['Products.MeetingIDEA:default'])
        self.reinstall(profiles=[u'profile-Products.MeetingIDEA:default'],
                       ignore_dependencies=True,
                       dependency_strategy=DEPENDENCY_STRATEGY_NEW)

    def _migrateInternalCommunicationAttribute(self):
        '''Field MeetingConfig.itemGroupInChargeStates was renamed to MeetingConfig.itemGroupsInChargeStates.
           Value reader_groupincharge is now reader_groupsincharge.'''
        logger.info('Adapting meetingConfigs...')
        for cfg in self.tool.objectValues('MeetingConfig'):
            usedItemAttrs = list(cfg.getUsedItemAttributes())
            if 'meetingManagersNotes' not in usedItemAttrs:
                usedItemAttrs.append('meetingManagersNotes')
            cfg.setUsedItemAttributes(usedItemAttrs)
        logger.info('Adapting items...')
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(meta_type=['MeetingItem'])
        for brain in brains:
            item = brain.getObject()
            if hasattr(item, 'internalCommunication'):
                item.setMeetingManagersNotes(item.internalCommunication)
                delattr(item, 'internalCommunication')



def migrate(context):
    '''This migration will:
       1) Execute Products.MeetingCommunes migration.
    '''
    migrator = Migrate_To_4_1(context)
    migrator.run()
    migrator.finish()