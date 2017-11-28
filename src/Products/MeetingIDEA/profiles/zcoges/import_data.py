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
cgppMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'validateByCD',
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
cgppMeeting.recurringItems = [
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
cgpartMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'validateByCD',
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
cgpartMeeting.recurringItems = [
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
cgpartMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(cgppMeeting, cgpartMeeting),
                                 groups=[])
data.enableUserPreferences = False

# ------------------------------------------------------------------------------
