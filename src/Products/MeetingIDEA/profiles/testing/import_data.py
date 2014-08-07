# -*- coding: utf-8 -*-
from Products.PloneMeeting.profiles import *

# File types -------------------------------------------------------------------

annexe = MeetingFileTypeDescriptor('annexe', 'Annexe', 'attach.png', '')
annexeBudget = MeetingFileTypeDescriptor('annexeBudget', 'Article Budgetaire', 'budget.png', '')
annexeCahier = MeetingFileTypeDescriptor('annexeCahier', 'Cahier des Charges', 'cahier.gif', '')
itemAnnex = MeetingFileTypeDescriptor('item-annex', 'Other annex(es)', 'attach.png', '')
annexeDecision = MeetingFileTypeDescriptor('annexeDecision', 'Annexe a la decision', 'attach.png', '', 'item_decision')
# Some type of annexes taken from the default PloneMeeting test profile
marketingAnalysis = MeetingFileTypeDescriptor(
    'marketing-annex', 'Marketing annex(es)', 'attach.png', '', 'item_decision',
    active=False)
overheadAnalysis = MeetingFileTypeDescriptor(
    'overhead-analysis', 'Administrative overhead analysis',
    'attach.png', '')
# Advice annexes types
adviceAnnex = MeetingFileTypeDescriptor(
    'advice-annex', 'Advice annex(es)', 'attach.png', '', 'advice')
adviceLegalAnalysis = MeetingFileTypeDescriptor(
    'advice-legal-analysis', 'Advice legal analysis', 'attach.png', '', 'advice')


# Pod templates ----------------------------------------------------------------
agendaTemplate = PodTemplateDescriptor('agendaTemplate', 'Meeting agenda')
agendaTemplate.podTemplate = 'Agenda.odt'
agendaTemplate.podCondition = 'python:here.meta_type=="Meeting"'

decisionsTemplate = PodTemplateDescriptor('decisionsTemplate',
                                          'Meeting decisions')
decisionsTemplate.podTemplate = 'Decisions.odt'
decisionsTemplate.podCondition = 'python:here.meta_type=="Meeting" and ' \
                                 'here.adapted().isDecided()'

itemTemplate = PodTemplateDescriptor('itemTemplate', 'Meeting item')
itemTemplate.podTemplate = 'Item.odt'
itemTemplate.podCondition = 'python:here.meta_type=="MeetingItem"'

# Categories -------------------------------------------------------------------
categories = [
    CategoryDescriptor('deployment', 'Deployment topics'),
    CategoryDescriptor('maintenance', 'Maintenance topics'),
    CategoryDescriptor('development', 'Development topics'),
    CategoryDescriptor('events', 'Events'),
    CategoryDescriptor('research', 'Research topics'),
    CategoryDescriptor('projects', 'Projects'),
    # A vintage category
    CategoryDescriptor('marketing', 'Marketing', active=False),
    # usingGroups category
    CategoryDescriptor('subproducts', 'Subproducts wishes', usingGroups=('vendors',)),
]

# Users and groups -------------------------------------------------------------
pmManager = UserDescriptor('pmManager', ['MeetingManager'])
pmCreator1 = UserDescriptor('pmCreator1', [])
pmCreator1b = UserDescriptor('pmCreator1b', [])
pmReviewer1 = UserDescriptor('pmReviewer1', [])
pmCreator2 = UserDescriptor('pmCreator2', [])
pmReviewer2 = UserDescriptor('pmReviewer2', [])
pmAdviser1 = UserDescriptor('pmAdviser1', [])
pmDepartmentHead1 = UserDescriptor('pmDepartmentHead1', [])
pmDirector1 = UserDescriptor('pmDirector1', [])
pmDirector2 = UserDescriptor('pmDirector2', [])
voter1 = UserDescriptor('voter1', [], fullname='M. Voter One')
voter2 = UserDescriptor('voter2', [], fullname='M. Voter Two')
powerobserver1 = UserDescriptor('powerobserver1', [], fullname='M. Power Observer1')
# powerobserver1 is MeetingPowerObserverLocal because in the meetingPma '_powerobservers' group
plonemeeting_assembly_powerobservers = PloneGroupDescriptor('meeting-config-council_powerobservers',
                                                            'meeting-config-council_powerobservers',
                                                            [])
powerobserver1.ploneGroups = [plonemeeting_assembly_powerobservers, ]
powerobserver2 = UserDescriptor('powerobserver2', [], fullname='M. Power Observer2')

developers = GroupDescriptor('developers', 'Developers', 'Devel')
developers.creators.append(pmCreator1)
developers.creators.append(pmCreator1b)
developers.creators.append(pmDepartmentHead1)
developers.creators.append(pmManager)
developers.reviewers.append(pmReviewer1)
developers.reviewers.append(pmManager)
developers.observers.append(pmReviewer1)
developers.observers.append(pmManager)
developers.advisers.append(pmAdviser1)
developers.advisers.append(pmManager)
developers.departmentheads.append(pmDepartmentHead1)
developers.departmentheads.append(pmReviewer1)
developers.departmentheads.append(pmManager)
developers.director.append(pmReviewer1)
developers.director.append(pmDirector1)
developers.director.append(pmManager)
# reviewers

setattr(developers, 'signatures', 'developers signatures')
setattr(developers, 'echevinServices', 'developers')

#give an advice on recurring items
vendors = GroupDescriptor('vendors', 'Vendors', 'Devil')
vendors.creators.append(pmCreator2)
vendors.reviewers.append(pmReviewer2)
vendors.observers.append(pmReviewer2)
vendors.advisers.append(pmReviewer2)
vendors.advisers.append(pmManager)
setattr(vendors, 'signatures', '')

# Do voters able to see items to vote for
developers.observers.append(voter1)
developers.observers.append(voter2)
vendors.observers.append(voter1)
vendors.observers.append(voter2)
# Add a vintage group
endUsers = GroupDescriptor('endUsers', 'End users', 'EndUsers', active=False)

pmManager_observer = MeetingUserDescriptor('pmManager',
                                           duty='Secrétaire de la Chancellerie',
                                           usages=['assemblyMember'])
cadranel_signer = MeetingUserDescriptor('cadranel', duty='Secrétaire',
                                        usages=['assemblyMember', 'signer'],
                                        signatureImage='SignatureCadranel.jpg',
                                        signatureIsDefault=True)
# Add meeting users (voting purposes)
muser_voter1 = MeetingUserDescriptor('voter1', duty='Voter1',
                                     usages=['assemblyMember', 'voter', ])
muser_voter2 = MeetingUserDescriptor('voter2', duty='Voter2',
                                     usages=['assemblyMember', 'voter', ])

# Meeting configurations -------------------------------------------------------
# college
caMeeting = MeetingConfigDescriptor(
    'meeting-config-college', 'College Communal',
    'College communal', isDefault=True)
caMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                          'Charles Exemple - 1er Echevin,\n' \
                          'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                          'Jacqueline Exemple, Responsable du CPAS'
caMeeting.signatures = 'Pierre Dupont, Bourgmestre - Charles Exemple, Secrétaire communal'
caMeeting.certifiedSignatures = 'Mr Présent Actuellement, Bourgmestre ff - Charles Exemple, Secrétaire communal'
caMeeting.categories = categories
caMeeting.shortName = 'College'
caMeeting.meetingFileTypes = [annexe, annexeBudget, annexeCahier, itemAnnex,
                                   annexeDecision, overheadAnalysis, marketingAnalysis,
                                   adviceAnnex, adviceLegalAnalysis]
caMeeting.usedItemAttributes = ('toDiscuss', 'associatedGroups', 'itemIsSigned',)
caMeeting.xhtmlTransformFields = ('MeetingItem.description',
                                       'MeetingItem.detailedDescription',
                                       'MeetingItem.decision',
                                       'MeetingItem.observations',
                                       'Meeting.observations', )
caMeeting.xhtmlTransformTypes = ('removeBlanks',)
caMeeting.itemWorkflow = 'meetingitemcaidea_workflow'
caMeeting.meetingWorkflow = 'meetingcaidea_workflow'
caMeeting.itemConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowConditions'
caMeeting.itemActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowActions'
caMeeting.meetingConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowConditions'
caMeeting.meetingActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowActions'
caMeeting.transitionsToConfirm = []
caMeeting.meetingTopicStates = ('created', 'frozen')
caMeeting.decisionTopicStates = ('decided', 'closed')
caMeeting.recordItemHistoryStates = []
caMeeting.maxShownMeetings = 5
caMeeting.maxDaysDecisions = 60
caMeeting.meetingAppDefaultView = 'topic_searchmyitems'
caMeeting.itemDocFormats = ('odt', 'pdf')
caMeeting.meetingDocFormats = ('odt', 'pdf')
caMeeting.useAdvices = False
caMeeting.itemAdviceStates = ['proposed', ]
caMeeting.itemAdviceEditStates = ['proposed', 'validated']
caMeeting.itemAdviceViewStates = ['presented', ]
caMeeting.enforceAdviceMandatoriness = False
caMeeting.itemPowerObserversStates = ('itemcreated', 'presented', 'accepted', 'delayed', 'refused')
caMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
caMeeting.sortingMethodOnAddItem = 'on_proposing_groups'
caMeeting.useGroupsAsCategories = True
caMeeting.meetingPowerObserversStates = ('frozen', 'published', 'decided', 'closed')
caMeeting.useCopies = True
caMeeting.selectableCopyGroups = [developers.getIdSuffixed('reviewers'), vendors.getIdSuffixed('reviewers'), ]
caMeeting.podTemplates = [agendaTemplate, decisionsTemplate, itemTemplate]
caMeeting.meetingConfigsToCloneTo = ['meeting-config-council', ]

caMeeting.recurringItems = [
    RecurringItemDescriptor(
        id='recItem1',
        description='<p>This is the first recurring item.</p>',
        title='Recurring item #1',
        proposingGroup='',
        category='developers',
        decision='First recurring item approved'),

    RecurringItemDescriptor(
        id='recItem2',
        title='Recurring item #2',
        description='<p>This is the second recurring item.</p>',
        proposingGroup='',
        category='developers',
        decision='Second recurring item approved'),

    RecurringItemDescriptor(
        id='template1',
        title='Tutelle CPAS',
        description='Tutelle CPAS',
        category='',
        proposingGroup='developers',
        templateUsingGroups=['developers', 'vendors'],
        usages=['as_template_item', ],
        decision="""<p>Vu la loi du 8 juillet 1976 organique des centres publics d'action sociale et plus particulièrement son article 111;</p>
<p>Vu l'Arrêté du Gouvernement Wallon du 22 avril 2004 portant codification de la législation relative aux pouvoirs locaux tel que confirmé par le décret du 27 mai 2004 du Conseil régional wallon;</p>
<p>Attendu que les décisions suivantes du Bureau permanent/du Conseil de l'Action sociale du XXX ont été reçues le XXX dans le cadre de la tutelle générale sur les centres publics d'action sociale :</p>
<p>- ...;</p>
<p>- ...;</p>
<p>- ...</p>
<p>Attendu que ces décisions sont conformes à la loi et à l'intérêt général;</p>
<p>Déclare à l'unanimité que :</p>
<p><strong>Article 1er :</strong></p>
<p>Les décisions du Bureau permanent/Conseil de l'Action sociale visées ci-dessus sont conformes à la loi et à l'intérêt général et qu'il n'y a, dès lors, pas lieu de les annuler.</p>
<p><strong>Article 2 :</strong></p>
<p>Copie de la présente délibération sera transmise au Bureau permanent/Conseil de l'Action sociale.</p>"""),
    RecurringItemDescriptor(
        id='template2',
        title='Contrôle médical systématique agent contractuel',
        description='Contrôle médical systématique agent contractuel',
        category='',
        proposingGroup='vendors',
        templateUsingGroups=['vendors', ],
        usages=['as_template_item', ],
        decision="""
            <p>Vu la loi du 26 mai 2002 instituant le droit à l’intégration sociale;</p>
<p>Vu la délibération du Conseil communal du 29 juin 2009 concernant le cahier spécial des charges relatif au marché de services portant sur le contrôle des agents communaux absents pour raisons médicales;</p>
<p>Vu sa délibération du 17 décembre 2009 désignant le docteur XXX en qualité d’adjudicataire pour la mission de contrôle médical des agents de l’Administration communale;</p>
<p>Vu également sa décision du 17 décembre 2009 d’opérer les contrôles médicaux de manière systématique et pour une période d’essai d’un trimestre;</p>
<p>Attendu qu’un certificat médical a été  reçu le XXX concernant XXX la couvrant du XXX au XXX, avec la mention « XXX »;</p>
<p>Attendu que le Docteur XXX a transmis au service du Personnel, par fax, le même jour à XXX le rapport de contrôle mentionnant l’absence de XXX ce XXX à XXX;</p>
<p>Considérant que XXX avait été informée par le Service du Personnel de la mise en route du système de contrôle systématique que le médecin-contrôleur;</p>
<p>Considérant qu’ayant été absent(e) pour maladie la semaine précédente elle avait reçu la visite du médecin-contrôleur;</p>
<p>DECIDE :</p>
<p><strong>Article 1</strong> : De convoquer XXX devant  Monsieur le Secrétaire communal f.f. afin de lui rappeler ses obligations en la matière.</p>
<p><strong>Article 2</strong> :  De prévenir XXX, qu’en cas de récidive, il sera proposé par le Secrétaire communal au Collège de transformer les jours de congés de maladie en absence injustifiée (retenue sur traitement avec application de la loi du 26 mai 2002 citée ci-dessus).</p>
<p><strong>Article 3</strong> : De charger le service du personnel du suivi de ce dossier.</p>"""),
]

# Conseil communal
agMeeting = MeetingConfigDescriptor(
    'meeting-config-council', 'Conseil Communal',
    'Conseil Communal')
agMeeting.assembly = 'Default assembly'
agMeeting.signatures = 'Default signatures'
agMeeting.certifiedSignatures = 'Mr Présent Actuellement, Bourgmestre ff - Charles Exemple, Secrétaire communal'
agMeeting.categories = categories
agMeeting.shortName = 'Council'
agMeeting.meetingFileTypes = [annexe, annexeBudget, annexeCahier,
                                   itemAnnex, annexeDecision, adviceAnnex, adviceLegalAnalysis]
agMeeting.xhtmlTransformFields = ('MeetingItem.description',
                                       'MeetingItem.detailedDescription',
                                       'MeetingItem.decision',
                                       'MeetingItem.observations',
                                       'Meeting.observations', )
agMeeting.xhtmlTransformTypes = ('removeBlanks',)
agMeeting.itemWorkflow = 'meetingitemcaidea_workflow'
agMeeting.meetingWorkflow = 'meetingcaidea_workflow'
agMeeting.itemConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowConditions'
agMeeting.itemActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingItemCAIDEAWorkflowActions'
agMeeting.meetingConditionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowConditions'
agMeeting.meetingActionsInterface = 'Products.MeetingIDEA.interfaces.IMeetingCAIDEAWorkflowActions'
agMeeting.transitionsToConfirm = []
agMeeting.meetingTopicStates = ('created', 'frozen', 'published')
agMeeting.decisionTopicStates = ('decided', 'closed')
agMeeting.recordItemHistoryStates = []
agMeeting.maxShownMeetings = 5
agMeeting.maxDaysDecisions = 60
agMeeting.meetingAppDefaultView = 'topic_searchmyitems'
agMeeting.itemDocFormats = ('odt', 'pdf')
agMeeting.meetingDocFormats = ('odt', 'pdf')
agMeeting.usedItemAttributes = ('toDiscuss', 'associatedGroups', 'itemIsSigned',)
agMeeting.sortingMethodOnAddItem = 'on_categories'
agMeeting.useGroupsAsCategories = False
agMeeting.useAdvices = True
agMeeting.itemAdviceStates = ['proposed', ]
agMeeting.itemAdviceEditStates = ['proposed', 'validated']
agMeeting.itemAdviceViewStates = ['presented', ]
agMeeting.transitionReinitializingDelays = 'backToItemCreated'
agMeeting.enforceAdviceMandatoriness = False
agMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
agMeeting.itemPowerObserversStates = caMeeting.itemPowerObserversStates
agMeeting.meetingPowerObserversStates = caMeeting.meetingPowerObserversStates
agMeeting.useCopies = True
agMeeting.selectableCopyGroups = [developers.getIdSuffixed('reviewers'), vendors.getIdSuffixed('reviewers'), ]
agMeeting.useVotes = True
agMeeting.meetingUsers = [muser_voter1, muser_voter2, ]
agMeeting.recurringItems = []

#no recurring items for this meetingConfig, only for tests !!!
#so we can test a meetingConfig with recurring items (college) and without (council)

data = PloneMeetingConfiguration(
    meetingFolderTitle='Mes seances',
    meetingConfigs=(caMeeting, agMeeting),
    groups=(developers, vendors, endUsers))
data.unoEnabledPython = '/usr/bin/python'
data.usersOutsideGroups = [voter1, voter2, powerobserver1, powerobserver2]
# ------------------------------------------------------------------------------
