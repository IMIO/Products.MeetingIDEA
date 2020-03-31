# -*- coding: utf-8 -*-
#
# File: testWorkflows.py
#
# Copyright (c) 2007-2010 by PloneGov
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

from DateTime import DateTime
from Products.CMFCore.permissions import View
from Products.MeetingIDEA.tests.MeetingIDEATestCase import MeetingIDEATestCase
from Products.MeetingCommunes.tests.testWorkflows import testWorkflows as mctw
from Products.PloneMeeting.config import EXECUTE_EXPR_VALUE


class testWorkflows(MeetingIDEATestCase, mctw):
    """Tests the default workflows implemented in MeetingIDEA.

       WARNING:
       The Plone test system seems to be bugged: it does not seem to take into
       account the write_permission and read_permission tags that are defined
       on some attributes of the Archetypes model. So when we need to check
       that a user is not authorized to set the value of a field protected
       in this way, we do not try to use the accessor to trigger an exception
       (self.assertRaise). Instead, we check that the user has the permission
       to do so (getSecurityManager().checkPermission)."""

    def test_pm_WholeDecisionProcess(self):
        """Bypass this test..."""
        pass

    def test_pm_WorkflowPermissions(self):
        """Bypass this test..."""
        pass

    def test_pm_RecurringItems(self):
        """Bypass this test..."""
        pass

    def test_pm_MeetingExecuteActionOnLinkedItemsGiveAccessToAcceptedItemsOfAMeetingToPowerAdvisers(self):
        '''Test the MeetingConfig.onMeetingTransitionItemActionToExecute parameter :
           specific usecase, being able to give access to decided items of a meeting only when meeting
           is closed, even if item is decided before the meeting is closed.'''
        self.changeUser('siteadmin')
        cfg = self.meetingConfig
        cfg.setMeetingManagerMayCorrectClosedMeeting(True)
        # call updateLocalRoles on item only if it not already decided
        # as updateLocalRoles is called when item review_state changed
        self.assertTrue('accepted' in cfg.getItemDecidedStates())
        cfg.setOnMeetingTransitionItemActionToExecute(
            [{'meeting_transition': 'decide',
              'item_action': 'itempublish',
              'tal_expression': ''},
             {'meeting_transition': 'decide',
              'item_action': 'itemfreeze',
              'tal_expression': ''},

             {'meeting_transition': 'close',
              'item_action': 'itempublish',
              'tal_expression': ''},
             {'meeting_transition': 'close',
              'item_action': 'itemfreeze',
              'tal_expression': ''},
             {'meeting_transition': 'close',
              'item_action': EXECUTE_EXPR_VALUE,
              'tal_expression': 'python: item.queryState() in cfg.getItemDecidedStates() and '
                'item.updateLocalRoles()'},
             {'meeting_transition': 'close',
              'item_action': 'accept',
              'tal_expression': ''},
             {'meeting_transition': 'backToDecided',
              'item_action': EXECUTE_EXPR_VALUE,
              'tal_expression': 'python: item.updateLocalRoles()'},
             ])
        # configure access of powerobservers only access if meeting is 'closed'
        cfg.setPowerObservers([
            {'item_access_on': 'python: item.getMeeting().queryState() == "closed"',
             'item_states': ['accepted'],
             'label': 'Power observers',
             'meeting_access_on': '',
             'meeting_states': ['closed'],
             'row_id': 'powerobservers'}])
        self.changeUser('pmManager')
        item1 = self.create('MeetingItem')
        item1.setDecision(self.decisionText)
        item2 = self.create('MeetingItem', decision=self.decisionText)
        item2.setDecision(self.decisionText)
        meeting = self.create('Meeting', date=DateTime('2019/09/10'))
        self.presentItem(item1)
        self.presentItem(item2)
        self.decideMeeting(meeting)
        self.do(item1, 'accept')
        self.assertEqual(item1.queryState(), 'accepted')
        # power observer does not have access to item1/item2
        self.changeUser('powerobserver1')
        self.assertFalse(self.hasPermission(View, item1))
        self.assertFalse(self.hasPermission(View, item2))
        self.changeUser('pmManager')
        self.decideMeeting(meeting)
        self.do(meeting, 'publish')
        # make sure we close as a MeetingManager
        # this test that meetingExecuteActionOnLinkedItems execute TAL exprs as 'Manager'
        self.do(meeting, 'close')
        # items are accepted
        self.assertEqual(item1.queryState(), 'accepted')
        self.assertEqual(item2.queryState(), 'accepted')
        # and powerobserver has also access to item1 that was already accepted before meeting was closed
        self.changeUser('powerobserver1')
        self.assertTrue(self.hasPermission(View, item1))
        self.assertTrue(self.hasPermission(View, item2))
        # when meeting set back to decided, items are no more viewable
        self.changeUser('pmManager')
        self.do(meeting, 'backToPublished')
        self.do(meeting, 'backToDecided')
        self.changeUser('powerobserver1')
        self.assertFalse(self.hasPermission(View, item1))
        self.assertFalse(self.hasPermission(View, item2))
        # and closed again
        self.changeUser('pmManager')
        self.do(meeting, 'publish')
        self.do(meeting, 'close')
        self.changeUser('powerobserver1')
        self.assertTrue(self.hasPermission(View, item1))
        self.assertTrue(self.hasPermission(View, item2))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testWorkflows, prefix='test_pm_'))
    return suite