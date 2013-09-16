# -*- coding: utf-8 -*-
from Products.PloneMeeting.profiles import *
from Products.MeetingIDEA.config import *

# File types -------------------------------------------------------------------
annexe = MeetingFileTypeDescriptor('annexe', 'Annexe', 'attach.png', '')
annexeBudget = MeetingFileTypeDescriptor('annexeBudget', 'Article Budgétaire', 'budget.png', '')
annexeCahier = MeetingFileTypeDescriptor('annexeCahier', 'Cahier des Charges', 'cahier.gif', '')
annexeDecision = MeetingFileTypeDescriptor('annexeDecision', 'Annexe à la décision', 'attach.png', '', True, active=False)

# Pod templates ----------------------------------------------------------------
agendaTemplate = PodTemplateDescriptor('agenda', 'Ordre du jour')
agendaTemplate.podTemplate = 'Agenda.odt'
agendaTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_membership.' \
                              'getAuthenticatedMember().has_role("' \
                              'MeetingManager")'

agendaTemplatePDF = PodTemplateDescriptor('agendapdf', 'Ordre du jour')
agendaTemplatePDF.podTemplate = 'Agenda.odt'
agendaTemplatePDF.podFormat = 'pdf'
agendaTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                  'here.portal_membership.' \
                                  'getAuthenticatedMember().has_role("' \
                                  'MeetingManager")'

decisionsTemplate = PodTemplateDescriptor('decisions', 'Procès-verbal')
decisionsTemplate.podTemplate = 'Decisions.odt'
decisionsTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                 'here.portal_membership.' \
                                 'getAuthenticatedMember().has_role("' \
                                 'MeetingManager")'

decisionsTemplatePDF = PodTemplateDescriptor('decisionspdf', 'Procès-verbal')
decisionsTemplatePDF.podTemplate = 'Decisions.odt'
decisionsTemplatePDF.podFormat = 'pdf'
decisionsTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                    'here.portal_membership.' \
                                    'getAuthenticatedMember().has_role("' \
                                    'MeetingManager")'
decisionsByCatTemplate = PodTemplateDescriptor('decisionsbycat', 'PV avec catégories')
decisionsByCatTemplate.podTemplate = 'DecisionsWithItemsByCategory.odt'
decisionsByCatTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                 'here.portal_membership.' \
                                 'getAuthenticatedMember().has_role("' \
                                 'MeetingManager")'

decisionsByCatTemplatePDF = PodTemplateDescriptor('decisionsbycatpdf', 'PV avec catégories')
decisionsByCatTemplatePDF.podTemplate = 'DecisionsWithItemsByCategory.odt'
decisionsByCatTemplatePDF.podFormat = 'pdf'
decisionsByCatTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                    'here.portal_membership.' \
                                    'getAuthenticatedMember().has_role("' \
                                    'MeetingManager")'

itemTemplate = PodTemplateDescriptor('item', 'Délibération')
itemTemplate.podTemplate = 'MeetingItem.odt'
itemTemplate.podCondition = 'python:here.meta_type=="MeetingItem"'

itemTemplatePDF = PodTemplateDescriptor('itempdf', 'Délibération')
itemTemplatePDF.podTemplate = 'MeetingItem.odt'
itemTemplatePDF.podFormat = 'pdf'
itemTemplatePDF.podCondition = 'python:here.meta_type=="MeetingItem"'

allTemplates = [agendaTemplate, agendaTemplatePDF,
                decisionsTemplate, decisionsTemplatePDF,
                decisionsByCatTemplate, decisionsByCatTemplatePDF,
                itemTemplate, itemTemplatePDF]


# Users and groups -------------------------------------------------------------
secretaire = UserDescriptor('secretaire', ['MeetingManager'], email="test@test.be")
agentInfo = UserDescriptor('agentInfo', [], email="test@test.be")
chefInfo = UserDescriptor('chefInfo', [], email="test@test.be")

groups = [
           GroupDescriptor('secretariat', 'Secretariat', 'Secr'),
           GroupDescriptor('informatique', 'Service informatique', 'Info'),
           GroupDescriptor('personnel', 'Service du personnel', 'Pers'),
         ]

# MeetingManager
groups[0].creators.append(secretaire)
groups[0].observers.append(secretaire)
groups[0].advisers.append(secretaire)

groups[1].creators.append(agentInfo)
groups[1].creators.append(secretaire)
groups[1].observers.append(agentInfo)
groups[1].advisers.append(agentInfo)
groups[1].reviewers.append(chefInfo)
groups[1].reviewers.append(secretaire)


# Meeting configurations -------------------------------------------------------
# CA
CAMeeting = MeetingConfigDescriptor(
    'meeting-config-CA', 'CA',
    'CA', isDefault=True)
CAMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                          'Charles Exemple - 1er Echevin,\n' \
                          'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                          'Jacqueline Exemple, Responsable du CPAS'
CAMeeting.signatures = 'Pierre Dupont, Bourgmestre - Charles Exemple, 1er Echevin'
CAMeeting.categories = []
CAMeeting.shortName = 'CA'
CAMeeting.meetingFileTypes = [annexe, annexeBudget, annexeCahier, annexeDecision]
CAMeeting.itemWorkflow = 'meetingitemcaidea_workflow'
CAMeeting.meetingWorkflow = 'meetingcaidea_workflow'
CAMeeting.itemConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowConditions'
CAMeeting.itemActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowActions'
CAMeeting.meetingConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowConditions'
CAMeeting.meetingActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowActions'
CAMeeting.itemTopicStates = ('itemcreated', 'proposedToDepartmentHead', 'proposedToDirector', 'proposedToSecretariat', 'proposedToValidationByDirector', 'proposedToValidationBySecretariat', 'proposedToDG', 'validated', 'presented', 'itemfrozen', 'accepted', 'refused', 'delayed', 'pre_accepted', 'removed',)
CAMeeting.meetingTopicStates = ('created', 'frozen')
CAMeeting.decisionTopicStates = ('decided', 'closed')
CAMeeting.itemAdviceStates = ('validated',)
CAMeeting.itemAdviceEditStates = ('validated',)
CAMeeting.recordItemHistoryStates = ['',]
CAMeeting.maxShownMeetings = 5
CAMeeting.maxDaysDecisions = 60
CAMeeting.meetingAppDefaultView = 'topic_searchmyitems'
CAMeeting.itemDocFormats = ('odt', 'pdf')
CAMeeting.meetingDocFormats = ('odt', 'pdf')
CAMeeting.useAdvices = True
CAMeeting.enforceAdviceMandatoriness = False
CAMeeting.enableAdviceInvalidation = False
CAMeeting.useCopies = True
CAMeeting.selectableCopyGroups = [groups[0].getIdSuffixed('reviewers'), groups[1].getIdSuffixed('reviewers')]
CAMeeting.podTemplates = allTemplates
CAMeeting.sortingMethodOnAddItem = 'on_proposing_groups'
CAMeeting.useGroupsAsCategories = True
CAMeeting.recurringItems = []
CAMeeting.meetingUsers = []

# AG
# Categories -------------------------------------------------------------------

AGMeeting = MeetingConfigDescriptor(
    'meeting-config-AG', 'AG',
    'AG')
AGMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                          'Charles Exemple - 1er Echevin,\n' \
                          'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                          'Jacqueline Exemple, Responsable du CPAS'
AGMeeting.categories = []
AGMeeting.shortName = 'AG'
AGMeeting.meetingFileTypes = [annexe, annexeBudget, annexeCahier, annexeDecision]
AGMeeting.usedItemAttributes = ['observations', 'itemAssembly', ]
AGMeeting.usedMeetingAttributes = ('place', 'observations', 'signatures', 'assembly', 'preMeetingDate', 'preMeetingPlace', 'preMeetingAssembly', \
                                        'preMeetingDate_2', 'preMeetingPlace_2', 'preMeetingAssembly_2', 'preMeetingDate_3', 'preMeetingPlace_3', 'preMeetingAssembly_3', \
                                        'preMeetingDate_4', 'preMeetingPlace_4', 'preMeetingAssembly_4', 'preMeetingDate_5', 'preMeetingPlace_5', 'preMeetingAssembly_5', \
                                        'preMeetingDate_6', 'preMeetingPlace_6', 'preMeetingAssembly_6', 'preMeetingDate_7', 'preMeetingPlace_7', 'preMeetingAssembly_7',
                                        'startDate', 'endDate',
)
AGMeeting.recordMeetingHistoryStates = []
AGMeeting.itemWorkflow = 'meetingitemcaidea_workflow'
AGMeeting.meetingWorkflow = 'meetingcaidea_workflow'
AGMeeting.itemConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowConditions'
AGMeeting.itemActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowActions'
AGMeeting.meetingConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowConditions'
AGMeeting.meetingActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowActions'
#show every items states
AGMeeting.itemTopicStates = ('itemcreated', 'proposedToDepartmentHead', 'proposedToDirector', 'proposedToSecretariat', 'proposedToValidationByDirector', 'proposedToValidationBySecretariat', 'proposedToDG', 'validated', 'presented', 'itemfrozen', 'accepted', 'refused', 'delayed', 'pre_accepted', 'removed',)
AGMeeting.meetingTopicStates = ('created', 'frozen')
AGMeeting.decisionTopicStates = ('decided', 'closed')
AGMeeting.itemAdviceStates = ('itemcreated',)
AGMeeting.itemAdviceEditStates = ('itemcreated',)
AGMeeting.recordItemHistoryStates = ['',]
AGMeeting.maxShownMeetings = 5
AGMeeting.maxDaysDecisions = 60
AGMeeting.meetingAppDefaultView = 'topic_searchmyitems'
AGMeeting.itemDocFormats = ('odt', 'pdf')
AGMeeting.meetingDocFormats = ('odt', 'pdf')
AGMeeting.useAdvices = True
AGMeeting.enforceAdviceMandatoriness = False
AGMeeting.enableAdviceInvalidation = False
AGMeeting.useCopies = True
AGMeeting.selectableCopyGroups = [groups[0].getIdSuffixed('reviewers'), groups[1].getIdSuffixed('reviewers')]
AGMeeting.podTemplates = allTemplates
AGMeeting.transitionsToConfirm = ['MeetingItem.return_to_service',]
AGMeeting.sortingMethodOnAddItem = 'on_proposing_groups'
AGMeeting.useGroupsAsCategories = True

data = PloneMeetingConfiguration(
           meetingFolderTitle='Mes séances',
           meetingConfigs=(CAMeeting, AGMeeting),
           groups=groups)
data.unoEnabledPython='/usr/bin/python'
data.usedColorSystem='state_color'
# ------------------------------------------------------------------------------
