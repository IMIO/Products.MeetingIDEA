# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Copyright (c) 2017 by Imio.be
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
# ------------------------------------------------------------------------------

import re
from collections import OrderedDict

from Products.MeetingIDEA import logger
from Products.MeetingIDEA.interfaces import IMeetingCAIDEAWorkflowActions
from Products.MeetingIDEA.interfaces import IMeetingCAIDEAWorkflowConditions
from Products.MeetingIDEA.interfaces import IMeetingItemCAIDEAWorkflowActions
from Products.MeetingIDEA.interfaces import IMeetingItemCAIDEAWorkflowConditions
from Products.PloneMeeting import PMMessageFactory as _
from Products.PloneMeeting.Meeting import Meeting
from Products.PloneMeeting.Meeting import MeetingWorkflowActions
from Products.PloneMeeting.Meeting import MeetingWorkflowConditions
from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.MeetingItem import MeetingItem
from Products.PloneMeeting.MeetingItem import MeetingItemWorkflowActions
from Products.PloneMeeting.MeetingItem import MeetingItemWorkflowConditions
from Products.PloneMeeting.ToolPloneMeeting import ToolPloneMeeting
from Products.PloneMeeting.config import ITEM_NO_PREFERRED_MEETING_VALUE
from Products.PloneMeeting.interfaces import IMeetingConfigCustom
from Products.PloneMeeting.interfaces import IMeetingCustom
from Products.PloneMeeting.interfaces import IMeetingItemCustom
from Products.PloneMeeting.interfaces import IToolPloneMeetingCustom
from Products.PloneMeeting.model import adaptations
from Products.PloneMeeting.model.adaptations import WF_APPLIED

from AccessControl import ClassSecurityInfo, getSecurityManager
from AccessControl.class_init import InitializeClass
from DateTime import DateTime
from Products.CMFCore.permissions import ReviewPortalContent
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName
from appy.gen import No
from imio.helpers.xhtml import xhtmlContentIsEmpty
from plone import api
from zope.annotation import IAnnotations
from zope.i18n import translate
from zope.interface import implements

# # Names of available workflow adaptations.
# customwfAdaptations = list(MeetingConfig.wfAdaptations)
# # remove the 'creator_initiated_decisions' as this is always the case in our wfs
# if 'creator_initiated_decisions' in customwfAdaptations:
#     customwfAdaptations.remove('creator_initiated_decisions')
# # remove the 'archiving' as we do not handle archive in our wfs
# if 'archiving' in customwfAdaptations:
#     customwfAdaptations.remove('archiving')
#
# MeetingConfig.wfAdaptations = customwfAdaptations

MeetingConfig.wfAdaptations = ['return_to_proposing_group']
# configure parameters for the returned_to_proposing_group wfAdaptation
adaptations.RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES = ('presented', 'itemfrozen',)

RETURN_TO_PROPOSING_GROUP_MAPPINGS = {'backTo_presented_from_returned_to_proposing_group':
                                          ['created'],
                                      'backTo_itemfrozen_from_returned_to_proposing_group':
                                          ['frozen', 'decided', 'published', 'decisions_published', ],
                                      'NO_MORE_RETURNABLE_STATES': ['closed', 'archived', ]
                                      }

adaptations.RETURN_TO_PROPOSING_GROUP_MAPPINGS.update(RETURN_TO_PROPOSING_GROUP_MAPPINGS)

RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS = {'meetingitemcaidea_workflow':
                                                # view permissions
                                                    {'Access contents information':
                                                         ('Manager', 'MeetingManager', 'MeetingMember',
                                                          'MeetingDepartmentHead',
                                                          'MeetingReviewer', 'MeetingObserverLocal', 'Reader',),
                                                     'View':
                                                         ('Manager', 'MeetingManager', 'MeetingMember',
                                                          'MeetingDepartmentHead',
                                                          'MeetingReviewer', 'MeetingObserverLocal', 'Reader',),
                                                     'PloneMeeting: Read decision':
                                                         ('Manager', 'MeetingManager', 'MeetingMember',
                                                          'MeetingDepartmentHead',
                                                          'MeetingReviewer', 'MeetingObserverLocal', 'Reader',),
                                                     'PloneMeeting: Read optional advisers':
                                                         ('Manager', 'MeetingManager', 'MeetingMember',
                                                          'MeetingDepartmentHead',
                                                          'MeetingReviewer', 'MeetingObserverLocal', 'Reader',),
                                                     'PloneMeeting: Read decision annex':
                                                         ('Manager', 'MeetingManager', 'MeetingMember',
                                                          'MeetingDepartmentHead',
                                                          'MeetingReviewer', 'MeetingObserverLocal', 'Reader',),
                                                     'PloneMeeting: Read item observations':
                                                         ('Manager', 'MeetingManager', 'MeetingMember',
                                                          'MeetingDepartmentHead',
                                                          'MeetingReviewer', 'MeetingObserverLocal', 'Reader',),
                                                     'PloneMeeting: Read budget infos':
                                                         ('Manager', 'MeetingManager', 'MeetingMember',
                                                          'MeetingDepartmentHead',
                                                          'MeetingReviewer', 'MeetingObserverLocal', 'Reader',),
                                                     # edit permissions
                                                     'Modify portal content':
                                                         ('Manager', 'MeetingMember', 'MeetingDepartmentHead',
                                                          'MeetingReviewer', 'MeetingManager',),
                                                     'PloneMeeting: Write decision':
                                                         ('Manager', 'MeetingMember', 'MeetingDepartmentHead',
                                                          'MeetingReviewer', 'MeetingManager',),
                                                     'Review portal content':
                                                         ('Manager', 'MeetingMember', 'MeetingDepartmentHead',
                                                          'MeetingReviewer', 'MeetingManager',),
                                                     'Add portal content':
                                                         ('Manager', 'MeetingMember', 'MeetingDepartmentHead',
                                                          'MeetingReviewer', 'MeetingManager',),
                                                     'PloneMeeting: Add annex':
                                                         ('Manager', 'MeetingMember', 'MeetingDepartmentHead',
                                                          'MeetingReviewer', 'MeetingManager',),
                                                     'PloneMeeting: Add annexDecision':
                                                         ('Manager', 'MeetingMember', 'MeetingDepartmentHead',
                                                          'MeetingReviewer', 'MeetingManager',),
                                                     'PloneMeeting: Add MeetingFile':
                                                         ('Manager', 'MeetingMember', 'MeetingDepartmentHead',
                                                          'MeetingReviewer', 'MeetingManager',),
                                                     'PloneMeeting: Write optional advisers':
                                                         ('Manager', 'MeetingMember', 'MeetingDepartmentHead',
                                                          'MeetingReviewer', 'MeetingManager',),
                                                     'PloneMeeting: Write budget infos':
                                                         ('Manager', 'MeetingMember', 'MeetingOfficeManager',
                                                          'MeetingManager', 'MeetingBudgetImpactEditor',),
                                                     'PloneMeeting: Write marginal notes':
                                                         ('Manager', 'MeetingManager',),
                                                     # MeetingManagers edit permissions
                                                     'Delete objects':
                                                         ['Manager', 'MeetingManager', ],
                                                     'PloneMeeting: Write item observations':
                                                         ('Manager', 'MeetingManager',),
                                                     'PloneMeeting: Write item MeetingManager reserved fields':
                                                         ('Manager', 'MeetingManager',),
                                                     }
                                                }

adaptations.RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS = RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS

RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE = {'meetingitemcaidea_workflow': 'meetingitemcaidea_workflow.itemcreated', }
adaptations.RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE = RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE


class CustomMeeting(Meeting):
    """Adapter that adapts a meeting implementing IMeeting to the
       interface IMeetingCustom."""

    implements(IMeetingCustom)
    security = ClassSecurityInfo()

    def __init__(self, meeting):
        self.context = meeting

    # Implements here methods that will be used by templates
    security.declarePublic('getPrintableItems')

    def getPrintableItems(self, itemUids, listTypes=['normal'], ignore_review_states=[],
                          privacy='*', oralQuestion='both', toDiscuss='both', categories=[],
                          excludedCategories=[], groupIds=[], excludedGroupIds=[],
                          firstNumber=1, renumber=False):
        '''Returns a list of items.
           An extra list of review states to ignore can be defined.
           A privacy can also be given, and the fact that the item is an
           oralQuestion or not (or both). Idem with toDiscuss.
           Some specific categories can be given or some categories to exclude.
           We can also receive in p_groupIds MeetingGroup ids to take into account.
           These 2 parameters are exclusive.  If renumber is True, a list of tuple
           will be return with first element the number and second element, the item.
           In this case, the firstNumber value can be used.'''
        # We just filter ignore_review_states here and privacy and call
        # getItems(uids), passing the correct uids and removing empty uids.
        # privacy can be '*' or 'public' or 'secret' or 'public_heading' or 'secret_heading'
        # oralQuestion can be 'both' or False or True
        # toDiscuss can be 'both' or 'False' or 'True'
        for elt in itemUids:
            if elt == '':
                itemUids.remove(elt)

        # check filters
        filteredItemUids = []
        uid_catalog = self.context.uid_catalog
        for itemUid in itemUids:
            obj = uid_catalog(UID=itemUid)[0].getObject()
            if obj.queryState() in ignore_review_states:
                continue
            elif not (privacy == '*' or obj.getPrivacy() == privacy):
                continue
            elif not (oralQuestion == 'both' or obj.getOralQuestion() == oralQuestion):
                continue
            elif not (toDiscuss == 'both' or obj.getToDiscuss() == toDiscuss):
                continue
            elif categories and not obj.getCategory() in categories:
                continue
            elif groupIds and not obj.getProposingGroup() in groupIds:
                continue
            elif excludedCategories and obj.getCategory() in excludedCategories:
                continue
            elif excludedGroupIds and obj.getProposingGroup() in excludedGroupIds:
                continue
            filteredItemUids.append(itemUid)
        # in case we do not have anything, we return an empty list
        if not filteredItemUids:
            return []
        else:
            items = self.context.getItems(uids=filteredItemUids, listTypes=listTypes, ordered=True)
            if renumber:
                # return a list of tuple with first element the number and second
                # element the item itself
                i = firstNumber
                res = []
                for item in items:
                    res.append((i, item))
                    i = i + 1
                items = res
            return items

    def _getAcronymPrefix(self, group, groupPrefixes):
        '''This method returns the prefix of the p_group's acronym among all
           prefixes listed in p_groupPrefixes. If group acronym does not have a
           prefix listed in groupPrefixes, this method returns None.'''
        res = None
        groupAcronym = group.getAcronym()
        for prefix in groupPrefixes.iterkeys():
            if groupAcronym.startswith(prefix):
                res = prefix
                break
        return res

    def _getGroupIndex(self, group, groups, groupPrefixes):
        '''Is p_group among the list of p_groups? If p_group is not among
           p_groups but another group having the same prefix as p_group
           (the list of prefixes is given by p_groupPrefixes), we must conclude
           that p_group is among p_groups. res is -1 if p_group is not
           among p_group; else, the method returns the index of p_group in
           p_groups.'''
        prefix = self._getAcronymPrefix(group, groupPrefixes)
        if not prefix:
            if group not in groups:
                return -1
            else:
                return groups.index(group)
        else:
            for gp in groups:
                if gp.getAcronym().startswith(prefix):
                    return groups.index(gp)
            return -1

    def _insertGroupInCategory(self, categoryList, meetingGroup, groupPrefixes, groups, item=None):
        '''Inserts a group list corresponding to p_meetingGroup in the given
           p_categoryList, following meeting group order as defined in the
           main configuration (groups from the config are in p_groups).
           If p_item is specified, the item is appended to the group list.'''
        usedGroups = [g[0] for g in categoryList[1:]]
        groupIndex = self._getGroupIndex(meetingGroup, usedGroups, groupPrefixes)
        if groupIndex == -1:
            # Insert the group among used groups at the right place.
            groupInserted = False
            i = -1
            for usedGroup in usedGroups:
                i += 1
                if groups.index(meetingGroup) < groups.index(usedGroup):
                    if item:
                        categoryList.insert(i + 1, [meetingGroup, item])
                    else:
                        categoryList.insert(i + 1, [meetingGroup])
                    groupInserted = True
                    break
            if not groupInserted:
                if item:
                    categoryList.append([meetingGroup, item])
                else:
                    categoryList.append([meetingGroup])
        else:
            # Insert the item into the existing group.
            if item:
                categoryList[groupIndex + 1].append(item)

    def _insertItemInCategory(self, categoryList, item, byProposingGroup, groupPrefixes, groups):
        '''This method is used by the next one for inserting an item into the
           list of all items of a given category. if p_byProposingGroup is True,
           we must add it in a sub-list containing items of a given proposing
           group. Else, we simply append it to p_category.'''
        if not byProposingGroup:
            categoryList.append(item)
        else:
            group = item.getProposingGroup(True)
            self._insertGroupInCategory(categoryList, group, groupPrefixes, groups, item)

    security.declarePublic('getPrintableItemsByCategory')

    def getPrintableItemsByCategory(self, itemUids=[], late=False,
                                          ignore_review_states=[], by_proposing_group=False, group_prefixes={},
                                          oralQuestion='both', toDiscuss='both', excludeCategories=[],
                                          includeEmptyCategories=False, includeEmptyDepartment=False,
                                          includeEmptyGroups=False):
        '''Returns a list of (late-)items (depending on p_late) ordered by
           category. Items being in a state whose name is in
           p_ignore_review_state will not be included in the result.
           If p_by_proposing_group is True, items are grouped by proposing group
           within every category. In this case, specifying p_group_prefixes will
           allow to consider all groups whose acronym starts with a prefix from
           this param prefix as a unique group. p_group_prefixes is a dict whose
           keys are prefixes and whose values are names of the logical big
           groups. A toDiscuss and oralQuestion can also be given, the item is a
           toDiscuss (oralQuestion) or not (or both) item.
           If p_includeEmptyCategories is True, categories for which no
           item is defined are included nevertheless. If p_includeEmptyGroups
           is True, proposing groups for which no item is defined are included
           nevertheless.'''
        # The result is a list of lists, where every inner list contains:
        # - at position 0: the category object (MeetingCategory or MeetingGroup)
        # - at position 1 to n: the items in this category
        # If by_proposing_group is True, the structure is more complex.
        # oralQuestion can be 'both' or False or True
        # toDiscuss can be 'both' or 'False' or 'True'
        # Every inner list contains:
        # - at position 0: the category object
        # - at positions 1 to n: inner lists that contain:
        #   * at position 0: the proposing group object
        #   * at positions 1 to n: the items belonging to this group.
        ann = IAnnotations(self.context.REQUEST)
        if not late:
            printableItems = 'printableItems'
            printableItemsByCat = 'printableItemsByCategory'
        else:
            printableItems = 'printableLateItems'
            printableItemsByCat = 'printableItemsLateByCategory'
        if printableItemsByCat in ann:
            return ann[printableItemsByCat]
        if 'activeGroupes' not in ann:
            ann['activeGroupes'] = self.context.portal_plonemeeting.getMeetingGroups()
        res = []
        items = []
        previousCatId = None
        # Retrieve the list of items
        for elt in itemUids:
            if elt == '':
                itemUids.remove(elt)
        if printableItems not in ann:
            ann[printableItems] = self.context.getItemsInOrder(late=late, uids=itemUids)
        items = ann[printableItems]
        if by_proposing_group:
            groups = ann['activeGroupes']
        else:
            groups = None

        if items:
            for item in items:
                # Check if the review_state has to be taken into account
                if item.queryState() in ignore_review_states:
                    continue
                elif excludeCategories != [] and item.getProposingGroup() in excludeCategories:
                    continue
                elif not (oralQuestion == 'both' or item.getOralQuestion() == oralQuestion):
                    continue
                elif not (toDiscuss == 'both' or item.getToDiscuss() == toDiscuss):
                    continue
                currentCat = item.getCategory(theObject=True)
                currentCatId = currentCat.getId()
                if currentCatId != previousCatId:
                    # Add the item to a new category, excepted if the
                    # category already exists.
                    catExists = False
                    for catList in res:
                        if catList[0] == currentCat:
                            catExists = True
                            break
                    if catExists:
                        self._insertItemInCategory(catList, item, by_proposing_group, group_prefixes, groups)
                    else:
                        res.append([currentCat])
                        self._insertItemInCategory(res[-1], item, by_proposing_group, group_prefixes, groups)
                    previousCatId = currentCatId
                else:
                    # Append the item to the same category
                    self._insertItemInCategory(res[-1], item, by_proposing_group, group_prefixes, groups)
        if includeEmptyCategories:
            meetingConfig = self.context.portal_plonemeeting.getMeetingConfig(
                self.context)
            allCategories = meetingConfig.getCategories()
            usedCategories = [elem[0] for elem in res]
            for cat in allCategories:
                if cat not in usedCategories:
                    # no empty service, we want only show department
                    if cat.getAcronym().find('-') > 0:
                        continue
                    elif not includeEmptyDepartment:
                        dpt_empty = True
                        for uc in usedCategories:
                            if uc.getAcronym().startswith(cat.getAcronym()):
                                dpt_empty = False
                                break
                        if dpt_empty:
                            continue
                            # Insert the category among used categories at the right place.
                    categoryInserted = False
                    for i in range(len(usedCategories)):
                        try:
                            if allCategories.index(cat) < \
                                    allCategories.index(usedCategories[i]):
                                usedCategories.insert(i, cat)
                                res.insert(i, [cat])
                                categoryInserted = True
                                break
                        except:
                            continue
                    if not categoryInserted:
                        usedCategories.append(cat)
                        res.append([cat])
        if by_proposing_group and includeEmptyGroups:
            # Include, in every category list, not already used groups.
            # But first, compute "macro-groups": we will put one group for
            # every existing macro-group.
            macroGroups = []  # Contains only 1 group of every "macro-group"
            consumedPrefixes = []
            for group in groups:
                prefix = self._getAcronymPrefix(group, group_prefixes)
                if not prefix:
                    group._v_printableName = group.Title()
                    macroGroups.append(group)
                else:
                    if prefix not in consumedPrefixes:
                        consumedPrefixes.append(prefix)
                        group._v_printableName = group_prefixes[prefix]
                        macroGroups.append(group)
            # Every category must have one group from every macro-group
            for catInfo in res:
                for group in macroGroups:
                    self._insertGroupInCategory(catInfo, group, group_prefixes,
                                                groups)
                    # The method does nothing if the group (or another from the
                    # same macro-group) is already there.
        if printableItemsByCat not in ann:
            ann[printableItemsByCat] = res
        return res

    security.declarePublic('getNumberOfItems')

    def getNumberOfItems(self, itemUids, privacy='*', categories=[], listTypes=['normal']):
        '''Returns the number of items depending on parameters.
           This is used in templates to know how many items of a particular kind exist and
           often used to determine the 'firstNumber' parameter of getPrintableItems/getPrintableItemsByCategory.'''
        # sometimes, some empty elements are inserted in itemUids, remove them...
        itemUids = [itemUid for itemUid in itemUids if itemUid != '']
        if not categories and privacy == '*':
            return len(self.context.getItems(uids=itemUids, listTypes=listTypes))
        # Either, we will have to filter (privacy, categories, late)
        filteredItemUids = []
        uid_catalog = getToolByName(self.context, 'uid_catalog')
        for itemUid in itemUids:
            obj = uid_catalog(UID=itemUid)[0].getObject()
            if not (privacy == '*' or obj.getPrivacy() == privacy):
                continue
            elif not (categories == [] or obj.getCategory() in categories):
                continue
            elif not obj.isLate() == bool(listTypes == ['late']):
                continue
            filteredItemUids.append(itemUid)
        return len(filteredItemUids)

    security.declarePublic('getPrintableItemsByNumCategory')

    def getPrintableItemsByNumCategory(self, listTypes=['normal'], uids=[],
                                       catstoexclude=[], exclude=True, allItems=False):
        '''Returns a list of items ordered by category number. If there are many
           items by category, there is always only one category, even if the
           user have chosen a different order. If exclude=True , catstoexclude
           represents the category number that we don't want to print and if
           exclude=False, catsexclude represents the category number that we
           only want to print. This is useful when we want for exemple to
           exclude a personnal category from the meeting an realize a separate
           meeeting for this personal category. If allItems=True, we return
           late items AND items in order.'''

        def getPrintableNumCategory(current_cat):
            '''Method used here above.'''
            current_cat_id = current_cat.getId()
            current_cat_name = current_cat.Title()
            current_cat_name = current_cat_name[0:2]
            try:
                catNum = int(current_cat_name)
            except ValueError:
                current_cat_name = current_cat_name[0:1]
                try:
                    catNum = int(current_cat_name)
                except ValueError:
                    catNum = current_cat_id
            return catNum

        if not allItems and listTypes == ['late']:
            items = self.context.getItems(uids=uids, listTypes=['late'], ordered=True)
        elif not allItems and not listTypes == ['late']:
            items = self.context.getItems(uids=uids, listTypes=['normal'], ordered=True)
        else:
            items = self.context.getItems(uids=uids, ordered=True)
        # res contains all items by category, the key of res is the category
        # number. Pay attention that the category number is obtain by extracting
        # the 2 first caracters of the categoryname, thus the categoryname must
        # be for exemple ' 2.travaux' or '10.Urbanisme. If not, the catnum takes
        # the value of the id + 1000 to be sure to place those categories at the
        # end.
        res = {}
        # First, we create the category and for each category, we create a
        # dictionary that must contain the list of item in in res[catnum][1]
        for item in items:
            if uids:
                if (item.UID() in uids):
                    inuid = "ok"
                else:
                    inuid = "ko"
            else:
                inuid = "ok"
            if (inuid == "ok"):
                current_cat = item.getCategory(theObject=True)
                catNum = getPrintableNumCategory(current_cat)
                if catNum in res:
                    res[catNum][1][item.getItemNumber()] = item
                else:
                    res[catNum] = {}
                    # first value of the list is the category object
                    res[catNum][0] = item.getCategory(True)
                    # second value of the list is a list of items
                    res[catNum][1] = {}
                    res[catNum][1][item.getItemNumber()] = item

        # Now we must sort the res dictionary with the key (containing catnum)
        # and copy it in the returned array.
        reskey = res.keys()
        reskey.sort()
        ressort = []
        for i in reskey:
            if catstoexclude:
                if (i in catstoexclude):
                    if exclude is False:
                        guard = True
                    else:
                        guard = False
                else:
                    if exclude is False:
                        guard = False
                    else:
                        guard = True
            else:
                guard = True

            if guard is True:
                k = 0
                ressorti = []
                ressorti.append(res[i][0])
                resitemkey = res[i][1].keys()
                resitemkey.sort()
                ressorti1 = []
                for j in resitemkey:
                    k = k + 1
                    ressorti1.append([res[i][1][j], k])
                ressorti.append(ressorti1)
                ressort.append(ressorti)
        return ressort

    security.declarePublic('getAvailableItems')

    def getAvailableItems(self):
        '''Items are available to the meeting no matter the meeting state (except 'closed').
           In the 'created' state, every validated items are availble, in other states, only items
           for wich the specific meeting is selected as preferred will appear.'''
        meeting = self.getSelf()
        if meeting.queryState() not in ('created', 'frozen', 'decided'):
            return []
        meetingConfig = meeting.portal_plonemeeting.getMeetingConfig(meeting)
        # First, get meetings accepting items for which the date is lower or
        # equal to the date of this meeting (self)
        meetings = meeting.portal_catalog(
            portal_type=meetingConfig.getMeetingTypeName(),
            getDate={'query': meeting.getDate(), 'range': 'max'}, )
        meetingUids = [b.getObject().UID() for b in meetings]
        meetingUids.append(ITEM_NO_PREFERRED_MEETING_VALUE)
        # Then, get the items whose preferred meeting is None or is among
        # those meetings.
        itemsUids = meeting.portal_catalog(
            portal_type=meetingConfig.getItemTypeName(),
            review_state='validated',
            getPreferredMeeting=meetingUids,
            sort_on="modified")
        if meeting.queryState() in ('frozen', 'decided'):
            # Oups. I can only take items which are "late" items.
            res = []
            for uid in itemsUids:
                if uid.getObject().wfConditions().isLateFor(meeting):
                    res.append(uid)
        else:
            res = itemsUids
        return res

    security.declarePublic('getNumberOfItems')

    def getNumberOfItems(self, itemUids, privacy='*', categories=[], late=False):
        '''Returns the number of items depending on parameters.
           This is used in templates to know how many items of a particular kind exist and
           often used to determine the 'firstNumber' parameter of getPrintableItems/getPrintableItemsByCategory.'''
        # sometimes, some empty elements are inserted in itemUids, remove them...
        itemUids = [itemUid for itemUid in itemUids if itemUid != '']
        # no filtering, return the items ordered
        if not categories and privacy == '*':
            return len(self.context.getItemsInOrder(late=late, uids=itemUids))
        # Either, we will have to filter (privacy, categories, late)
        filteredItemUids = []
        uid_catalog = getToolByName(self.context, 'uid_catalog')
        for itemUid in itemUids:
            obj = uid_catalog(UID=itemUid)[0].getObject()
            if not (privacy == '*' or obj.getPrivacy() == privacy):
                continue
            elif not (categories == [] or obj.getCategory() in categories):
                continue
            elif not obj.isLate() == late:
                continue
            filteredItemUids.append(itemUid)
        return len(filteredItemUids)

    security.declarePublic('getPrintableItemsByNumCategory')

    def getPrintableItemsByNumCategory(self, late=False, uids=[],
                                       catstoexclude=[], exclude=True, allItems=False):
        '''Returns a list of items ordered by category number. If there are many
           items by category, there is always only one category, even if the
           user have chosen a different order. If exclude=True , catstoexclude
           represents the category number that we don't want to print and if
           exclude=False, catsexclude represents the category number that we
           only want to print. This is useful when we want for exemple to
           exclude a personnal category from the meeting an realize a separate
           meeeting for this personal category. If allItems=True, we return
           late items AND items in order.'''

        def getPrintableNumCategory(current_cat):
            '''Method used here above.'''
            current_cat_id = current_cat.getId()
            current_cat_name = current_cat.Title()
            current_cat_name = current_cat_name[0:2]
            try:
                catNum = int(current_cat_name)
            except ValueError:
                current_cat_name = current_cat_name[0:1]
                try:
                    catNum = int(current_cat_name)
                except ValueError:
                    catNum = current_cat_id
            return catNum

        itemsGetter = self.context.getItems
        if late:
            itemsGetter = self.context.getLateItems
        items = itemsGetter()
        if allItems:
            items = self.context.getItems() + self.context.getLateItems()
        # res contains all items by category, the key of res is the category
        # number. Pay attention that the category number is obtain by extracting
        # the 2 first caracters of the categoryname, thus the categoryname must
        # be for exemple ' 2.travaux' or '10.Urbanisme. If not, the catnum takes
        # the value of the id + 1000 to be sure to place those categories at the
        # end.
        res = {}
        # First, we create the category and for each category, we create a
        # dictionary that must contain the list of item in in res[catnum][1]
        for item in items:
            if uids:
                if (item.UID() in uids):
                    inuid = "ok"
                else:
                    inuid = "ko"
            else:
                inuid = "ok"
            if (inuid == "ok"):
                current_cat = item.getCategory(theObject=True)
                catNum = getPrintableNumCategory(current_cat)
                if catNum in res:
                    res[catNum][1][item.getItemNumber()] = item
                else:
                    res[catNum] = {}
                    # first value of the list is the category object
                    res[catNum][0] = item.getCategory(True)
                    # second value of the list is a list of items
                    res[catNum][1] = {}
                    res[catNum][1][item.getItemNumber()] = item

        # Now we must sort the res dictionary with the key (containing catnum)
        # and copy it in the returned array.
        reskey = res.keys()
        reskey.sort()
        ressort = []
        for i in reskey:
            if catstoexclude:
                if (i in catstoexclude):
                    if exclude is False:
                        guard = True
                    else:
                        guard = False
                else:
                    if exclude is False:
                        guard = False
                    else:
                        guard = True
            else:
                guard = True

            if guard is True:
                k = 0
                ressorti = []
                ressorti.append(res[i][0])
                resitemkey = res[i][1].keys()
                resitemkey.sort()
                ressorti1 = []
                for j in resitemkey:
                    k = k + 1
                    ressorti1.append([res[i][1][j], k])
                ressorti.append(ressorti1)
                ressort.append(ressorti)
        return ressort

    security.declarePrivate('validate_preMeetingDate')

    def validate_preMeetingDate(self, value):
        '''Checks that the preMeetingDate comes before the meeting date.'''
        if not value:
            return
        # Get the meeting date from the request
        try:
            meetingDate = DateTime(self.REQUEST['date'])
        except DateTime.DateError:
            meetingDate = None
        except DateTime.SyntaxError:
            meetingDate = None
        # Compare meeting and pre-meeting dates
        if meetingDate and (DateTime(value) >= meetingDate):
            label = 'pre_date_after_meeting_date'
            return self.utranslate(label, domain='PloneMeeting')

    Meeting.validate_preMeetingDate = validate_preMeetingDate

    security.declarePublic('getPresenceList')

    def getPresenceList(self, filter):
        '''return list of presence in the form of dictionnary
           keys are fullname, status [0=present;1:excused;2=procuration]
           filer on status : 0,1,2 or 3 or * for all
           This method is used on template
        '''
        # suppress paragraph
        assembly = self.context.getAssembly().replace('<p>', '').replace('</p>', '')
        # supress M., MM.
        assembly = re.sub(r"M{1,2}[.]", "", assembly)
        # suppress Mmes, Mme
        assembly = re.sub(r"Mmes*.?", "", assembly)
        assembly = assembly.split('<br />')
        res = []
        status = 0
        for ass in assembly:
            ass = ass.split(',')
            for a in ass:
                # retrieve blank and pass empty lines
                a = a.strip()
                if not a:
                    continue
                # a line "ExcusÃ©:" is used for define list of persons who are excused
                if a.find('xcus') >= 0:
                    status = 1
                    continue
                # a line "Absents:" is used for define list of persons who are absentee
                if a.upper().find('ABSENT') >= 0:
                    status = 2
                    continue
                # a line "Procurations:" is used for defined list of persons who recieve a procuration
                if a.upper().find('PROCURATION') >= 0:
                    status = 3
                    continue
                if filter == '*' or status in filter:
                    res.append({'fullname': a, 'status': status})
        return res

    security.declarePublic('getIdeaAssembly')

    def getIdeaAssembly(self, filter):
        '''return formated assembly
           filer is 'present', 'excused', 'procuration', 'absent' or '*' for all
           This method is used on template
        '''
        # suppress paragraph
        assembly = self.context.getAssembly().replace('<p>', '').replace('</p>', '')
        assembly = assembly.split('<br />')
        res = []
        status = 'present'
        for ass in assembly:
            # ass line "ExcusÃ©:" is used for define list of persons who are excused
            if ass.find('xcus') >= 0:
                status = 'excused'
                continue
            # ass line "Procurations:" is used for defined list of persons who recieve a procuration
            if ass.upper().find('PROCURATION') >= 0:
                status = 'procuration'
                continue
            # ass line "Absents:" is used for define list of persons who are excused
            if ass.upper().find('ABSENT') >= 0:
                status = 'absentee'
                continue
            if filter == '*' or status == filter:
                res.append(ass)
        return res


class CustomMeetingItem(MeetingItem):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCustom."""
    implements(IMeetingItemCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    def _initDecisionFieldIfEmpty(self):
        '''
          If decision field is empty, it will be initialized
          with data coming from title and description.
        '''
        # set keepWithNext to False as it will add a 'class' and so
        # xhtmlContentIsEmpty will never consider it empty...
        if xhtmlContentIsEmpty(self.getDecision(keepWithNext=False)):
            self.setDecision("<p>%s</p>%s" % (self.Title(),
                                              self.Description()))
            self.reindexObject()

    MeetingItem._initDecisionFieldIfEmpty = _initDecisionFieldIfEmpty

    security.declarePublic('getObservations')

    def getObservations(self, **kwargs):
        """Overridden version of 'observations' field accessor.
           Hides the observations for non-managers if meeting state is 'decided'."""
        item = self.getSelf()
        res = item.getField('observations').get(item, **kwargs)
        tool = getToolByName(item, 'portal_plonemeeting')
        if item.hasMeeting() and item.getMeeting().queryState() == 'decided' and not tool.isManager(item):
            return translate('intervention_under_edit',
                             domain='PloneMeeting',
                             context=item.REQUEST,
                             default='<p>The intervention is currently under '
                                     'edit by managers, you can not access it.</p>')
        return res

    MeetingItem.getObservations = getObservations
    MeetingItem.getRawObservations = getObservations

    security.declarePublic('getStrategicAxis')

    def getStrategicAxisView(self, **kwargs):
        """View Strategic Axis Title in page template."""
        item = self.getSelf()
        res = []
        for sa in item.getStrategicAxis():
            res.append(sa.Title())
        res.sort()
        return '<br />'.join(res)

    security.declarePublic('mustShowItemReference')

    def mustShowItemReference(self):
        """See doc in interfaces.py"""
        item = self.getSelf()
        if item.hasMeeting():
            return True

    def getExtraFieldsToCopyWhenCloning(self, cloned_to_same_mc):
        """
          Keep some new fields when item is cloned (to another mc or from itemtemplate).
        """
        res = ['internalCommunication', 'strategicAxis']
        if cloned_to_same_mc:
            res = res + []
        return res


# class CustomMeetingGroup(MeetingGroup):
#     '''Adapter that adapts a meeting group implementing IMeetingGroup to the
#        interface IMeetingGroupCustom.'''
#
#     implements(IMeetingGroupCustom)
#     security = ClassSecurityInfo()
#
#     def __init__(self, item):
#         self.context = item
#
#     security.declarePublic('listEchevinServices')
#
#     def listEchevinServices(self):
#         '''Returns a list of groups that can be selected on an group (without isEchevin).'''
#         res = []
#         tool = getToolByName(self, 'portal_plonemeeting')
#         # Get every Plone group related to a MeetingGroup
#         for group in tool.getMeetingGroups():
#             res.append((group.id, group.getProperty('title')))
#
#         return DisplayList(tuple(res))
#
#     MeetingGroup.listEchevinServices = listEchevinServices


class CustomMeetingConfig(MeetingConfig):
    """Adapter that adapts a meetingConfig implementing IMeetingConfig to the
       interface IMeetingConfigCustom."""

    implements(IMeetingConfigCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    def _extraSearchesInfo(self, infos):
        """Add some specific searches."""
        cfg = self.getSelf()
        itemType = cfg.getItemTypeName()
        extra_infos = OrderedDict(
            [
                # Items in state 'proposed'
                ('searchproposeditems',
                 {
                     'subFolderId': 'searches_items',
                     'active': True,
                     'query':
                         [
                             {'i': 'portal_type',
                              'o': 'plone.app.querystring.operation.selection.is',
                              'v': [itemType, ]},
                             {'i': 'review_state',
                              'o': 'plone.app.querystring.operation.selection.is',
                              'v': ['proposed']}
                         ],
                     'sort_on': u'created',
                     'sort_reversed': True,
                     'showNumberOfItems': False,
                     'tal_condition': "python: not tool.userIsAmong(['reviewers'])",
                     'roles_bypassing_talcondition': ['Manager', ]
                 }
                 ),
                # Items in state 'validated'
                ('searchvalidateditems',
                 {
                     'subFolderId': 'searches_items',
                     'active': True,
                     'query':
                         [
                             {'i': 'portal_type',
                              'o': 'plone.app.querystring.operation.selection.is',
                              'v': [itemType, ]},
                             {'i': 'review_state',
                              'o': 'plone.app.querystring.operation.selection.is',
                              'v': ['validated']}
                         ],
                     'sort_on': u'created',
                     'sort_reversed': True,
                     'showNumberOfItems': False,
                     'tal_condition': "",
                     'roles_bypassing_talcondition': ['Manager', ]
                 }
                 ),
            ]
        )
        infos.update(extra_infos)

        return infos

    def getMeetingsAcceptingItemsAdditionalManagerStates(self):
        """See doc in interfaces.py."""
        return 'created', 'frozen', 'decided'


class MeetingCAIDEAWorkflowActions(MeetingWorkflowActions):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCAIDEAWorkflowActions"""

    implements(IMeetingCAIDEAWorkflowActions)
    security = ClassSecurityInfo()

    security.declarePrivate('doDecide')

    def doDecide(self, stateChange):
        """We pass every item that is 'presented' in the 'itemfrozen'
           state.  It is the case for late items. Moreover, if
           MeetingConfig.initItemDecisionIfEmptyOnDecide is True, we
           initialize the decision field with content of Title+Description
           if decision field is empty."""
        tool = getToolByName(self.context, 'portal_plonemeeting')
        cfg = tool.getMeetingConfig(self.context)
        if cfg.getInitItemDecisionIfEmptyOnDecide():
            for item in self.context.getItems():
                # If deliberation (motivation+decision) is empty,
                # initialize it the decision field
                item._initDecisionFieldIfEmpty()

    security.declarePrivate('doBackToPublished')

    def doBackToPublished(self, stateChange):
        """We do not impact items while going back from decided."""
        pass


class MeetingCAIDEAWorkflowConditions(MeetingWorkflowConditions):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCAIDEAWorkflowConditions"""

    implements(IMeetingCAIDEAWorkflowConditions)
    security = ClassSecurityInfo()

    def __init__(self, meeting):
        self.context = meeting

        customAcceptItemsStates = ('created', 'frozen', 'decided')
        self.acceptItemsStates = customAcceptItemsStates

    security.declarePublic('mayCorrect')

    def mayCorrect(self, destinationState=None):
        '''Override to avoid call to _decisionsWereConfirmed.'''
        if not _checkPermission(ReviewPortalContent, self.context):
            return
        return True

    security.declarePublic('mayDecide')

    def mayDecide(self):
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
        return res


class MeetingItemCAIDEAWorkflowActions(MeetingItemWorkflowActions):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCAIDEAWorkflowActions"""

    implements(IMeetingItemCAIDEAWorkflowActions)
    security = ClassSecurityInfo()

    security.declarePrivate('doAccept_but_modify')

    def doAccept_but_modify(self, stateChange):
        pass

    security.declarePrivate('doPre_accept')

    def doPre_accept(self, stateChange):
        pass

    security.declarePrivate('doRemove')

    def doRemove(self, stateChange):
        pass

    security.declarePrivate('doProposeToDepartmentHead')

    def doProposeToDepartmentHead(self, stateChange):
        pass

    security.declarePrivate('doProposeToDirector')

    def doProposeToDirector(self, stateChange):
        pass


class MeetingItemCAIDEAWorkflowConditions(MeetingItemWorkflowConditions):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCAIDEAWorkflowConditions"""

    implements(IMeetingItemCAIDEAWorkflowConditions)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item  # Implements IMeetingItem
        self.sm = getSecurityManager()
        self.useHardcodedTransitionsForPresentingAnItem = True
        self.transitionsForPresentingAnItem = ('proposeToDepartmentHead', 'proposeToDirector', 'validate', 'present')

    security.declarePublic('mayDecide')

    def mayDecide(self):
        '''We may decide an item if the linked meeting is in relevant state.'''
        res = False
        meeting = self.context.getMeeting()
        if _checkPermission(ReviewPortalContent, self.context) and \
                meeting and meeting.adapted().isDecided():
            res = True
        return res

    def mayValidate(self):
        """
          The MeetingManager can bypass the validation process and validate an item
          that is in the state 'itemcreated'
        """
        res = False
        if not self.context.getCategory():
            return No(translate('required_category_ko',
                                domain="PloneMeeting",
                                context=self.context.REQUEST))
        # first of all, the use must have the 'Review portal content permission'
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
            # if the current item state is 'itemcreated', only the MeetingManager can validate
            if self.context.queryState() in ('itemcreated',) and \
                    not self.context.portal_plonemeeting.isManager(self.context):
                res = False
        return res

    security.declarePublic('mayProposeToDepartmentHead')

    def mayProposeToDepartmentHead(self):
        '''We may propose an item if the workflow permits it and if the
           necessary fields are filled.  In the case an item is transferred from
           another meetingConfig, the category could not be defined.'''
        if not self.context.getCategory():
            return No(_('required_category_ko'))
        if _checkPermission(ReviewPortalContent, self.context):
            return True

    security.declarePublic('mayProposeToDirector')

    def mayProposeToDirector(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
        return res

    security.declarePublic('mayRemove')

    def mayRemove(self):
        """
          We may remove an item if the linked meeting is in the 'decided'
          state.  For now, this is the same behaviour as 'mayDecide'
        """
        res = False
        meeting = self.context.getMeeting()
        if _checkPermission(ReviewPortalContent, self.context) and \
                meeting and (meeting.queryState() in ['decided', 'published', 'closed', 'decisions_published', ]):
            res = True
        return res


class CustomToolPloneMeeting(ToolPloneMeeting):
    '''Adapter that adapts a tool implementing ToolPloneMeeting to the
       interface IToolPloneMeetingCustom'''

    implements(IToolPloneMeetingCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    def isFinancialUser_cachekey(method, self, brain=False):
        '''cachekey method for self.isFinancialUser.'''
        return str(self.context.REQUEST._debug), self.context.REQUEST['AUTHENTICATED_USER']

    def performCustomWFAdaptations(self, meetingConfig, wfAdaptation, logger, itemWorkflow, meetingWorkflow):
        """ """
        if wfAdaptation == 'no_publication':
            # we override the PloneMeeting's 'no_publication' wfAdaptation
            # First, update the meeting workflow
            wf = meetingWorkflow
            # Delete transitions 'publish' and 'backToPublished'
            for tr in ('publish', 'backToPublished'):
                if tr in wf.transitions:
                    wf.transitions.deleteTransitions([tr])
            # Update connections between states and transitions
            wf.states['frozen'].setProperties(
                title='frozen', description='',
                transitions=['backToCreated', 'decide'])
            wf.states['decided'].setProperties(
                title='decided', description='', transitions=['backToFrozen', 'close'])
            # Delete state 'published'
            if 'published' in wf.states:
                wf.states.deleteStates(['published'])
            # Then, update the item workflow.
            wf = itemWorkflow
            # Delete transitions 'itempublish' and 'backToItemPublished'
            for tr in ('itempublish', 'backToItemPublished'):
                if tr in wf.transitions:
                    wf.transitions.deleteTransitions([tr])
            # Update connections between states and transitions
            wf.states['itemfrozen'].setProperties(
                title='itemfrozen', description='',
                transitions=['accept', 'accept_but_modify', 'refuse', 'delay', 'pre_accept', 'backToPresented'])
            for decidedState in ['accepted', 'refused', 'delayed', 'accepted_but_modified']:
                wf.states[decidedState].setProperties(
                    title=decidedState, description='',
                    transitions=['backToItemFrozen', ])
            wf.states['pre_accepted'].setProperties(
                title='pre_accepted', description='',
                transitions=['accept', 'accept_but_modify', 'backToItemFrozen'])
            # Delete state 'published'
            if 'itempublished' in wf.states:
                wf.states.deleteStates(['itempublished'])
            logger.info(WF_APPLIED % ("no_publication", meetingConfig.getId()))
            return True
        return False

    security.declarePublic('getSpecificAssemblyFor')

    def getSpecificAssemblyFor(self, assembly, startTxt=''):
        ''' Return the Assembly between two tag.
            This method is used in templates.
        '''
        # Pierre Dupont - Bourgmestre,
        # Charles Exemple - 1er Echevin,
        # Echevin Un, Echevin Deux excusé, Echevin Trois - Echevins,
        # Jacqueline Exemple, Responsable du CPAS
        # Absentes:
        # Mademoiselle x
        # Excusés:
        # Monsieur Y, Madame Z
        res = []
        tmp = ['<p class="mltAssembly">']
        splitted_assembly = assembly.replace('<p>', '').replace('</p>', '').split('<br />')
        start_text = startTxt == ''
        for assembly_line in splitted_assembly:
            assembly_line = assembly_line.strip()
            # check if this line correspond to startTxt (in this cas, we can begin treatment)
            if not start_text:
                start_text = assembly_line.startswith(startTxt)
                if start_text:
                    # when starting treatment, add tag (not use if startTxt=='')
                    res.append(assembly_line)
                continue
            # check if we must stop treatment...
            if assembly_line.endswith(':'):
                break
            lines = assembly_line.split(',')
            cpt = 1
            my_line = ''
            for line in lines:
                if cpt == len(lines):
                    my_line = "%s%s<br />" % (my_line, line)
                    tmp.append(my_line)
                else:
                    my_line = "%s%s," % (my_line, line)
                cpt = cpt + 1
        if len(tmp) > 1:
            tmp[-1] = tmp[-1].replace('<br />', '')
            tmp.append('</p>')
        else:
            return ''
        res.append(''.join(tmp))
        return res

    def initializeProposingGroupWithGroupInCharge(self):
        """Initialize every items of MeetingConfig for which
           'proposingGroupWithGroupInCharge' is in usedItemAttributes."""
        tool = self.getSelf()
        catalog = api.portal.get_tool('portal_catalog')
        logger.info('Initializing proposingGroupWithGroupInCharge...')
        for cfg in tool.objectValues('MeetingConfig'):
            if 'proposingGroupWithGroupInCharge' in cfg.getUsedItemAttributes():
                brains = catalog(portal_type=cfg.getItemTypeName())
                logger.info('Updating MeetingConfig {0}'.format(cfg.getId()))
                len_brains = len(brains)
                i = 1
                for brain in brains:
                    logger.info('Updating item {0}/{1}'.format(i, len_brains))
                    i = i + 1
                    item = brain.getObject()
                    proposingGroup = item.getProposingGroup(theObject=True)
                    groupsInCharge = proposingGroup.getGroupsInCharge()
                    groupInCharge = groupsInCharge and groupsInCharge[0] or ''
                    value = '{0}__groupincharge__{1}'.format(proposingGroup.getId(),
                                                             groupInCharge)
                    item.setProposingGroupWithGroupInCharge(value)
                    if cfg.getItemGroupInChargeStates():
                        item._updateGroupInChargeLocalRoles()
                        item.reindexObjectSecurity()
                    item.reindexObject(idxs=['getGroupInCharge'])
        logger.info('Done.')


# ------------------------------------------------------------------------------
InitializeClass(CustomMeeting)
InitializeClass(CustomMeetingItem)
InitializeClass(CustomMeetingConfig)
InitializeClass(MeetingCAIDEAWorkflowActions)
InitializeClass(MeetingCAIDEAWorkflowConditions)
InitializeClass(MeetingItemCAIDEAWorkflowActions)
InitializeClass(MeetingItemCAIDEAWorkflowConditions)
InitializeClass(CustomToolPloneMeeting)
