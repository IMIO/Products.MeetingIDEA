member = context.portal_membership.getAuthenticatedMember()
groups = context.portal_groups.getGroupsForPrincipal(member)

#check if the user is at least in one of the following sub group

reviewSuffixes =  ('_reviewers', '_director', '_sectorheads')

strgroups = str(groups)

isReviewer = False
for reviewSuffix in reviewSuffixes:
    if reviewSuffix in strgroups:
        isReviewer = True
        break
return isReviewer

