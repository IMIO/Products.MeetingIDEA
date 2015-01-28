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
        '''The state "proposed_to_secretariat" is removed.
        '''
        brains = self.portal.portal_catalog(meta_type=('MeetingItem', ))
        logger.info('Check Items %d and validate if state of item is in proposed to secretariat' % len(brains))
        for brain in brains:
            item = brain.getObject()
            do = item.portal_workflow.doActionFor
            if item.queryState() == 'proposed_to_secretariat':
                do(item, 'validate')
            item.updateLocalRoles()
        logger.info('Done.')

    def _migrateDirectorsInReviewersGroups(self):
        ''' MeetingDirector was removed, we must use reviewer suffix for roles.
            We must change selectableCopyGroups (replace director by reviewer).
        '''
        logger.info('Place director in reviewer group')
        pg = self.portal.portal_groups
        pgroups = pg.listGroups()
        for pgroup in pgroups:
            # if the group suffix is director (ie. xxx_director), get corresponding reviewer group (ie.xxx_reviewer)
            # and add the same member. After that, remove director's group
            if pgroup.id.endswith('_director'):
                directors = pgroup.getGroupMembers()
                group_reviewerID = pgroup.id.replace('_director', '_reviewers')
                group_reviewer = pg.getGroupById(group_reviewerID)
                # add member
                for director in directors:
                    group_reviewer.addMember(director.id)
                # remove group
                pg.removeGroup(pgroup.id)
            if pgroup.id.endswith('_reviewers'):
                # change title secretariat in director
                new_groupName = pgroup.getGroupTitleOrName().replace('(Secrétariat)', '(Directeur)')
                pgroup.setProperties(title=new_groupName)
        #replace selectable group for each meetingConfig
        for cfg in self.portal.portal_plonemeeting.objectValues('MeetingConfig'):
            new_scg = []
            for scg in cfg.getSelectableCopyGroups():
                new_scg.append(scg.replace('_director', '_reviewers'))
            cfg.setSelectableCopyGroups(new_scg)
        logger.info('Done.')

    def _transferClassifierToStartegicAxis(self):
        '''We use Strategic Axis instead of Classifier, because it's multivalued field.'''
        brains = self.portal.portal_catalog(meta_type=('MeetingItem', ))
        logger.info('Transfer Classifier in Strategic Axis for %d items.' % len(brains))
        for brain in brains:
            item = brain.getObject()
            item.setStrategicAxis((item.getClassifier(), ))
        logger.info('Done.')

    def run(self):
        logger.info('Migrating to MeetingIDEA 3.2.0...')
        self._addDefaultAdviceAnnexesFileTypes()
        self._valideItemInProposed_to_secretariat()
        self._migrateDirectorsInReviewersGroups()
        self._transferClassifierToStartegicAxis()
        # reinstall so skins and so on are correct
        self.reinstall(profiles=[u'profile-Products.MeetingIDEA:default', ])
        self.refreshDatabase(workflows=True)
        self.finish()


# The migration function -------------------------------------------------------
def migrate(context):
    '''This migration function:

       1) Add some default MeetingFileType relatedTo 'advice' so we can add annexes on advices.
    '''
    Migrate_To_3_2_0(context).run()
# ------------------------------------------------------------------------------
