# -*- coding: utf-8 -*-
#
# File: testChangeItemOrderView.py
#
# Copyright (c) 2013 by Imio.be
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

from Products.MeetingIDEA.tests.MeetingIDEATestCase import MeetingIDEATestCase
from Products.MeetingCommunes.tests.testChangeItemOrderView import testChangeItemOrderView as mctciov

from AccessControl import Unauthorized


class testChangeItemOrderView(MeetingIDEATestCase, mctciov):
    '''Tests the ChangeItemOrderView class methods.'''

    def test_subproduct_call_MayChangeItemOrder(self):
        '''Check docstring in PloneMeeting.'''
        self._mayChangeItemOrder()

    def _mayChangeItemOrder(self):
        """
          The item order can be changed until Meeting.mayChangeItemsOrder is False
        """
        # create a meetingWithItems and play
        self.changeUser('pmManager')
        meeting = self._createMeetingWithItems()
        item = meeting.getItemsInOrder()[0]
        view = item.restrictedTraverse('@@change_item_order')
        self.assertTrue(meeting.wfConditions().mayChangeItemsOrder())
        view('down')
        if 'publish' in self.transitions(meeting):
            self.do(meeting, 'publish')
            self.assertTrue(meeting.wfConditions().mayChangeItemsOrder())
            view('down')
        self.do(meeting, 'validateByCD')
        self.do(meeting, 'freeze')
        self.assertTrue(meeting.wfConditions().mayChangeItemsOrder())
        view('down')
        # add decision to items so meeting can be decided
        for item in meeting.getItems():
            item.setDecision('<p>Dummy decision</p>')
            item.reindexObject(idxs=['getDecision', ])
        # items order is changeable until the meeting is in a closed state
        for tr in self._getTransitionsToCloseAMeeting():
            if tr in self.transitions(meeting):
                self.do(meeting, tr)
                # order still changeable
                if not meeting.queryState() in meeting.meetingClosedStates:
                    self.assertTrue(meeting.wfConditions().mayChangeItemsOrder())
                else:
                    # if the meeting is in a closed state, order is no more changeable
                    self.assertFalse(meeting.wfConditions().mayChangeItemsOrder())
                    # if mayChangeItemsOrder is False, trying to change
                    # order will raise an Unauthorized
                    self.assertRaises(Unauthorized, view, 'up')

    def test_subproduct_call_MoveLateItemDoNotChangeNormalItems(self):
        '''Check docstring in PloneMeeting.'''
        self.test_pm_MoveLateItemDoNotChangeNormalItems()

    def test_pm_MoveLateItemDoNotChangeNormalItems(self):
        """
          Normal items are moved between them and late items also.
        """
        # create a meetingWithItems and play
        self.changeUser('pmManager')
        meeting = self._createMeetingWithItems()
        for item in meeting.getItems():
            item.setDecision('<p>Dummy decision</p>')
        # freeze the meeting to be able to add late items
        if 'publish' in self.transitions(meeting):
            self.do(meeting, 'publish')
        self.do(meeting, 'validateByCD')
        self.do(meeting, 'freeze')
        # create 4 items that will be late
        late1 = self.create('MeetingItem')
        late1.setPreferredMeeting(meeting.UID())
        late1.reindexObject()
        late2 = self.create('MeetingItem')
        late2.setPreferredMeeting(meeting.UID())
        late2.setTitle('i2')
        late2.reindexObject()
        late3 = self.create('MeetingItem')
        late3.setPreferredMeeting(meeting.UID())
        late3.setTitle('i3')
        late3.reindexObject()
        late4 = self.create('MeetingItem')
        late4.setPreferredMeeting(meeting.UID())
        late4.setTitle('i3')
        late4.reindexObject()
        # present the items
        for item in (late1, late2, late3, late4):
            self.presentItem(item)
        item1 = meeting.getItemsInOrder()[0]
        item2 = meeting.getItemsInOrder()[1]
        item3 = meeting.getItemsInOrder()[2]
        item4 = meeting.getItemsInOrder()[3]
        # normal and late items manage their own order
        self.assertEquals(item1.getItemNumber(), 1)
        self.assertEquals(item2.getItemNumber(), 2)
        self.assertEquals(item3.getItemNumber(), 3)
        self.assertEquals(item4.getItemNumber(), 4)
        self.assertEquals(late1.getItemNumber(), 1)
        self.assertEquals(late2.getItemNumber(), 2)
        self.assertEquals(late3.getItemNumber(), 3)
        self.assertEquals(late4.getItemNumber(), 4)
        # move a late item and check that normal items are not changed
        view = late2.restrictedTraverse('@@change_item_order')
        view('up')
        # late2 position changed but not normal items
        self.assertEquals(item1.getItemNumber(), 1)
        self.assertEquals(item2.getItemNumber(), 2)
        self.assertEquals(item3.getItemNumber(), 3)
        self.assertEquals(item4.getItemNumber(), 4)
        self.assertEquals(late1.getItemNumber(), 2)
        self.assertEquals(late2.getItemNumber(), 1)
        self.assertEquals(late3.getItemNumber(), 3)
        self.assertEquals(late4.getItemNumber(), 4)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testChangeItemOrderView, prefix='test_subproduct_'))
    return suite
