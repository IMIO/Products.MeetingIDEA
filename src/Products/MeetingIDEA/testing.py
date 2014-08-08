# -*- coding: utf-8 -*-
from plone.testing import z2, zca
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import FunctionalTesting
import Products.MeetingIDEA


MIDEA_ZCML = zca.ZCMLSandbox(filename="testing.zcml", package=Products.MeetingIDEA, name='MIDEA_ZCML')

MIDEA_Z2 = z2.IntegrationTesting(bases=(z2.STARTUP, MIDEA_ZCML), name='MIDEA_Z2')

MIDEA_TESTING_PROFILE = PloneWithPackageLayer(
    zcml_filename="testing.zcml",
    zcml_package=Products.MeetingIDEA,
    additional_z2_products=('Products.MeetingIDEA',
                            'Products.PloneMeeting',
                            'Products.CMFPlacefulWorkflow'),
    gs_profile_id='Products.MeetingIDEA:testing',
    name="MIDEA_TESTING_PROFILE")

MIDEA_TESTING_PROFILE_FUNCTIONAL = FunctionalTesting(
    bases=(MIDEA_TESTING_PROFILE,), name="MIDEA_TESTING_PROFILE_FUNCTIONAL")
