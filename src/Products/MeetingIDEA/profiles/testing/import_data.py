# -*- coding: utf-8 -*-

from copy import deepcopy
from Products.PloneMeeting.profiles.testing import import_data as pm_import_data
from Products.MeetingCommunes.profiles.testing import import_data as mc_import_data
from Products.PloneMeeting.config import MEETINGREVIEWERS
from Products.PloneMeeting.profiles import UserDescriptor

data = deepcopy(mc_import_data.data)

# Users and groups -------------------------------------------------------------
pmManager = UserDescriptor('pmManager', [], email="pmmanager@plonemeeting.org", fullname='M. PMManager')
pmCreator1 = UserDescriptor('pmCreator1', [], email="pmcreator1@plonemeeting.org", fullname='M. PMCreator One')
pmCreator1b = UserDescriptor('pmCreator1b', [], email="pmcreator1b@plonemeeting.org", fullname='M. PMCreator One bee')
pmObserver1 = UserDescriptor('pmObserver1', [], email="pmobserver1@plonemeeting.org", fullname='M. PMObserver One')
pmReviewer1 = UserDescriptor('pmReviewer1', [])
pmReviewerLevel1 = UserDescriptor('pmReviewerLevel1', [],
                                  email="pmreviewerlevel1@plonemeeting.org", fullname='M. PMReviewer Level One')
pmCreator2 = UserDescriptor('pmCreator2', [])
pmReviewer2 = UserDescriptor('pmReviewer2', [])
pmReviewerLevel2 = UserDescriptor('pmReviewerLevel2', [],
                                  email="pmreviewerlevel2@plonemeeting.org", fullname='M. PMReviewer Level Two')
pmAdviser1 = UserDescriptor('pmAdviser1', [])
pmDepartmentHead1 = UserDescriptor('pmDepartmentHead1', [])
pmDirector1 = UserDescriptor('pmDirector1', [])
pmDirector2 = UserDescriptor('pmDirector2', [])
powerobserver1 = UserDescriptor('powerobserver1',
                                [],
                                email="powerobserver1@plonemeeting.org",
                                fullname='M. Power Observer1')

# Inherited users
pmReviewer1 = deepcopy(pm_import_data.pmReviewer1)
pmReviewer2 = deepcopy(pm_import_data.pmReviewer2)
pmReviewerLevel1 = deepcopy(pm_import_data.pmReviewerLevel1)
pmReviewerLevel2 = deepcopy(pm_import_data.pmReviewerLevel2)
pmManager = deepcopy(pm_import_data.pmManager)


developers = data.orgs[0]
developers.creators.append(pmCreator1)
developers.creators.append(pmCreator1b)
developers.creators.append(pmManager)
developers.observers.append(pmObserver1)
developers.observers.append(pmReviewer1)
developers.observers.append(pmManager)
developers.advisers.append(pmAdviser1)
developers.advisers.append(pmManager)
developers.departmentheads.append(pmDepartmentHead1)
developers.departmentheads.append(pmManager)
developers.reviewers.append(pmReviewer1)
developers.reviewers.append(pmDirector1)
developers.reviewers.append(pmManager)
# reviewers

setattr(developers, 'signatures', 'developers signatures')
setattr(developers, 'echevinServices', 'developers')
# put pmReviewerLevel1 in first level of reviewers from what is in MEETINGREVIEWERS
getattr(developers, MEETINGREVIEWERS.keys()[-1]).append(pmReviewerLevel1)
# put pmReviewerLevel2 in second level of reviewers from what is in MEETINGREVIEWERS
getattr(developers, MEETINGREVIEWERS.keys()[0]).append(pmReviewerLevel2)

# give an advice on recurring items
vendors = data.orgs[1]
vendors.creators.append(pmCreator2)
vendors.reviewers.append(pmReviewer2)
vendors.observers.append(pmReviewer2)
vendors.advisers.append(pmReviewer2)
vendors.advisers.append(pmManager)
setattr(vendors, 'signatures', '')

# Meeting configurations -------------------------------------------------------
# college
caMeeting = deepcopy(mc_import_data.collegeMeeting)
caMeeting.itemWorkflow = 'meetingitemcaidea_workflow'
caMeeting.meetingWorkflow = 'meetingcaidea_workflow'
caMeeting.itemConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowConditions'
caMeeting.itemActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowActions'
caMeeting.meetingConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowConditions'
caMeeting.meetingActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowActions'
caMeeting.transitionsToConfirm = []
caMeeting.transitionsForPresentingAnItem = ['proposeToDepartmentHead', 'proposeToDirector', 'validate', 'present', ]
caMeeting.onMeetingTransitionItemTransitionToTrigger = (
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
caMeeting.workflowAdaptations = ['return_to_proposing_group']

# Conseil communal
agMeeting = deepcopy(mc_import_data.councilMeeting)
agMeeting.itemWorkflow = 'meetingitemcaidea_workflow'
agMeeting.meetingWorkflow = 'meetingcaidea_workflow'
agMeeting.itemConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowConditions'
agMeeting.itemActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowActions'
agMeeting.meetingConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowConditions'
agMeeting.meetingActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowActions'
agMeeting.transitionsToConfirm = []
agMeeting.transitionsForPresentingAnItem = ['proposeToDepartmentHead', 'proposeToDirector', 'validate', 'present', ]
agMeeting.onMeetingTransitionItemTransitionToTrigger = (
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
agMeeting.workflowAdaptations = ['return_to_proposing_group']

data.meetingConfigs = (caMeeting, agMeeting)
