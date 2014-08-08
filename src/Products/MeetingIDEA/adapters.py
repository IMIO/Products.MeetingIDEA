# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Copyright (c) 2013 by Imio
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
from DateTime import DateTime
from appy.gen import No
from zope.i18n import translate
from AccessControl import getSecurityManager, ClassSecurityInfo
from Globals import InitializeClass
from zope.interface import implements

from Products.CMFCore.permissions import ReviewPortalContent
from Products.CMFCore.utils import getToolByName
from Products.PloneMeeting.MeetingItem import MeetingItem, MeetingItemWorkflowConditions, MeetingItemWorkflowActions
from Products.PloneMeeting.utils import checkPermission, getCurrentMeetingObject
from Products.PloneMeeting.Meeting import MeetingWorkflowActions, MeetingWorkflowConditions, Meeting
from Products.PloneMeeting.interfaces import IMeetingCustom, IMeetingItemCustom, \
    IMeetingConfigCustom, IToolPloneMeetingCustom
from Products.MeetingIDEA.interfaces import \
    IMeetingItemCAIDEAWorkflowConditions, IMeetingItemCAIDEAWorkflowActions,\
    IMeetingCAIDEAWorkflowConditions, IMeetingCAIDEAWorkflowActions
from zope.annotation.interfaces import IAnnotations
from Products.PloneMeeting.model import adaptations
from Products.PloneMeeting.model.adaptations import *
from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.ToolPloneMeeting import ToolPloneMeeting
from Products.PloneMeeting import PloneMeetingError
from Products.PloneMeeting.config import ITEM_NO_PREFERRED_MEETING_VALUE

# Names of available workflow adaptations.
customWfAdaptations = ('return_to_proposing_group', )
MeetingConfig.wfAdaptations = customWfAdaptations
# configure parameters for the returned_to_proposing_group wfAdaptation
# we keep also 'itemfrozen' and 'itempublished' in case this should be activated for meeting-config-college...
RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES = ('presented', 'validated_by_cd', 'itemfrozen', )
adaptations.RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES = RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES
RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS = {
    # view permissions
    'Access contents information':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingDepartmentHead', 'MeetingDirector',
     'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'View':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingDepartmentHead', 'MeetingDirector',
     'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'PloneMeeting: Read decision':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingDepartmentHead', 'MeetingDirector',
     'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'PloneMeeting: Read optional advisers':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingDepartmentHead', 'MeetingDirector',
     'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'PloneMeeting: Read decision annex':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingDepartmentHead', 'MeetingDirector',
     'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'PloneMeeting: Read item observations':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingDepartmentHead', 'MeetingDirector',
     'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'PloneMeeting: Read budget infos':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingDepartmentHead', 'MeetingDirector',
     'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    # edit permissions
    'Modify portal content':
    ('Manager', 'MeetingMember', 'MeetingDepartmentHead', 'MeetingDirector', 'MeetingReviewer', 'MeetingManager', ),
    'PloneMeeting: Write decision':
    ('Manager', 'MeetingMember', 'MeetingDepartmentHead', 'MeetingDirector', 'MeetingReviewer', 'MeetingManager', ),
    'Review portal content':
    ('Manager', 'MeetingMember', 'MeetingDepartmentHead', 'MeetingDirector', 'MeetingReviewer', 'MeetingManager', ),
    'Add portal content':
    ('Manager', 'MeetingMember', 'MeetingDepartmentHead', 'MeetingDirector', 'MeetingReviewer', 'MeetingManager', ),
    'PloneMeeting: Add annex':
    ('Manager', 'MeetingMember', 'MeetingDepartmentHead', 'MeetingDirector', 'MeetingReviewer', 'MeetingManager', ),
    'PloneMeeting: Add MeetingFile':
    ('Manager', 'MeetingMember', 'MeetingDepartmentHead', 'MeetingDirector', 'MeetingReviewer', 'MeetingManager', ),
    'PloneMeeting: Write decision annex':
    ('Manager', 'MeetingMember', 'MeetingDepartmentHead', 'MeetingDirector', 'MeetingReviewer', 'MeetingManager', ),
    'PloneMeeting: Write optional advisers':
    ('Manager', 'MeetingMember', 'MeetingDepartmentHead', 'MeetingDirector', 'MeetingReviewer', 'MeetingManager', ),
    'PloneMeeting: Write optional advisers':
    ('Manager', 'MeetingMember', 'MeetingDepartmentHead', 'MeetingDirector', 'MeetingReviewer', 'MeetingManager', ),
    'PloneMeeting: Write budget infos':
    ('Manager', 'MeetingMember', 'MeetingOfficeManager', 'MeetingManager', 'MeetingBudgetImpactEditor', ),
    # MeetingManagers edit permissions
    'Delete objects':
    ['Manager', 'MeetingManager', ],
    'PloneMeeting: Write item observations':
    ('Manager', 'MeetingManager', ),
}

adaptations.RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS = RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS


class CustomMeeting(Meeting):
    '''Adapter that adapts a meeting implementing IMeeting to the
       interface IMeetingCustom.'''

    implements(IMeetingCustom)
    security = ClassSecurityInfo()

    def __init__(self, meeting):
        self.context = meeting

    # Implements here methods that will be used by templates
    security.declarePublic('getPrintableItems')
    def getPrintableItems(self, itemUids, late=False, ignore_review_states=[],
                          privacy='*', oralQuestion='both', toDiscuss='both', categories=[],
                          excludedCategories=[], firstNumber=1, renumber=False):
        '''Returns a list of items.
           An extra list of review states to ignore can be defined.
           A privacy can also be given, and the fact that the item is an
           oralQuestion or not (or both). Idem with toDiscuss.
           Some specific categories can be given or some categories to exchude.
           These 2 parameters are exclusive.  If renumber is True, a list of tuple
           will be return with first element the number and second element, the item.
           In this case, the firstNumber value can be used.'''
        # We just filter ignore_review_states here and privacy and call
        # getItemsInOrder(uids), passing the correct uids and removing empty
        # uids.
        # privacy can be '*' or 'public' or 'secret'
        # oralQuestion can be 'both' or False or True
        # toDiscuss can be 'both' or 'False' or 'True'
        ann = IAnnotations(self.context.REQUEST)
        for elt in itemUids:
            if elt == '':
                itemUids.remove(elt)
        #no filtering, return the items ordered
        if not categories and not ignore_review_states and privacy == '*' and \
           oralQuestion == 'both' and toDiscuss == 'both':
            if 'printableItems' not in ann:
                ann['printableItems'] = self.context.getItemsInOrder(late=late, uids=itemUids)
            return ann['printableItems']
        # Either, we will have to filter the state here and check privacy
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
            elif excludedCategories and obj.getCategory() in excludedCategories:
                continue
            filteredItemUids.append(itemUid)
        #in case we do not have anything, we return an empty list
        if not filteredItemUids:
            return []
        else:
            if 'printableItems' not in ann:
                ann['printableItems'] = self.context.getItemsInOrder(late=late, uids=filteredItemUids)
            items = ann['printableItems']
            if renumber:
                #return a list of tuple with first element the number and second
                #element the item itself
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
                        categoryList.insert(i+1, [meetingGroup, item])
                    else:
                        categoryList.insert(i+1, [meetingGroup])
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
                categoryList[groupIndex+1].append(item)

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
                    #no empty service, we want only show department
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

    security.declarePublic('getAvailableItems')
    def getAvailableItems(self):
        '''Items are available to the meeting no matter the meeting state (except 'closed').
           In the 'created' state, every validated items are availble, in other states, only items
           for wich the specific meeting is selected as preferred will appear.'''
        meeting = self.getSelf()
        if meeting.queryState() not in ('created', 'validated_by_cd', 'frozen', 'decided'):
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
        if meeting.queryState() in ('validated_by_cd', 'frozen', 'decided'):
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
        #no filtering, return the items ordered
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
                    #first value of the list is the category object
                    res[catNum][0] = item.getCategory(True)
                    #second value of the list is a list of items
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
                    k = k+1
                    ressorti1.append([res[i][1][j], k])
                ressorti.append(ressorti1)
                ressort.append(ressorti)
        return ressort

    security.declarePublic('getPreviousMeeting')
    def getPreviousMeeting(self, searchMeetingsInterval=60):
        '''Gets the previous meeting based on meeting date. We only search among
           meetings in the previous p_searchMeetingsInterval, which is a number
           of days. If no meeting is found, the method returns None.'''
        meetingDate = self.context.getDate()
        tool = getToolByName(self.context, 'portal_plonemeeting')
        meetingConfig = tool.getMeetingConfig(
            self.context)
        meetingTypeName = meetingConfig.getMeetingTypeName()
        catalog = getToolByName(self.context, 'portal_catalog')
        allMeetings = catalog(
            portal_type=meetingTypeName,
            getDate={'query': self.context.getDate()-searchMeetingsInterval,
                     'range': 'min'},
            sort_on='getDate', sort_order='reverse')
        res = None
        for meeting in allMeetings:
            if (meeting.getObject().getDate() < meetingDate):
                res = meeting
                break
        if res:
            res = res.getObject()
        return res

    security.declarePublic('showItemAdvices')
    def showItemAdvices(self):
        '''See doc in interfaces.py.'''
        return True

    security.declarePublic('showAllItemsAtOnce')
    def showAllItemsAtOnce(self):
        """
          Monkeypatch for hiding the allItemsAtOnce field
        """
        return False
    Meeting.showAllItemsAtOnce = showAllItemsAtOnce

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
        #suppress paragraph
        assembly = self.context.getAssembly().replace('<p>', '').replace('</p>', '')
        #supress M., MM.
        assembly = re.sub(r"M{1,2}[.]", "", assembly)
        #suppress Mmes, Mme
        assembly = re.sub(r"Mmes*.?", "", assembly)
        assembly = assembly.split('<br />')
        res = []
        status = 0
        for ass in assembly:
            ass = ass.split(',')
            for a in ass:
                #retrieve blank and pass empty lines
                a = a.strip()
                if not a:
                    continue
                #a line "Excusé:" is used for define list of persons who are excused
                if a.find('xcus') >= 0:
                    status = 1
                    continue
                #a line "Absents:" is used for define list of persons who are absentee
                if a.upper().find('ABSENT') >= 0:
                    status = 2
                    continue
                #a line "Procurations:" is used for defined list of persons who recieve a procuration
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
        #suppress paragraph
        assembly = self.context.getAssembly().replace('<p>', '').replace('</p>', '')
        assembly = assembly.split('<br />')
        res = []
        status = 'present'
        for ass in assembly:
            #ass line "Excusé:" is used for define list of persons who are excused
            if ass.find('xcus') >= 0:
                status = 'excused'
                continue
            #ass line "Procurations:" is used for defined list of persons who recieve a procuration
            if ass.upper().find('PROCURATION') >= 0:
                status = 'procuration'
                continue
            #ass line "Absents:" is used for define list of persons who are excused
            if ass.upper().find('ABSENT') >= 0:
                status = 'absentee'
                continue
            if filter == '*' or status == filter:
                res.append(ass)
        return res


class CustomMeetingItem(MeetingItem):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCustom.'''
    implements(IMeetingItemCustom)
    security = ClassSecurityInfo()

    customItemPositiveDecidedStates = ('accepted', 'accepted_but_modified', )
    MeetingItem.itemPositiveDecidedStates = customItemPositiveDecidedStates

    customBeforePublicationStates = ('itemcreated', 'proposed_to_departmenthead', 'proposed_to_director',
                                     'proposed_to_secretariat', 'validated', )
    MeetingItem.customBeforePublicationStates = customBeforePublicationStates

    customMeetingNotClosedStates = ('validated_by_cd', 'frozen', 'decided', )
    MeetingItem.meetingNotClosedStates = customMeetingNotClosedStates

    customMeetingTransitionsAcceptingRecurringItems = ('_init_', 'validateByCD', 'freeze', 'decide')
    MeetingItem.meetingTransitionsAcceptingRecurringItems = customMeetingTransitionsAcceptingRecurringItems

    #this list is used by doPresent defined in PloneMeeting
    customMeetingAlreadyFrozenStates = ('validated_by_cd', 'frozen', 'decided', )
    MeetingItem.meetingAlreadyFrozenStates = customMeetingAlreadyFrozenStates

    def __init__(self, item):
        self.context = item

    security.declarePublic('getMeetingsAcceptingItems')
    def getMeetingsAcceptingItems(self):
        '''Overrides the default method so we only display meetings that are
           in the 'created' or 'frozen' state.'''
        tool = getToolByName(self.context, 'portal_plonemeeting')
        catalog = getToolByName(self.context, "portal_catalog")
        meetingPortalType = tool.getMeetingConfig(self.context).getMeetingTypeName()
        # If the current user is a meetingManager (or a Manager),
        # he is able to add a meetingitem to a 'decided' meeting.
        review_state = ['created', 'validated_by_cd', 'frozen', ]
        if tool.isManager():
            review_state += ['decided', ]
        res = catalog.unrestrictedSearchResults(
            portal_type=meetingPortalType,
            review_state=review_state,
            sort_on='getDate')
        # Frozen meetings may still accept "late" items.
        return res

    security.declarePublic('mayBeLinkedToTasks')
    def mayBeLinkedToTasks(self):
        '''See doc in interfaces.py.'''
        item = self.getSelf()
        res = False
        if (item.queryState() in ('accepted', 'refused', 'delayed')):
            res = True
        return res

    security.declarePublic('getIcons')
    def getIcons(self, inMeeting, meeting):
        '''Check docstring in PloneMeeting interfaces.py.'''
        item = self.getSelf()
        # Default PM item icons
        res = MeetingItem.getIcons(item, inMeeting, meeting)
        # Add our icons for accepted_but_modified and pre_accepted
        itemState = item.queryState()
        if itemState == 'accepted_but_modified':
            res.append(('accepted_but_modified.png', 'accepted_but_modified'))
        elif itemState == 'pre_accepted':
            res.append(('pre_accepted.png', 'pre_accepted'))
        elif itemState == 'proposed_to_departmenthead':
            res.append(('proposeToDepartmentHead.png', 'proposed_to_DepartmentHead'))
        elif itemState == 'proposed_to_director':
            res.append(('proposeToDirector.png', 'proposed_to_director'))
        elif itemState == 'proposed_to_secretariat':
            res.append(('proposeToSecretariat.png', 'proposed_to_secretariat'))
        return res


class CustomMeetingConfig(MeetingConfig):
    '''Adapter that adapts a meetingConfig implementing IMeetingConfig to the
       interface IMeetingConfigCustom.'''

    implements(IMeetingConfigCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    #we need to be able to give an advice in the initial_state
    from Products.PloneMeeting.MeetingConfig import MeetingConfig
    MeetingConfig.listItemStatesInitExcepted = MeetingConfig.listItemStates

    security.declarePublic('searchItemsToValidate')
    def searchItemsToValidate(self, sortKey, sortOrder, filterKey, filterValue, **kwargs):
        '''See docstring in Products.PloneMeeting.MeetingConfig.
           We override it here because relevant groupIds and wf state are no the same...'''
        member = self.portal_membership.getAuthenticatedMember()
        groupIds = self.portal_groups.getGroupsForPrincipal(member)
        res = []
        for groupId in groupIds:
            if groupId.endswith('_reviewers'):
                res.append(groupId[:-10])

        params = {'portal_type': self.getItemTypeName(),
                  'getProposingGroup': res,
                  'review_state': 'proposed_to_secretariat',
                  'sort_on': sortKey,
                  'sort_order': sortOrder
                  }
        # Manage filter
        if filterKey:
            params[filterKey] = prepareSearchValue(filterValue)
        # update params with kwargs
        params.update(kwargs)
        # Perform the query in portal_catalog
        return self.portal_catalog(**params)
    MeetingConfig.searchItemsToValidate = searchItemsToValidate


# ------------------------------------------------------------------------------
class MeetingCAIDEAWorkflowActions(MeetingWorkflowActions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCAWorkflowActions'''

    implements(IMeetingCAIDEAWorkflowActions)
    security = ClassSecurityInfo()

    def _adaptEveryItemsOnMeetingClosure(self):
        """Helper method for accepting every items."""
        # Every item that is not decided will be automatically set to "accepted"
        wfTool = getToolByName(self.context, 'portal_workflow')
        for item in self.context.getAllItems():
            if item.queryState() == 'presented':
                wfTool.doActionFor(item, 'itemValidateByCD')
            if item.queryState() == 'validated_by_cd':
                wfTool.doActionFor(item, 'itemfreeze')
            if item.queryState() in ['itemfrozen', 'pre_accepted', ]:
                wfTool.doActionFor(item, 'accept')

    security.declarePrivate('doDecide')
    def doDecide(self, stateChange):
        '''We pass every item that is 'presented' in the 'itemfrozen'
           state.  It is the case for late items.'''
        for item in self.context.getAllItems(ordered=False):
            if item.queryState() == 'presented':
                self.context.portal_workflow.doActionFor(item, 'itemValidateByCD')
            if item.queryState() == 'validated_by_cd':
                self.context.portal_workflow.doActionFor(item, 'itemfreeze')

    security.declarePrivate('doFreeze')
    def doFreeze(self, stateChange):
        '''When freezing the meeting, every items must be automatically set to
           "itemfrozen".'''
        for item in self.context.getAllItems(ordered=True):
            if item.queryState() == 'presented':
                self.context.portal_workflow.doActionFor(item, 'itemValidateByCD')
            if item.queryState() == 'validated_by_cd':
                self.context.portal_workflow.doActionFor(item, 'itemfreeze')

    security.declarePrivate('doBackToCreated')
    def doBackToCreated(self, stateChange):
        '''When a meeting go back to the "created" state, for example the
           meeting manager wants to add an item, we do not do anything.'''
        pass

    security.declarePrivate('doValidateByCD')
    def doValidateByCD(self, stateChange):
        for item in self.context.getAllItems(ordered=True):
            if item.queryState() == 'presented':
                self.context.portal_workflow.doActionFor(item, 'itemValidateByCD')
        #manage meeting number
        self.initSequenceNumber()

    security.declarePrivate('doBackToValidatedByCD')
    def doBackToValidatedByCD(self, stateChange):
        pass


# ------------------------------------------------------------------------------
class MeetingCAIDEAWorkflowConditions(MeetingWorkflowConditions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCAWorkflowConditions'''

    implements(IMeetingCAIDEAWorkflowConditions)
    security = ClassSecurityInfo()

    def __init__(self, meeting):
        self.context = meeting
        customAcceptItemsStates = ('created', 'validated_by_cd', 'frozen', 'decided')
        self.acceptItemsStates = customAcceptItemsStates

    security.declarePublic('mayValidateByCD')
    def mayValidateByCD(self):
        res = False
        if checkPermission(ReviewPortalContent, self.context):
            res = True  # At least at present
            if not self.context.getRawItems():
                res = No(self.context.utranslate('item_required_to_publish'))
        return res

    security.declarePublic('mayFreeze')
    def mayFreeze(self):
        res = False
        if checkPermission(ReviewPortalContent, self.context):
            res = True  # At least at present
            if not self.context.getRawItems():
                res = No(translate('item_required_to_publish', domain='PloneMeeting', context=self.context.REQUEST))
        return res

    security.declarePublic('mayClose')
    def mayClose(self):
        res = False
        # The user just needs the "Review portal content" permission on the
        # object to close it.
        if checkPermission(ReviewPortalContent, self.context):
            res = True
        return res

    security.declarePublic('mayDecide')
    def mayDecide(self):
        res = False
        if checkPermission(ReviewPortalContent, self.context) and \
           (not self._allItemsAreDelayed()):
            res = True
        return res


# ------------------------------------------------------------------------------
class MeetingItemCAIDEAWorkflowActions(MeetingItemWorkflowActions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCAWorkflowActions'''

    implements(IMeetingItemCAIDEAWorkflowActions)
    security = ClassSecurityInfo()

    security.declarePrivate('doAccept_but_modify')
    def doAccept_but_modify(self, stateChange):
        pass

    security.declarePrivate('doPre_accept')
    def doPre_accept(self, stateChange):
        pass

    security.declarePrivate('doDelay')
    def doDelay(self, stateChange):
        '''When an item is delayed, we will duplicate it: the copy is back to
           the initial state and will be linked to this one.
           After, we replace decision for initial items if needed'''
        DECISION_ERROR = 'There was an error in the TAL expression for defining the ' \
            'decision when an item is reported. Please check this in your meeting config. ' \
            'Original exception: %s'
        # call PloneMeeting's doDelay then make our additional things
        MeetingItemWorkflowActions.doDelay(self, stateChange)
        # manage itemDecisionReportText
        tool = getToolByName(self.context, 'portal_plonemeeting')
        meetingConfig = tool.getMeetingConfig(self.context)
        itemDecisionReportText = meetingConfig.getRawItemDecisionReportText()
        if itemDecisionReportText.strip():
            from Products.CMFCore.Expression import Expression, createExprContext
            portal_url = getToolByName(self.context, 'portal_url')
            portal = portal_url.getPortalObject()
            ctx = createExprContext(self.context.getParentNode(), portal, self.context)
            try:
                res = Expression(itemDecisionReportText)(ctx)
            except Exception, e:
                self.context.plone_utils.addPortalMessage(PloneMeetingError(DECISION_ERROR % str(e)))
                return
            self.context.setDecision(res)

    security.declarePrivate('doRemove')
    def doRemove(self, stateChange):
        pass

    security.declarePrivate('doProposeToDepartmentHead')
    def doProposeToDepartmentHead(self, stateChange):
        pass

    security.declarePrivate('doProposeToDirector')
    def doProposeToDirector(self, stateChange):
        pass

    security.declarePrivate('doProposeToSecretariat')
    def doProposeToSecretariat(self, stateChange):
        pass

    security.declarePrivate('doItemValidateByCD')
    def doItemValidateByCD(self, stateChange):
        pass

    security.declarePrivate('doPresent')
    def doPresent(self, stateChange, forceNormal=False):
        '''Presents an item into a meeting. If p_forceNormal is True, and the
           item should be inserted as a late item, it is nevertheless inserted
           as a normal item.'''
        meeting = getCurrentMeetingObject(self.context)
        meeting.insertItem(self.context, forceNormal=forceNormal)
        # If the meeting is already frozen and this item is a "late" item,
        # I must set automatically the item to "itemfrozen".
        meetingState = meeting.queryState()
        wTool = self.context.portal_workflow
        if meetingState in self.context.meetingAlreadyFrozenStates:
            try:
                wTool.doActionFor(self.context, 'itempublish')
            except:
                pass  # Maybe does state 'itempublish' not exist.
            wTool.doActionFor(self.context, 'itemValidateByCD')
            if meetingState == "frozen":
                wTool.doActionFor(self.context, 'itemfreeze')
        # We may have to send a mail.
        self.context.sendMailIfRelevant('itemPresented', 'Owner', isRole=True)


# ------------------------------------------------------------------------------
class MeetingItemCAIDEAWorkflowConditions(MeetingItemWorkflowConditions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCAWorkflowConditions'''

    implements(IMeetingItemCAIDEAWorkflowConditions)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item  # Implements IMeetingItem
        self.sm = getSecurityManager()
        self.useHardcodedTransitionsForPresentingAnItem = True
        self.transitionsForPresentingAnItem = ('proposeToDepartmentHead', 'proposeToDirector', 'proposeToSecretariat',
                                               'validate', 'present')

    security.declarePublic('mayDelete')
    def mayDelete(self):
        '''
          By default it is not possible to delete an item if some
          decision annexes exist.  Here we do not care about this...
        '''
        return True

    security.declarePublic('mayDecide')
    def mayDecide(self):
        '''We may decide an item if the linked meeting is in relevant state.'''
        res = False
        meeting = self.context.getMeeting()
        if checkPermission(ReviewPortalContent, self.context) and \
           meeting and (meeting.queryState() in ['decided', 'closed', 'decisions_published', ]):
            res = True
        return res

    security.declarePublic('isLateFor')
    def isLateFor(self, meeting):
        res = False
        if meeting and (meeting.queryState() in MeetingItem.meetingAlreadyFrozenStates) and \
           (meeting.UID() == self.context.getPreferredMeeting()):
            itemValidationDate = self._getDateOfAction(self.context, 'validate')
            meetingFreezingDate = self._getDateOfAction(meeting, 'validateByCD')
            if itemValidationDate and meetingFreezingDate:
                if itemValidationDate > meetingFreezingDate:
                    res = True
        return res

    security.declarePublic('mayValidate')
    def mayValidate(self):
        """
          Either the alderman or the MeetingManager can validate
          The MeetingManager can bypass the validation process and validate an item
          that is in the state 'itemcreated'
        """
        res = False
        #first of all, the use must have the 'Review portal content permission'
        if checkPermission(ReviewPortalContent, self.context):
            res = True
            #if the current item state is 'itemcreated', only the MeetingManager can validate
            member = self.context.portal_membership.getAuthenticatedMember()
            if self.context.queryState() in ('itemcreated',) and not \
               (member.has_role('MeetingManager') or member.has_role('Manager')):
                res = False
        return res

    security.declarePublic('mayFreeze')
    def mayFreeze(self):
        res = False
        if checkPermission(ReviewPortalContent, self.context):
            if self.context.hasMeeting() and \
               (self.context.getMeeting().queryState() in ('frozen', 'decided', 'closed', 'decisions_published', )):
                res = True
        return res

    security.declarePublic('mayCorrect')
    def mayCorrect(self):
        # Check with the default PloneMeeting method and our test if res is
        # False. The diffence here is when we correct an item from itemfrozen to
        # presented, we have to check if the Meeting is in the "created" state
        # and not "published".
        res = MeetingItemWorkflowConditions.mayCorrect(self)
        # Manage our own behaviour now when the item is linked to a meeting,
        # a MeetingManager can correct anything except if the meeting is closed
        if not res is True:
            if checkPermission(ReviewPortalContent, self.context):
                # Get the meeting
                meeting = self.context.getMeeting()
                if meeting:
                    # Meeting can be None if there was a wf problem leading
                    # an item to be in a "presented" state with no linked
                    # meeting.
                    meetingState = meeting.queryState()
                    # A user having ReviewPortalContent permission can correct
                    # an item in any case except if the meeting is closed.
                    if meetingState != 'closed':
                        res = True
                else:
                    res = True
        return res

    security.declarePublic('mayProposeToDepartmentHead')
    def mayProposeToDepartmentHead(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToDirector')
    def mayProposeToDirector(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToSecretariat')
    def mayProposeToSecretariat(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if checkPermission(ReviewPortalContent, self.context):
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
        if checkPermission(ReviewPortalContent, self.context) and \
           meeting and (meeting.queryState() in ['decided', 'closed']):
            res = True
        return res

    security.declarePublic('mayValidateByCD')
    def mayValidateByCD(self):
        res = False
        if checkPermission(ReviewPortalContent, self.context):
            return True
        return res


class CustomToolPloneMeeting(ToolPloneMeeting):
    '''Adapter that adapts a tool implementing ToolPloneMeeting to the
       interface IToolPloneMeetingCustom'''

    implements(IToolPloneMeetingCustom)
    security = ClassSecurityInfo()

    security.declarePublic('getSpecificAssemblyFor')
    def getSpecificAssemblyFor(self, assembly, startTxt=''):
        ''' Return the Assembly between two tag.
            This method is use in template
        '''
        #Pierre Dupont - Bourgmestre,
        #Charles Exemple - 1er Echevin,
        #Echevin Un, Echevin Deux excusé, Echevin Trois - Echevins,
        #Jacqueline Exemple, Responsable du CPAS
        #Absentes:
        #Mademoiselle x
        #Excusés:
        #Monsieur Y, Madame Z
        res = []
        tmp = ['<p class="mltAssembly">']
        splitted_assembly = assembly.replace('<p>', '').replace('</p>', '').split('<br />')
        start_text = startTxt == ''
        for assembly_line in splitted_assembly:
            assembly_line = assembly_line.strip()
            #check if this line correspond to startTxt (in this cas, we can begin treatment)
            if not start_text:
                start_text = assembly_line.startswith(startTxt)
                if start_text:
                    #when starting treatment, add tag (not use if startTxt=='')
                    res.append(assembly_line)
                continue
            #check if we must stop treatment...
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

# ------------------------------------------------------------------------------
InitializeClass(CustomMeeting)
InitializeClass(CustomMeetingItem)
InitializeClass(MeetingCAIDEAWorkflowActions)
InitializeClass(MeetingCAIDEAWorkflowConditions)
InitializeClass(MeetingItemCAIDEAWorkflowActions)
InitializeClass(MeetingItemCAIDEAWorkflowConditions)
InitializeClass(CustomToolPloneMeeting)
# ------------------------------------------------------------------------------
