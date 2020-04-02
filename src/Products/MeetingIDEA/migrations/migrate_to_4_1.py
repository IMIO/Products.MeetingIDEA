# -*- coding: utf-8 -*-

from copy import deepcopy
from Products.MeetingCommunes.profiles.examples_fr.import_data import collegeMeeting
from Products.MeetingCommunes.profiles.examples_fr.import_data import data
from Products.PloneMeeting.migrations.migrate_to_4_1 import (
    Migrate_To_4_1 as PMMigrate_To_4_1,
)
from Products.PloneMeeting.migrations.migrate_to_4100 import Migrate_To_4100
from Products.PloneMeeting.migrations.migrate_to_4101 import Migrate_To_4101
from Products.PloneMeeting.migrations.migrate_to_4102 import Migrate_To_4102
from Products.PloneMeeting.migrations.migrate_to_4103 import Migrate_To_4103
from Products.PloneMeeting.migrations.migrate_to_4104 import Migrate_To_4104

import logging

from plone import api

logger = logging.getLogger("MeetingIDEA")


class Migrate_To_4_1(PMMigrate_To_4_1):
    def _defineDirectoryPositionTypes(self):
        """Set default value for contacts directoryy 'position_types'."""
        logger.info("Setting default value for contact.position_types...")
        position_types = self.portal.contacts.position_types
        if len(position_types) == 1 and position_types[0]["token"] == "default":
            self.portal.contacts.position_types = data.directory_position_types
        logger.info("Done.")

    def _defaultFTWLabels(self):
        """Return default FTW Labels, called by _initPersonalFTWLabels."""
        return deepcopy(collegeMeeting.defaultLabels)

    def _migrateInternalCommunicationAttribute(self):
        """Field MeetingConfig.itemGroupInChargeStates was renamed to MeetingConfig.itemGroupsInChargeStates.
           Value reader_groupincharge is now reader_groupsincharge."""
        logger.info("Adapting meetingConfigs...")
        for cfg in self.tool.objectValues("MeetingConfig"):
            usedItemAttrs = list(cfg.getUsedItemAttributes())
            if "meetingManagersNotes" not in usedItemAttrs:
                usedItemAttrs.append("meetingManagersNotes")
            cfg.setUsedItemAttributes(usedItemAttrs)
        logger.info("Adapting items...")
        catalog = api.portal.get_tool("portal_catalog")
        brains = catalog(meta_type=["MeetingItem"])
        for brain in brains:
            item = brain.getObject()
            if hasattr(item, "internalCommunication"):
                item.setMeetingManagersNotes(item.internalCommunication)
                delattr(item, "internalCommunication")

    def run(
        self, profile_name=u"profile-Products.MeetingCommunes:default", extra_omitted=[]
    ):
        # change self.profile_name that is reinstalled at the beginning of the PM migration
        self.profile_name = profile_name

        # call steps from Products.PloneMeeting
        super(Migrate_To_4_1, self).run(extra_omitted=extra_omitted)

        # execute upgrade steps in PM that were added after main upgrade to 4.1
        Migrate_To_4100(self.portal).run()
        Migrate_To_4101(self.portal).run(from_migration_to_41=True)
        Migrate_To_4102(self.portal).run()
        Migrate_To_4103(self.portal).run()
        Migrate_To_4104(self.portal).run()

        # now MeetingCommunes specific steps
        logger.info("Migrating to MeetingCommunes 4.1...")
        self._defineDirectoryPositionTypes()

        # now MeetingIDEA specific steps
        logger.info("Migrating to MeetingIDEA 4.1...")
        self._migrateInternalCommunicationAttribute()


# The migration function -------------------------------------------------------
def migrate(context):
    """This migration function:

       1) Reinstall Products.MeetingCommunes and execute the Products.PloneMeeting migration;
       2) Define default values for 'contacts' directory.position_types;
       3) Define default ftw.labels labels.
    """
    migrator = Migrate_To_4_1(context)
    migrator.run()
    migrator.finish()
