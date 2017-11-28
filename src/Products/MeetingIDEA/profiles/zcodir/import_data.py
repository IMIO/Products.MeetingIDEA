# -*- coding: utf-8 -*-
from Products.PloneMeeting.profiles import AnnexTypeDescriptor, RecurringItemDescriptor
from Products.PloneMeeting.profiles import CategoryDescriptor
from Products.PloneMeeting.profiles import GroupDescriptor
from Products.PloneMeeting.profiles import ItemAnnexTypeDescriptor
from Products.PloneMeeting.profiles import MeetingConfigDescriptor
from Products.PloneMeeting.profiles import PloneMeetingConfiguration
from Products.PloneMeeting.profiles import PodTemplateDescriptor
from Products.PloneMeeting.profiles import UserDescriptor

from DateTime import DateTime

today = DateTime().strftime('%Y/%m/%d')

# File types -------------------------------------------------------------------
annexe = ItemAnnexTypeDescriptor('annexe', 'Annexe', u'attach.png')
annexeDecision = ItemAnnexTypeDescriptor('annexeDecision', 'Annexe à la décision',
                                         u'attach.png', relatedTo='item_decision')
annexeAvis = AnnexTypeDescriptor('annexeAvis', 'Annexe à un avis',
                                 u'attach.png', relatedTo='advice')
annexeSeance = AnnexTypeDescriptor('annexe', 'Annexe',
                                   u'attach.png', relatedTo='meeting')

# Categories -------------------------------------------------------------------
categories = [CategoryDescriptor('category1', 'Catégorie 1'),
              CategoryDescriptor('category2', 'Catégorie 2'),
              CategoryDescriptor('category3', 'Catégorie 3'),
              CategoryDescriptor('category4', 'Catégorie 4'),
              CategoryDescriptor('category5', 'Catégorie 5')]

# Pod templates ----------------------------------------------------------------
agendaTemplate = PodTemplateDescriptor('oj', 'Ordre du jour')
agendaTemplate.odt_file = '../../examples_fr/templates/oj.odt'
agendaTemplate.pod_formats = ['odt', 'pdf', ]
agendaTemplate.pod_portal_types = ['MeetingCoDir']
agendaTemplate.tal_condition = 'python:tool.isManager(here)'

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.odt_file = '../../examples_fr/templates/pv.odt'
decisionsTemplate.pod_formats = ['odt', 'pdf', ]
decisionsTemplate.pod_portal_types = ['MeetingCoDir']
decisionsTemplate.tal_condition = 'python:tool.isManager(here)'

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.odt_file = '../../examples_fr/templates/deliberation.odt'
itemTemplate.pod_formats = ['odt', 'pdf', ]
itemTemplate.pod_portal_types = ['MeetingItemCoDir']

codirTemplates = [agendaTemplate, decisionsTemplate, itemTemplate]

# Users and groups -------------------------------------------------------------
dgen = UserDescriptor('dgen', [], email="test@test.be", fullname="Henry Directeur")
dfin = UserDescriptor('dfin', [], email="test@test.be", fullname="Directeur Financier")
agentInfo = UserDescriptor('agentInfo', [], email="test@test.be", fullname="Agent Service Informatique")
agentCompta = UserDescriptor('agentCompta', [], email="test@test.be", fullname="Agent Service Comptabilité")
agentPers = UserDescriptor('agentPers', [], email="test@test.be", fullname="Agent Service du Personnel")
chefPers = UserDescriptor('chefPers', [], email="test@test.be", fullname="Chef Personnel")
chefCompta = UserDescriptor('chefCompta', [], email="test@test.be", fullname="Chef Comptabilité")

groups = [GroupDescriptor('dirgen', 'Directeur Général', 'DG'),
          GroupDescriptor('secretariat', 'Secrétariat communal', 'Secr'),
          GroupDescriptor('informatique', 'Service informatique', 'Info'),
          GroupDescriptor('personnel', 'Service du personnel', 'Pers'),
          GroupDescriptor('dirfin', 'Directeur Financier', 'DF'),
          GroupDescriptor('comptabilite', 'Service comptabilité', 'Compt')]

# MeetingManager
groups[0].creators.append(dgen)
groups[0].reviewers.append(dgen)
groups[0].observers.append(dgen)
groups[0].advisers.append(dgen)

groups[1].creators.append(dgen)
groups[1].reviewers.append(dgen)
groups[1].observers.append(dgen)
groups[1].advisers.append(dgen)

groups[2].creators.append(agentInfo)
groups[2].creators.append(dgen)
groups[2].reviewers.append(agentInfo)
groups[2].reviewers.append(dgen)
groups[2].observers.append(agentInfo)
groups[2].advisers.append(agentInfo)

groups[3].creators.append(agentPers)
groups[3].observers.append(agentPers)
groups[3].creators.append(dgen)
groups[3].reviewers.append(dgen)
groups[3].creators.append(chefPers)
groups[3].reviewers.append(chefPers)
groups[3].observers.append(chefPers)

groups[4].creators.append(dfin)
groups[4].reviewers.append(dfin)
groups[4].observers.append(dfin)
groups[4].advisers.append(dfin)

groups[5].creators.append(agentCompta)
groups[5].creators.append(chefCompta)
groups[5].creators.append(dfin)
groups[5].creators.append(dgen)
groups[5].reviewers.append(chefCompta)
groups[5].reviewers.append(dfin)
groups[5].reviewers.append(dgen)
groups[5].observers.append(agentCompta)
groups[5].advisers.append(chefCompta)
groups[5].advisers.append(dfin)

# Meeting configurations -------------------------------------------------------
# codir
codirMeeting = MeetingConfigDescriptor('codir', 'CODIR', 'CODIR')
codirMeeting.meetingManagers = ['pmManager', ]
codirMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                        'Charles Exemple - 1er Echevin,\n' \
                        'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                        'Jacqueline Exemple, Responsable du CPAS'
codirMeeting.signatures = 'Pierre Dupont, Bourgmestre - Charles Exemple, Secrétaire communal'
codirMeeting.certifiedSignatures = []
codirMeeting.categories = categories
codirMeeting.shortName = 'CODIR'
codirMeeting.meetingFileTypes = [annexe]
codirMeeting.usedItemAttributes = ('toDiscuss', 'associatedGroups', 'itemIsSigned',)
codirMeeting.itemWorkflow = 'meetingitemcaidea_workflow'
codirMeeting.meetingWorkflow = 'meetingcaidea_workflow'
codirMeeting.itemConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowConditions'
codirMeeting.itemActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowActions'
codirMeeting.meetingConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowConditions'
codirMeeting.meetingActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowActions'
codirMeeting.transitionsToConfirm = []
codirMeeting.transitionsForPresentingAnItem = ['validate', 'present', ]
codirMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'validateByCD',
                                                            'item_transition': 'itemValidateByCD'},

                                                           {'meeting_transition': 'freeze',
                                                            'item_transition': 'itemValidateByCD'},
                                                           {'meeting_transition': 'freeze',
                                                            'item_transition': 'itemfreeze'},

                                                           {'meeting_transition': 'decide',
                                                            'item_transition': 'itemValidateByCD'},
                                                           {'meeting_transition': 'decide',
                                                            'item_transition': 'itemfreeze'},
                                                           {'meeting_transition': 'decide',
                                                            'item_transition': 'itempublish'},

                                                           {'meeting_transition': 'close',
                                                            'item_transition': 'itemValidateByCD'},
                                                           {'meeting_transition': 'close',
                                                            'item_transition': 'itemfreeze'},
                                                           {'meeting_transition': 'close',
                                                            'item_transition': 'itempublish'},
                                                           {'meeting_transition': 'close',
                                                            'item_transition': 'accept'},

                                                           {'meeting_transition': 'backToCreated',
                                                            'item_transition': 'backToValidateByCD'},
                                                           {'meeting_transition': 'backToCreated',
                                                            'item_transition': 'backToPresented'},

                                                           {'meeting_transition': 'backToValidatedByCD',
                                                            'item_transition': 'backToValidateByCD'},)

codirMeeting.meetingTopicStates = ('created', 'frozen')
codirMeeting.decisionTopicStates = ('decided', 'closed')
codirMeeting.recordItemHistoryStates = []
codirMeeting.maxShownMeetings = 5
codirMeeting.maxDaysDecisions = 60
codirMeeting.meetingAppDefaultView = 'searchmyitems'
codirMeeting.itemDocFormats = ('odt', 'pdf')
codirMeeting.meetingDocFormats = ('odt', 'pdf')
codirMeeting.useAdvices = True
codirMeeting.itemAdviceStates = ['proposed_to_director', ]
codirMeeting.itemAdviceEditStates = ['proposed_to_director', 'validated']
codirMeeting.itemAdviceViewStates = ['presented', ]
codirMeeting.transitionReinitializingDelays = 'backToItemCreated'
codirMeeting.enforceAdviceMandatoriness = False
codirMeeting.itemPowerObserversStates = ('itemcreated', 'presented', 'accepted', 'delayed', 'refused')
codirMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
codirMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                           'reverse': '0'},)
codirMeeting.useGroupsAsCategories = True
codirMeeting.meetingPowerObserversStates = ('frozen', 'published', 'decided', 'closed')
codirMeeting.useCopies = True
codirMeeting.selectableCopyGroups = [groups[0].getIdSuffixed('reviewers'),
                                     groups[1].getIdSuffixed('reviewers'),
                                     groups[2].getIdSuffixed('reviewers'),
                                     groups[4].getIdSuffixed('reviewers')]
codirMeeting.podTemplates = [agendaTemplate, decisionsTemplate, itemTemplate]
codirMeeting.meetingConfigsToCloneTo = []
codirMeeting.recurringItems = [
    RecurringItemDescriptor(
        id='recItem1',
        description='<p>This is the first recurring item.</p>',
        title='Recurring item #1',
        proposingGroup='developers',
        decision='First recurring item approved'),

    RecurringItemDescriptor(
        id='recItem2',
        title='Recurring item #2',
        description='<p>This is the second recurring item.</p>',
        proposingGroup='developers',
        decision='Second recurring item approved'),
]
codirMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(codirMeeting,),
                                 groups=groups)
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
