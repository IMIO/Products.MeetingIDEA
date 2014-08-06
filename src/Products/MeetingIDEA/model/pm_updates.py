from Products.Archetypes.atapi import *
from Products.PloneMeeting.Meeting import Meeting
from Products.PloneMeeting.MeetingItem import MeetingItem
from Products.PloneMeeting.MeetingConfig import MeetingConfig


def update_item_schema(baseSchema):

    specificSchema = Schema((
        TextField(
            name='internalCommunication',
            widget=RichWidget(
                condition="python: here.portal_plonemeeting.isManager()",
                description="InternalCommunication",
                description_msgid="item_internalCommunication_descr",
                label='InternalCommunication',
                label_msgid='PloneMeeting_label_internalCommunication',
                i18n_domain='PloneMeeting',
            ),
            optional=True,
            default_content_type="text/html",
            allowable_content_types=('text/html',),
            default_output_type="text/x-html-safe",
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


def update_config_schema(baseSchema):
    specificSchema = Schema((
        TextField(
            name='itemDecisionReportText',
            widget=TextAreaWidget(
                description="ItemDecisionReportText",
                description_msgid="item_decision_report_text_descr",
                label='ItemDecisionReportText',
                label_msgid='PloneMeeting_label_itemDecisionReportText',
                i18n_domain='PloneMeeting',
            ),
            allowable_content_types=('text/plain', 'text/html', ),
            default_output_type="text/plain",
        )
    ),)
    completeConfigSchema = baseSchema + specificSchema.copy()
    completeConfigSchema.moveField('itemDecisionReportText', after='budgetDefault')
    return completeConfigSchema
MeetingConfig.schema = update_config_schema(MeetingConfig.schema)

# Classes have already been registered, but we register them again here
# because we have potentially applied some schema adaptations (see above).
# Class registering includes generation of accessors and mutators, for
# example, so this is why we need to do it again now.
from Products.PloneMeeting.config import registerClasses
registerClasses()
