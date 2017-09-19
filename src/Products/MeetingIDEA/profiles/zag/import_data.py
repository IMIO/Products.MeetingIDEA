# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.PloneMeeting.profiles import AnnexTypeDescriptor
from Products.PloneMeeting.profiles import CategoryDescriptor
from Products.PloneMeeting.profiles import ItemAnnexTypeDescriptor
from Products.PloneMeeting.profiles import PodTemplateDescriptor
from Products.PloneMeeting.profiles import MeetingConfigDescriptor
from Products.PloneMeeting.profiles import PloneMeetingConfiguration

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
agendaTemplate.pod_portal_types = ['MeetingAG']
agendaTemplate.tal_condition = 'python:tool.isManager(here)'

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.odt_file = '../../examples_fr/templates/pv.odt'
decisionsTemplate.pod_formats = ['odt', 'pdf', ]
decisionsTemplate.pod_portal_types = ['MeetingAG']
decisionsTemplate.tal_condition = 'python:tool.isManager(here)'

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.odt_file = '../../examples_fr/templates/deliberation.odt'
itemTemplate.pod_formats = ['odt', 'pdf', ]
itemTemplate.pod_portal_types = ['MeetingItemAG']

agTemplates = [agendaTemplate, decisionsTemplate, itemTemplate]

# Meeting configurations -------------------------------------------------------
# ag
agMeeting = MeetingConfigDescriptor(
    'meeting-config-ag', 'Assemblée Générale',
    'Assemblée Générale')
agMeeting.meetingManagers = ['pmManager',]
agMeeting.assembly = 'Default assembly'
                     
agMeeting.signatures = 'Default signatures'
agMeeting.certifiedSignatures = []

agMeeting.categories = categories
agMeeting.shortName = 'AG'
agMeeting.annexTypes = [annexe, annexeDecision, annexeAvis, annexeSeance]
agMeeting.itemWorkflow = 'meetingitemcaidea_workflow'
agMeeting.meetingWorkflow = 'meetingcaidea_workflow'
agMeeting.itemConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowConditions'
agMeeting.itemActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowActions'
agMeeting.meetingConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowConditions'
agMeeting.meetingActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowActions'
agMeeting.transitionsToConfirm = []
agMeeting.meetingTopicStates = ('created', 'frozen', 'published')
agMeeting.decisionTopicStates = ('decided', 'closed')
agMeeting.enforceAdviceMandatoriness = False
agMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_categories',
                                        'reverse': '0'}, )
agMeeting.recordItemHistoryStates = []
agMeeting.maxShownMeetings = 5
agMeeting.maxDaysDecisions = 60
agMeeting.meetingAppDefaultView = 'searchmyitems'
agMeeting.usedItemAttributes = ('toDiscuss', 'associatedGroups', 'itemIsSigned',)
agMeeting.useAdvices = False
agMeeting.itemAdviceStates = ('proposed_to_director',)
agMeeting.itemAdviceEditStates = ('proposed_to_director', 'validated',)
agMeeting.itemAdviceViewStates = ('presented',)
agMeeting.transitionReinitializingDelays = 'backToItemCreated'
agMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
agMeeting.enableAdviceInvalidation = False
agMeeting.itemAdviceInvalidateStates = []
agMeeting.customAdvisers = []
agMeeting.itemPowerObserversStates = ('itemcreated', 'presented', 'accepted', 'delayed', 'refused')
agMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
agMeeting.workflowAdaptations = ['no_publication', 'no_global_observation', 'return_to_proposing_group']
agMeeting.transitionsForPresentingAnItem = ('validate', 'present', )
agMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le Comité décide de reporter le point.</p>"},))
agMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'validateByCD',
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
                                                         'item_transition': 'backToValidatedByCD'},
                                                        {'meeting_transition': 'backToCreated',
                                                         'item_transition': 'backToPresented'},

                                                        {'meeting_transition': 'backToValidatedByCD',
                                                         'item_transition': 'backToValidatedByCD'},)
agMeeting.meetingPowerObserversStates = ('frozen', 'published', 'decided', 'closed')
agMeeting.powerAdvisersGroups = ()
agMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
agMeeting.useCopies = True
agMeeting.selectableCopyGroups = []
agMeeting.useVotes = True
agMeeting.meetingUsers = []
agMeeting.meetingConfigsToCloneTo = []
agMeeting.recurringItems = []
agMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(agMeeting, ),
                                 groups=[])
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
