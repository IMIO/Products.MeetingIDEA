from Products.Archetypes.atapi import *
from Products.PloneMeeting.Meeting import Meeting
from Products.PloneMeeting.MeetingItem import MeetingItem


def update_item_schema(baseSchema):

    specificSchema = Schema((
        TextField(
            name='internalCommunication',
            widget=TextAreaWidget(
                condition="python: here.portal_plonemeeting.isManager()",
                description="InternalCommunication",
                description_msgid="item_internalCommunication_descr",
                label='InternalCommunication',
                label_msgid='PloneMeeting_label_internalCommunication',
                i18n_domain='PloneMeeting',
            ),
            optional=True,
        ),)
    )

    baseSchema['detailedDescription'].widget.description = "DetailedDescriptionMethode"
    baseSchema['detailedDescription'].widget.description_msgid = "detailedDescription_item_descr"
    completeItemSchema = baseSchema + specificSchema.copy()
    return completeItemSchema
MeetingItem.schema = update_item_schema(MeetingItem.schema)


def update_meeting_schema(baseSchema):
    specificSchema = Schema((
    ),)

    baseSchema['assembly'].widget.description_msgid = "assembly_meeting_descr"

    completeMeetingSchema = baseSchema + specificSchema.copy()
    return completeMeetingSchema
Meeting.schema = update_meeting_schema(Meeting.schema)
