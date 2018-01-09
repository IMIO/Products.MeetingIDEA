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

categories = [CategoryDescriptor('category1', 'Catégorie 1'),
              CategoryDescriptor('category2', 'Catégorie 2'),
              CategoryDescriptor('category3', 'Catégorie 3'),
              CategoryDescriptor('category4', 'Catégorie 4'),
              CategoryDescriptor('category5', 'Catégorie 5')]

# Pod templates ----------------------------------------------------------------
agendaTemplate = PodTemplateDescriptor('oj', 'Ordre du jour')
agendaTemplate.odt_file = '../../examples_fr/templates/oj.odt'
agendaTemplate.pod_formats = ['odt', 'pdf', ]
agendaTemplate.pod_portal_types = ['MeetingCOGES']
agendaTemplate.tal_condition = 'python:tool.isManager(here)'

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.odt_file = '../../examples_fr/templates/pv.odt'
decisionsTemplate.pod_formats = ['odt', 'pdf', ]
decisionsTemplate.pod_portal_types = ['MeetingCOGES']
decisionsTemplate.tal_condition = 'python:tool.isManager(here)'

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.odt_file = '../../examples_fr/templates/deliberation.odt'
itemTemplate.pod_formats = ['odt', 'pdf', ]
itemTemplate.pod_portal_types = ['MeetingItemCOGES']

coGesTemplates = [agendaTemplate, decisionsTemplate, itemTemplate]

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
# cgpp
cgppMeeting = MeetingConfigDescriptor('cgpp', 'CGPP', 'CGPP')
cgppMeeting.meetingManagers = ['pmManager', ]
cgppMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                       'Charles Exemple - 1er Echevin,\n' \
                       'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                       'Jacqueline Exemple, Responsable du CPAS'
cgppMeeting.signatures = 'Pierre Dupont, Bourgmestre - Charles Exemple, Secrétaire communal'
cgppMeeting.certifiedSignatures = []
cgppMeeting.categories = categories
cgppMeeting.shortName = 'CGPP'
cgppMeeting.meetingFileTypes = [annexe]
cgppMeeting.usedItemAttributes = ('toDiscuss', 'associatedGroups', 'itemIsSigned',)
cgppMeeting.itemWorkflow = 'meetingitemcaidea_workflow'
cgppMeeting.meetingWorkflow = 'meetingcaidea_workflow'
cgppMeeting.itemConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowConditions'
cgppMeeting.itemActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowActions'
cgppMeeting.meetingConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowConditions'
cgppMeeting.meetingActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowActions'
cgppMeeting.transitionsToConfirm = []
cgppMeeting.transitionsForPresentingAnItem = ['validate', 'present', ]
cgppMeeting.onMeetingTransitionItemTransitionToTrigger = (
                                                        {'meeting_transition': 'freeze',
                                                         'item_transition': 'itemfreeze'},
                                                        {'meeting_transition': 'decide',
                                                         'item_transition': 'itemfreeze'},
                                                        {'meeting_transition': 'close',
                                                         'item_transition': 'itemfreeze'},
                                                        {'meeting_transition': 'close',
                                                         'item_transition': 'accept'},
                                                        {'meeting_transition': 'backToCreated',
                                                         'item_transition': 'backToPresented'},)

cgppMeeting.meetingTopicStates = ('created', 'frozen')
cgppMeeting.decisionTopicStates = ('decided', 'closed')
cgppMeeting.recordItemHistoryStates = []
cgppMeeting.maxShownMeetings = 5
cgppMeeting.maxDaysDecisions = 60
cgppMeeting.meetingAppDefaultView = 'searchmyitems'
cgppMeeting.itemDocFormats = ('odt', 'pdf')
cgppMeeting.meetingDocFormats = ('odt', 'pdf')
cgppMeeting.useAdvices = True
cgppMeeting.itemAdviceStates = ['proposed_to_director', ]
cgppMeeting.itemAdviceEditStates = ['proposed_to_director', 'validated']
cgppMeeting.itemAdviceViewStates = ['presented', ]
cgppMeeting.transitionReinitializingDelays = 'backToItemCreated'
cgppMeeting.enforceAdviceMandatoriness = False
cgppMeeting.itemPowerObserversStates = ('itemcreated', 'presented', 'accepted', 'delayed', 'refused')
cgppMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
cgppMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                          'reverse': '0'},)
cgppMeeting.useGroupsAsCategories = True
cgppMeeting.meetingPowerObserversStates = ('frozen', 'published', 'decided', 'closed')
cgppMeeting.useCopies = True
cgppMeeting.selectableCopyGroups = []
cgppMeeting.podTemplates = []
cgppMeeting.meetingConfigsToCloneTo = []
cgppMeeting.recurringItems = []
cgppMeeting.itemTemplates = []


# Meeting configurations -------------------------------------------------------
# cgpart
cgpartMeeting = MeetingConfigDescriptor('cgpart', 'CGPART', 'CGPART')
cgpartMeeting.meetingManagers = ['pmManager', ]
cgpartMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                       'Charles Exemple - 1er Echevin,\n' \
                       'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                       'Jacqueline Exemple, Responsable du CPAS'
cgpartMeeting.signatures = 'Pierre Dupont, Bourgmestre - Charles Exemple, Secrétaire communal'
cgpartMeeting.certifiedSignatures = []
cgpartMeeting.categories = categories
cgpartMeeting.shortName = 'CGPART'
cgpartMeeting.meetingFileTypes = [annexe]
cgpartMeeting.usedItemAttributes = ('toDiscuss', 'associatedGroups', 'itemIsSigned',)
cgpartMeeting.itemWorkflow = 'meetingitemcaidea_workflow'
cgpartMeeting.meetingWorkflow = 'meetingcaidea_workflow'
cgpartMeeting.itemConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowConditions'
cgpartMeeting.itemActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowActions'
cgpartMeeting.meetingConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowConditions'
cgpartMeeting.meetingActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowActions'
cgpartMeeting.transitionsToConfirm = []
cgpartMeeting.transitionsForPresentingAnItem = ['validate', 'present', ]
cgpartMeeting.onMeetingTransitionItemTransitionToTrigger = (
                                                        {'meeting_transition': 'freeze',
                                                         'item_transition': 'itemfreeze'},
                                                        {'meeting_transition': 'decide',
                                                         'item_transition': 'itemfreeze'},
                                                        {'meeting_transition': 'close',
                                                         'item_transition': 'itemfreeze'},
                                                        {'meeting_transition': 'close',
                                                         'item_transition': 'accept'},
                                                        {'meeting_transition': 'backToCreated',
                                                         'item_transition': 'backToPresented'},)

cgpartMeeting.meetingTopicStates = ('created', 'frozen')
cgpartMeeting.decisionTopicStates = ('decided', 'closed')
cgpartMeeting.recordItemHistoryStates = []
cgpartMeeting.maxShownMeetings = 5
cgpartMeeting.maxDaysDecisions = 60
cgpartMeeting.meetingAppDefaultView = 'searchmyitems'
cgpartMeeting.itemDocFormats = ('odt', 'pdf')
cgpartMeeting.meetingDocFormats = ('odt', 'pdf')
cgpartMeeting.useAdvices = True
cgpartMeeting.itemAdviceStates = ['proposed_to_director', ]
cgpartMeeting.itemAdviceEditStates = ['proposed_to_director', 'validated']
cgpartMeeting.itemAdviceViewStates = ['presented', ]
cgpartMeeting.transitionReinitializingDelays = 'backToItemCreated'
cgpartMeeting.enforceAdviceMandatoriness = False
cgpartMeeting.itemPowerObserversStates = ('itemcreated', 'presented', 'accepted', 'delayed', 'refused')
cgpartMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
cgpartMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                          'reverse': '0'},)
cgpartMeeting.useGroupsAsCategories = True
cgpartMeeting.meetingPowerObserversStates = ('frozen', 'published', 'decided', 'closed')
cgpartMeeting.useCopies = True
cgpartMeeting.selectableCopyGroups = []
cgpartMeeting.podTemplates = []
cgpartMeeting.meetingConfigsToCloneTo = []
cgpartMeeting.recurringItems = []
cgpartMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(cgppMeeting, cgpartMeeting),
                                 groups=groups)
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
