# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('PloneMeeting')

from Acquisition import aq_base

from Products.PloneMeeting.profiles import MeetingFileTypeDescriptor
from Products.PloneMeeting.migrations import Migrator


# The migration class ----------------------------------------------------------
class Migrate_To_3_2_0(Migrator):

    def _addDefaultAdviceAnnexesFileTypes(self):
        '''Add some default MeetingFileType relatedTo 'advice' so we can add
           annexes on advices.'''
        logger.info('Addind default MeetingFileType relatedTo \'advice\'...')
        mfts = []
        mfts.append(MeetingFileTypeDescriptor(id='annexeAvis',
                                              title=u'Annexe à un avis',
                                              theIcon='attach.png',
                                              predefinedTitle='',
                                              relatedTo='advice',
                                              active=True))
        mfts.append(MeetingFileTypeDescriptor(id='annexeAvisLegal',
                                              title=u'Extrait article de loi',
                                              theIcon='legalAdvice.png',
                                              predefinedTitle='',
                                              relatedTo='advice',
                                              active=True))
        # find theIcon path so we can give it to MeetingConfig.addFileType
        mcProfilePath = [profile for profile in self.context.listProfileInfo() if 'id' in profile
                         and profile['id'] == u'Products.MeetingIDEA:default'][0]['path']
        # the icon are located in the example_fr/images folder
        mcProfilePath = mcProfilePath.replace('profiles/default', 'profiles/idea')
        for cfg in self.portal.portal_plonemeeting.objectValues('MeetingConfig'):
            for mft in mfts:
                if not hasattr(aq_base(cfg.meetingfiletypes), mft.id):
                    cfg.addFileType(mft, source=mcProfilePath)
        logger.info('Done.')

    def _valideItemInProposed_to_secretariat(self):
        '''In 3.3, the state "proposed_to_secretariat" is removed
        '''
        logger.info('Validate Item in proposed to secretariat')
        brains = self.portal.portal_catalog(meta_type=('MeetingItem', ))
        logger.info('Check Items %d and validate if state of item is in proposed to secretariat' % len(brains))
        for brain in brains:
            item = brain.getObject()
            do = item.portal_workflow.doActionFor
            if item.queryState() == 'proposed_to_secretariat':
                do(item, 'validate')
        logger.info('Done.')

    def run(self):
        logger.info('Migrating to MeetingIDEA 3.2.0...')
        self._addDefaultAdviceAnnexesFileTypes()
        # reinstall so skins and so on are correct
        self._valideItemInProposed_to_secretariat()
        self.reinstall(profiles=[u'profile-Products.MeetingIDEA:default', ])
        self.refreshDatabase(catalogs=False, workflows=True)
        self.finish()


# The migration function -------------------------------------------------------
def migrate(context):
    '''This migration function:

       1) Add some default MeetingFileType relatedTo 'advice' so we can add annexes on advices.
    '''
    Migrate_To_3_2_0(context).run()
# ------------------------------------------------------------------------------
