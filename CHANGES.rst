Products.MeetingIDEA Changelog
==================================

Older versions than 3.0 can be found at http://svn.communesplone.org/svn/communesplone/MeetingIDEA/tags/
The Products.MeetingIDEA version must be the same as the Products.PloneMeeting version

4.1.8 (unreleased)
------------------

- Nothing changed yet.


4.1.7 (2020-08-21)
------------------

- Adapted templates regarding last changes in Products.PloneMeeting.
  [gbastien]


4.1.6 (2020-06-24)
------------------

- Fixed guards so groupsInCharge field is required (if applicable) to make a WF transition.


4.1.5 (2020-06-16)
------------------

- Removed AG profile because it was unecessary and renamed correctly executive_office profile
- Fixed issue in performCustomWFAdaptations where 'refused' may no be in item WF
- Updated meetingitem_view.pt

4.1.4 (2020-06-11)
------------------
- Added 2 profiles (BE and AG) to MeetingIDEA.

4.1.3 (2020-05-28)
------------------
- Fix metadata in setup.py.

4.1.3 (2020-05-28)
------------------

- Fix metadata in setup.py.


4.1.2 (2020-05-28)
------------------
- Using MeetingCommunes
- Compatible for PloneMeeting 4.1

4.0.1 (2017)
------------
- Compatible for PloneMeeting 4.0.1

3.3 (2015-02-27)
----------------
- Updated regarding changes in PloneMeeting
- Removed profile 'examples' that loaded examples in english
- Removed dependencies already defined in PloneMeeting's setup.py
- Added parameter MeetingConfig.initItemDecisionIfEmptyOnDecide that let enable/disable
  items decision field initialization when meeting 'decide' transition is triggered
- Field 'MeetingGroup.signatures' was moved to PloneMeeting

3.2.0 (2015-01-01)
------------------
- Updated regarding changes in PloneMeeting
- Use getToolByName where necessary

3.1.0 (2013-11-04)
------------------
- Simplified overrides now that PloneMeeting manage this correctly
- Moved 'add_published_state' to PloneMeeting and renamed to 'hide_decisions_when_under_writing'
- Moved 'searchitemstovalidate' topic to PloneMeeting now that PloneMeeting also manage a 'searchitemstoprevalidate' search

3.0.3 (2013-08-19)
------------------
- Added method getNumberOfItems usefull in pod templates
- Adapted regarding changes about "less roles" from PloneMeeting
- Added "demo data" profile
- Refactored tests regarding changes in PloneMeeting

3.0.2 (2013-06-21)
------------------
- Removed override of Meeting.mayChangeItemsOrder
- Removed override of meeting_changeitemsorder
- Removed override of browser.async.Discuss.isAsynchToggleEnabled, now enabled by default
- Added missing tests from PloneMeeting
- Corrected bug in printAdvicesInfos leading to UnicodeDecodeError when no advice was asked on an item

3.0.1 (2013-06-07)
------------------
- Added sample of document template with printed annexes
- Added method to ease pritning of assembly with 'category' of assembly members
- Make printing by category as functionnal as printing without category
- Corrected bug while going back to published that could raise a WorkflowException sometimes

3.0 (2013-04-03)
----------------
- Migrated to Plone 4 (use PloneMeeting 3.x, see PloneMeeting's HISTORY.txt for full changes list)

2.1.3 (2012-09-19)
------------------
- Added possibility to give, modify and view an advice on created item
- Added possibility to define a decision of replacement when an item is delayed
- Added new workflow adaptation to add publish state with hidden decision for no meeting-manager
