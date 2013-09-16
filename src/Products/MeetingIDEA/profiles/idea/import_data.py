# -*- coding: utf-8 -*-
from Products.PloneMeeting.profiles import *
from Products.MeetingIDEA.config import *

# File types -------------------------------------------------------------------
annexe = MeetingFileTypeDescriptor('annexe', 'Annexe', 'attach.png', '')
annexeBudget = MeetingFileTypeDescriptor('annexeBudget', 'Article Budgétaire', 'budget.png', '')
annexeCahier = MeetingFileTypeDescriptor('annexeCahier', 'Cahier des Charges', 'cahier.gif', '')
annexeDecision = MeetingFileTypeDescriptor('annexeDecision', 'Annexe à la décision', 'attach.png', '',
                                           True, active=False)

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


# Users and groups are imported after initialized-------------------------------------------------------------

# Meeting configurations -------------------------------------------------------
# CA
CAMeeting = MeetingConfigDescriptor(
    'meeting-config-CA', 'CA',
    'CA', isDefault=True)
CAMeeting.assembly = 'M. Pierre TACHENION Président\n' \
                     'Mmes Jacqueline GALANT, Catherine HOUDART, Elena MILLITARI, Savine MOUCHERON, Annie TAULET\n' \
                     'MM. Georges-Louis BOUCHEZ, Philippe DEBAISIEUX, Benoît DE GHORAIN, Alain DE NOOZE, ' \
                     'Yves DRUGMAND, Jean-Marc DUPONT, Jacques FAUCONNIER, Philippe FONTAINE, Fabrice FOURMANOIT, ' \
                     'Jacques GOBERT, Jean GODIN, François GOUDAILLEZ, Pascal HOYAUX, Michel HUIN, ' \
                     'Jean-Pierre JAUMOT, Bernard LIEBIN, Vincent LOISEAU, Bernard PIRSON, Patrick PREVOT, ' \
                     'Ahmed RYADI, Achille SAKAS, Philippe TISON, Jean-Marc URBAIN, Marc WINDERS Administrateurs \n' \
                     'M. Jean-François ESCARMELLE Directeur Général\n' \
                     'Mme Axelle DINANT Secrétaire du Conseil d’Administration'
CAMeeting.signatures = "Axelle DINANT,\n Secrétaire du Conseil d'Administration.\n" \
                       "Pierre TACHENION, \n Président."
CAMeeting.categories = []
CAMeeting.shortName = 'CA'
CAMeeting.meetingFileTypes = [annexe, annexeBudget, annexeCahier, annexeDecision]
CAMeeting.itemWorkflow = 'meetingitemcaidea_workflow'
CAMeeting.meetingWorkflow = 'meetingcaidea_workflow'
CAMeeting.itemConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowConditions'
CAMeeting.itemActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowActions'
CAMeeting.meetingConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowConditions'
CAMeeting.meetingActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowActions'
CAMeeting.itemTopicStates = ('itemcreated', 'proposedToDepartmentHead', 'proposedToDirector', 'proposedToSecretariat',
                             'validated', 'presented', 'validated_by_cd', 'itemfrozen', 'accepted', 'refused',
                             'delayed', 'pre_accepted', 'removed',)
CAMeeting.meetingTopicStates = ('created', 'validated_by_cd', 'frozen')
CAMeeting.decisionTopicStates = ('decided', 'closed')
CAMeeting.itemAdviceStates = ('validated',)
CAMeeting.itemAdviceEditStates = ('validated',)
CAMeeting.recordItemHistoryStates = ['', ]
CAMeeting.maxShownMeetings = 5
CAMeeting.maxDaysDecisions = 60
CAMeeting.meetingAppDefaultView = 'topic_searchmyitems'
CAMeeting.itemDocFormats = ('odt', 'pdf')
CAMeeting.meetingDocFormats = ('odt', 'pdf')
CAMeeting.useAdvices = True
CAMeeting.enforceAdviceMandatoriness = False
CAMeeting.enableAdviceInvalidation = False
CAMeeting.useCopies = True
CAMeeting.selectableCopyGroups = []
CAMeeting.podTemplates = allTemplates
CAMeeting.sortingMethodOnAddItem = 'on_proposing_groups'
CAMeeting.transitionsToConfirm = []
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
AGMeeting.usedMeetingAttributes = ('place', 'observations', 'signatures', 'assembly', 'startDate', 'endDate',)
AGMeeting.recordMeetingHistoryStates = []
AGMeeting.itemWorkflow = 'meetingitemcaidea_workflow'
AGMeeting.meetingWorkflow = 'meetingcaidea_workflow'
AGMeeting.itemConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowConditions'
AGMeeting.itemActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowActions'
AGMeeting.meetingConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowConditions'
AGMeeting.meetingActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowActions'
#show every items states
AGMeeting.itemTopicStates = ('itemcreated', 'proposedToDepartmentHead', 'proposedToDirector', 'proposedToSecretariat',
                             'validated', 'presented', 'validated_by_cd', 'itemfrozen', 'accepted', 'refused',
                             'delayed', 'pre_accepted', 'removed',)
AGMeeting.meetingTopicStates = ('created', 'validated_by_cd', 'frozen')
AGMeeting.decisionTopicStates = ('decided', 'closed')
AGMeeting.itemAdviceStates = ('itemcreated',)
AGMeeting.itemAdviceEditStates = ('itemcreated',)
AGMeeting.recordItemHistoryStates = ['', ]
AGMeeting.maxShownMeetings = 5
AGMeeting.maxDaysDecisions = 60
AGMeeting.meetingAppDefaultView = 'topic_searchmyitems'
AGMeeting.itemDocFormats = ('odt', 'pdf')
AGMeeting.meetingDocFormats = ('odt', 'pdf')
AGMeeting.useAdvices = True
AGMeeting.enforceAdviceMandatoriness = False
AGMeeting.enableAdviceInvalidation = False
AGMeeting.useCopies = True
AGMeeting.selectableCopyGroups = []
AGMeeting.podTemplates = allTemplates
AGMeeting.transitionsToConfirm = []
AGMeeting.sortingMethodOnAddItem = 'on_proposing_groups'
AGMeeting.useGroupsAsCategories = True

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances', meetingConfigs=(CAMeeting, AGMeeting), groups= [])
data.unoEnabledPython = '/usr/bin/python'
data.usedColorSystem = 'state_color'
# ------------------------------------------------------------------------------
