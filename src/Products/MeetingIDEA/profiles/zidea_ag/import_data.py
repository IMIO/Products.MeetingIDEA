# -*- coding: utf-8 -*-

from copy import deepcopy
from Products.MeetingCommunes.profiles.simple import import_data as simple_import_data
from Products.PloneMeeting.profiles import PloneMeetingConfiguration


config = deepcopy(simple_import_data.simpleMeeting)
config.id = 'meeting-config-ag'
config.title = 'Assemblée Générale'
config.folderTitle = 'Assemblée Générale'
config.shortName = 'AG'

config.workflowAdaptations = [
    'no_publication',
    'return_to_proposing_group',
    'refused'
]


data = PloneMeetingConfiguration(
    meetingFolderTitle='Mes séances',
    meetingConfigs=(config, ),
    orgs=[])