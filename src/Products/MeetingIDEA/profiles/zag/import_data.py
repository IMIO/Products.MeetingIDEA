# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.PloneMeeting.profiles import MeetingFileTypeDescriptor
from Products.PloneMeeting.profiles import CategoryDescriptor
from Products.PloneMeeting.profiles import PodTemplateDescriptor
from Products.PloneMeeting.profiles import MeetingConfigDescriptor
from Products.PloneMeeting.profiles import PloneMeetingConfiguration

today = DateTime().strftime('%Y/%m/%d')

# File types -------------------------------------------------------------------
annexe = MeetingFileTypeDescriptor('annexe', 'Annexe', 'attach.png', '')
annexeDecision = MeetingFileTypeDescriptor('annexeDecision', 'Annexe à la décision', 'attach.png', '', 'item_decision')
annexeAvis = MeetingFileTypeDescriptor('annexeAvis', 'Annexe à un avis',
                                       'attach.png', '', 'advice')

# Categories -------------------------------------------------------------------
categories = [CategoryDescriptor('category1', 'Catégorie 1'),
              CategoryDescriptor('category2', 'Catégorie 2'),
              CategoryDescriptor('category3', 'Catégorie 3'),
              CategoryDescriptor('category4', 'Catégorie 4'),
              CategoryDescriptor('category5', 'Catégorie 5')]

# Pod templates ----------------------------------------------------------------
agendaTemplate = PodTemplateDescriptor('oj', 'Ordre du jour')
agendaTemplate.podTemplate = '../../examples_fr/templates/oj.odt'
agendaTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager(here)'

agendaTemplatePDF = PodTemplateDescriptor('oj-pdf', 'Ordre du jour')
agendaTemplatePDF.podTemplate = '../../examples_fr/templates/oj.odt'
agendaTemplatePDF.podFormat = 'pdf'
agendaTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                 'here.portal_plonemeeting.isManager(here)'

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.podTemplate = '../../examples_fr/templates/pv.odt'
decisionsTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                 'here.portal_plonemeeting.isManager(here)'

decisionsTemplatePDF = PodTemplateDescriptor('pv-pdf', 'Procès-verbal')
decisionsTemplatePDF.podTemplate = '../../examples_fr/templates/pv.odt'
decisionsTemplatePDF.podFormat = 'pdf'
decisionsTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                    'here.portal_plonemeeting.isManager(here)'

itemProjectTemplate = PodTemplateDescriptor('projet-deliberation', 'Projet délibération')
itemProjectTemplate.podTemplate = '../../examples_fr/templates/projet-deliberation.odt'
itemProjectTemplate.podCondition = 'python:here.meta_type=="MeetingItem" and not here.hasMeeting()'

itemProjectTemplatePDF = PodTemplateDescriptor('projet-deliberation-pdf', 'Projet délibération')
itemProjectTemplatePDF.podTemplate = '../../examples_fr/templates/projet-deliberation.odt'
itemProjectTemplatePDF.podFormat = 'pdf'
itemProjectTemplatePDF.podCondition = 'python:here.meta_type=="MeetingItem" and not here.hasMeeting()'

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.podTemplate = '../../examples_fr/templates/deliberation.odt'
itemTemplate.podCondition = 'python:here.meta_type=="MeetingItem" and here.hasMeeting()'

itemTemplatePDF = PodTemplateDescriptor('deliberation-pdf', 'Délibération')
itemTemplatePDF.podTemplate = '../../examples_fr/templates/deliberation.odt'
itemTemplatePDF.podFormat = 'pdf'
itemTemplatePDF.podCondition = 'python:here.meta_type=="MeetingItem" and here.hasMeeting()'

agTemplates = [agendaTemplate, agendaTemplatePDF,
               decisionsTemplate, decisionsTemplatePDF,
               itemProjectTemplate, itemProjectTemplatePDF,
               itemTemplate, itemTemplatePDF]

# Meeting configurations -------------------------------------------------------
# ag
agMeeting = MeetingConfigDescriptor(
    'meeting-config-ag', 'Assemblée générale',
    'Assemblée générale')
agMeeting.meetingManagers = ['pmManager', ]
agMeeting.assembly = 'Default assembly'
agMeeting.signatures = 'Default signatures'
agMeeting.certifiedSignatures = []
agMeeting.categories = categories
agMeeting.shortName = 'AG'
agMeeting.meetingFileTypes = [annexe, annexeDecision, annexeAvis]
agMeeting.itemWorkflow = 'meetingitemcaidea_workflow'
agMeeting.meetingWorkflow = 'meetingcaidea_workflow'
agMeeting.itemConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowConditions'
agMeeting.itemActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowActions'
agMeeting.meetingConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowConditions'
agMeeting.meetingActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowActions'
agMeeting.transitionsToConfirm = []
agMeeting.transitionsForPresentingAnItem = ['validate', 'present', ]
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

agMeeting.meetingTopicStates = ('created', 'frozen', 'published')
agMeeting.decisionTopicStates = ('decided', 'closed')
agMeeting.itemAdviceStates = ('validated',)
agMeeting.recordItemHistoryStates = []
agMeeting.maxShownMeetings = 5
agMeeting.maxDaysDecisions = 60
agMeeting.meetingAppDefaultView = 'topic_searchmyitems'
agMeeting.usedItemAttributes = ('toDiscuss', 'associatedGroups', 'itemIsSigned',)
agMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_categories',
                                        'reverse': '0'}, )
agMeeting.useGroupsAsCategories = False
agMeeting.useAdvices = False
agMeeting.itemAdviceStates = ['proposed_to_director', ]
agMeeting.itemAdviceEditStates = ['proposed_to_director', 'validated']
agMeeting.itemAdviceViewStates = ['presented', ]
agMeeting.transitionReinitializingDelays = 'backToItemCreated'
agMeeting.enforceAdviceMandatoriness = False
agMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
agMeeting.itemPowerObserversStates = ('itemcreated', 'presented', 'accepted', 'delayed', 'refused')
agMeeting.meetingPowerObserversStates = ('frozen', 'published', 'decided', 'closed')
agMeeting.useCopies = True
agMeeting.selectableCopyGroups = []
agMeeting.useVotes = True
agMeeting.meetingUsers = []
agMeeting.recurringItems = []
agMeeting.itemTemplates = ()

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(agMeeting, ),
                                 groups=[])
data.unoEnabledPython = '/usr/bin/python'
data.usedColorSystem = 'state_color'
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
