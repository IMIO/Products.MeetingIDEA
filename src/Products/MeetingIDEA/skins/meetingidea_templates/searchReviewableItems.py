## Script (Python) "searchReviewableItems"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=sortKey, sortOrder, topic,batch_size=0
##title=Return a list of items in copy for the current user
##

member = context.portal_membership.getAuthenticatedMember()
groups = context.portal_groups.getGroupsForPrincipal(member)

#the logic is :
#a user is reviewer for his level of hierarchy and every levels below in a group
#so find the different groups (a user could be divisionhead in groupA and director in groupB)
#and find the different states we have to search for this group (proposingGroup of the item)

reviewSuffixes = ('_reviewers', '_director', '_departmentheads')
statesMapping = {
                 '_reviewers': ('proposed_to_departmenthead','proposed_to_director','proposed_to_secretariat','proposed_to_validation_by_director','proposed_to_validation_by_secretariat','proposed_to_general_director'),
                 '_n2': ('proposed_to_departmenthead','proposed_to_director'),
                 '_departmentheads': 'proposed_to_departmenthead',
                }

foundGroups = {}
#check that we have a real PM group, not "echevins", or "Administrators"
for group in groups:
    isOK = False
    for reviewSuffix in reviewSuffixes:
        if group.endswith(reviewSuffix):
            isOK = True
            break
    if not isOK:
        continue
    #remove the suffix
    groupPrefix = '_'.join(group.split('_')[:-1])
    if not groupPrefix in foundGroups:
        foundGroups[groupPrefix] = ''

#now we have the differents services (equal to the MeetingGroup id) the user is in
strgroup = str(groups)
for foundGroup in foundGroups:
    for reviewSuffix in reviewSuffixes:
        if "%s%s" % (foundGroup, reviewSuffix) in str(groups):
            foundGroups[foundGroup] = reviewSuffix
            break

#now we have in the dict foundGroups the group the user is in in the key and the highest level in the value
res=[]
for foundGroup in foundGroups:
    brains = context.portal_catalog(portal_type='MeetingItemCA', getProposingGroup=foundGroup, review_state=statesMapping[foundGroups[foundGroup]])
    res = res+list(brains)

return res

