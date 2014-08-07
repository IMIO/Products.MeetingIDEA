# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# Copyright (c) 2014 by Imio
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Andre Nuyens <andre@imio.be>"""
__docformat__ = 'plaintext'


import logging
logger = logging.getLogger('MeetingIDEA: setuphandlers')
from Products.MeetingIDEA.config import PROJECTNAME
from Products.MeetingIDEA.config import DEPENDENCIES
import os
from Products.CMFCore.utils import getToolByName
import transaction
##code-section HEAD
from Products.PloneMeeting.exportimport.content import ToolInitializer
from Products.PloneMeeting.config import TOPIC_TYPE, TOPIC_SEARCH_SCRIPT, TOPIC_TAL_EXPRESSION
##/code-section HEAD

def isNotMeetingIDEAProfile(context):
    return context.readDataFile("MeetingIDEA_marker.txt") is None



def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    if isNotMeetingIDEAProfile(context): return
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()

def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if isNotMeetingIDEAProfile(context):
        return
    logStep("postInstall", context)
    site = context.getSite()
    add_CA_AG_Searches(context, site)
    #need to reinstall PloneMeeting after reinstalling MC workflows to re-apply wfAdaptations
    reinstallPloneMeeting(context, site)
    showHomeTab(context, site)
    reorderSkinsLayers(context, site)



##code-section FOOT
def add_CA_AG_Searches(context, portal):
    '''
       Add additional searches to the 'meeting-config-ag' and 'meeting-config-ca' MeetingConfig
    '''
    if isNotMeetingIDEAProfile(context):
        return

    logStep("add_CA_AG_Searches", context)
    topicsInfo = (
        # Items in state 'proposed_to_departmenthead'
        ('searchdepartmentheaditems', (('Type', 'ATPortalTypeCriterion', 'MeetingItem'),),
        ('proposed_to_departmenthead', ), '', 'python: not here.portal_plonemeeting.userIsAmong("departmenthead")',),
        # Items in state 'proposed_to_director'
        # Used in the "todo" portlet
        ('searchdirectoritems', (('Type', 'ATPortalTypeCriterion', 'MeetingItem'), ),
        ('proposed_to_director', ), '', 'python: here.portal_plonemeeting.userIsAmong("director")',),
        # Items in state 'proposed_to_secretariat
        ('searchsecretariatitems', (('Type', 'ATPortalTypeCriterion', 'MeetingItem'),),
        ('proposed_to_secretariat', ), '', 'python: here.portal_plonemeeting.isManager()',),
        # Items in state 'validated'
        ('searchvalidateditems', (('Type', 'ATPortalTypeCriterion', 'MeetingItem'), ), ('validated', ), '', '',),
        # All 'decided' items
        ('searchdecideditems', (('Type', 'ATPortalTypeCriterion', 'MeetingItem'),),
        ('accepted', 'refused', 'delayed', 'accepted_but_modified'), '', '',), )
    mcs = portal.portal_plonemeeting.objectValues("MeetingConfig")
    if not mcs:
        return

    #Add these searches by meeting config
    for meetingConfig in mcs:
        if not meetingConfig.getId() == 'meeting-config-CA' and not meetingConfig.getId() == 'meeting-config-AG':
            continue
        for topicId, topicCriteria, stateValues, topicSearchScript, topicTalExpr in topicsInfo:
            #if reinstalling, we need to check if the topic does not already exist
            if hasattr(meetingConfig.topics, topicId):
                continue
            meetingConfig.topics.invokeFactory('Topic', topicId)
            topic = getattr(meetingConfig.topics, topicId)
            topic.setExcludeFromNav(True)
            topic.setTitle(topicId)
            for criterionName, criterionType, criterionValue in topicCriteria:
                criterion = topic.addCriterion(field=criterionName, criterion_type=criterionType)
                topic.manage_addProperty(TOPIC_TYPE, criterionValue, 'string')
                criterionValue = '%s%s' % (criterionValue, meetingConfig.getShortName())
                criterion.setValue([criterionValue])

            stateCriterion = topic.addCriterion(field='review_state', criterion_type='ATListCriterion')
            stateCriterion.setValue(stateValues)
            topic.manage_addProperty(TOPIC_SEARCH_SCRIPT, topicSearchScript, 'string')
            topic.manage_addProperty(TOPIC_TAL_EXPRESSION, topicTalExpr, 'string')
            topic.setLimitNumber(True)
            topic.setItemCount(20)
            topic.setSortCriterion('created', True)
            topic.setCustomView(True)
            topic.setCustomViewFields(['Title', 'CreationDate', 'Creator', 'review_state'])
            topic.reindexObject()


def logStep(method, context):
    logger.info("Applying '%s' in profile '%s'" % (method, '/'.join(context._profile_path.split(os.sep)[-3:])))


def istMeetingIDEAConfigureProfile(context):
    return context.readDataFile("MeetingIDEA_idea_marker.txt") or \
        context.readDataFile("MeetingIDEA_test_marker.txt")


def installMeetingIDEA(context):
    """ Run the default profile before bing able to run the IDEA profile"""
    if not istMeetingIDEAConfigureProfile(context):
        return
    logStep("installMeetingIDEA", context)
    portal = context.getSite()
    portal.portal_setup.runAllImportStepsFromProfile('profile-Products.MeetingIDEA:default')


def initializeTool(context):
    '''Initialises the PloneMeeting tool based on information from the current
       profile.'''
    if not istMeetingIDEAConfigureProfile(context):
        return
    logStep("initializeTool", context)
    #PloneMeeting is no more a dependency to avoid
    #magic between quickinstaller and portal_setup
    #so install it manually
    _installPloneMeeting(context)
    return ToolInitializer(context, PROJECTNAME).run()


def reinstallPloneMeeting(context, site):
    '''Reinstall PloneMeeting so after install methods are called and applied,
       like performWorkflowAdaptations for example.'''

    if isNotMeetingIDEAProfile(context):
        return
    logStep("reinstallPloneMeeting", context)
    _installPloneMeeting(context)


def _installPloneMeeting(context):
    site = context.getSite()
    profileId = u'profile-Products.PloneMeeting:default'
    site.portal_setup.runAllImportStepsFromProfile(profileId)


def showHomeTab(context, site):
    """
       Make sure the 'home' tab is shown...
    """
    if isNotMeetingIDEAProfile(context):
        return

    logStep("showHomeTab", context)

    index_html = getattr(site.portal_actions.portal_tabs, 'index_html', None)
    if index_html:
        index_html.visible = True
    else:
        logger.info("The 'Home' tab does not exist !!!")


def reorderSkinsLayers(context, site):
    """
       Reinstall Products.plonemeetingskin and re-apply MeetingIDEA skins.xml step
       as the reinstallation of MeetingIDEA and PloneMeeting changes the portal_skins layers order
    """
    if isNotMeetingIDEAProfile(context) and not istMeetingIDEAConfigureProfile:
        return

    logStep("reorderSkinsLayers", context)
    try:
        site.portal_setup.runImportStepFromProfile(u'profile-Products.MeetingIDEA:default', 'skins')
        site.portal_setup.runAllImportStepsFromProfile(u'profile-plonetheme.imioapps:default')
        site.portal_setup.runAllImportStepsFromProfile(u'profile-plonetheme.imioapps:plonemeetingskin')
    except KeyError:
        # if the Products.MeetingIDEA profile is not available
        # (not using MeetingIDEA or in testing?) we pass...
        pass


def finalizeExampleInstance(context):
    """
       Some parameters can not be handled by the PloneMeeting installation,
       so we handle this here
    """
    if not istMeetingIDEAConfigureProfile(context):
        return

    specialUserId = 'president'
    meetingConfig1Id = 'meeting-config-ca'
    meetingConfig2Id = 'meeting-config-ag'

    site = context.getSite()

    logStep("finalizeExampleInstance", context)
    # add the test user 'president' to every '_powerobservers' groups
    member = site.portal_membership.getMemberById(specialUserId)
    if member:
        site.portal_groups.addPrincipalToGroup(member.getId(), '%s_powerobservers' % meetingConfig1Id)
        site.portal_groups.addPrincipalToGroup(member.getId(), '%s_powerobservers' % meetingConfig2Id)
    # add the test user 'conseiller' to only the every 'meeting-config-council_powerobservers' groups
    member = site.portal_membership.getMemberById('conseiller')
    if member:
        site.portal_groups.addPrincipalToGroup(member.getId(), '%s_powerobservers' % meetingConfig2Id)

    # define some parameters for 'meeting-config-ca'
    # items are sendable to the 'meeting-config-ag'
    mc_ca_or_ag = getattr(site.portal_plonemeeting, meetingConfig1Id)
    mc_ca_or_ag.setMeetingConfigsToCloneTo([meetingConfig2Id, ])
    # add some topcis to the portlet_todo
    mc_ca_or_ag.setToDoListTopics(
        [getattr(mc_ca_or_ag.topics, 'searchdecideditems'),
         getattr(mc_ca_or_ag.topics, 'searchitemstovalidate'),
         getattr(mc_ca_or_ag.topics, 'searchallitemsincopy'),
         getattr(mc_ca_or_ag.topics, 'searchallitemstoadvice'),
         ])
    # call updateCloneToOtherMCActions inter alia
    mc_ca_or_ag.at_post_edit_script()

    # define some parameters for 'meeting-config-council'
    mc_ca_or_ag = getattr(site.portal_plonemeeting, meetingConfig2Id)
    # add some topcis to the portlet_todo
    mc_ca_or_ag.setToDoListTopics(
        [getattr(mc_ca_or_ag.topics, 'searchdecideditems'),
         getattr(mc_ca_or_ag.topics, 'searchitemstovalidate'),
         getattr(mc_ca_or_ag.topics, 'searchallitemsincopy'),
         ])

    # finally, re-launch plonemeetingskin and MeetingIDEA skins step
    # because PM has been installed before the import_data profile and messed up skins layers
    site.portal_setup.runImportStepFromProfile(u'profile-Products.MeetingIDEA:default', 'skins')
    site.portal_setup.runImportStepFromProfile(u'profile-plonetheme.imioapps:default', 'skins')
    site.portal_setup.runImportStepFromProfile(u'profile-plonetheme.imioapps:plonemeetingskin', 'skins')


def reorderCss(context):
    """
       Make sure CSS are correctly reordered in portal_css so things
       work as expected...
    """
    if isNotMeetingIDEAProfile(context) and istMeetingIDEAConfigureProfile:
        return

    site = context.getSite()

    logStep("reorderCss", context)

    portal_css = site.portal_css
    css = ['plonemeeting.css',
           'meeting.css',
           'meetingitem.css',
           'meetingidea.css',
           'imioapps.css',
           'plonemeetingskin.css',
           'imioapps_IEFixes.css',
           'ploneCustom.css']
    for resource in css:
        portal_css.moveResourceToBottom(resource)


def addMeetingCDGroup(context):
    """
      Add a Plone group configured to receive Direction Council
      These users can modify the items in prsented state
      This group recieved the MeetingPowerObserverRôle
    """
    if isNotMeetingIDEAProfile(context):
        return
    logStep("addCDGroup", context)
    portal = context.getSite()
    groupId = "meetingCD"
    if not groupId in portal.portal_groups.listGroupIds():
        portal.portal_groups.addGroup(groupId, title=portal.utranslate("meetingCDGroupTitle", domain='PloneMeeting'))
        portal.portal_groups.setRolesForGroup(groupId, ('MeetingObserverGlobal', 'MeetingCD'))

##/code-section FOOT
