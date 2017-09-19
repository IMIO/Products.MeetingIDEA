# -*- coding: utf-8 -*-
from plone.testing import z2, zca
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import FunctionalTesting
import Products.MeetingIDEA
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE

MIDEA_ZCML = zca.ZCMLSandbox(filename="testing.zcml",
                          package=Products.MeetingIDEA,
                          name='MIDEA_ZCML')

MIDEA_Z2 = z2.IntegrationTesting(bases=(z2.STARTUP, MIDEA_ZCML),
                              name='MIDEA_Z2')

MIDEA_TESTING_PROFILE = PloneWithPackageLayer(
    zcml_filename="testing.zcml",
    zcml_package=Products.MeetingIDEA,
    additional_z2_products=('imio.dashboard',
                            'Products.MeetingIDEA',
                            'Products.PloneMeeting',
                            'Products.CMFPlacefulWorkflow',
                            'Products.PasswordStrength'),
    gs_profile_id='Products.MeetingIDEA:testing',
    name="MIDEA_TESTING_PROFILE")

MIDEA_TESTING_PROFILE_FUNCTIONAL = FunctionalTesting(
    bases=(MIDEA_TESTING_PROFILE,), name="MIDEA_TESTING_PROFILE_FUNCTIONAL")

MIDEA_DEMO_TESTING_PROFILE = PloneWithPackageLayer(
    zcml_filename="testing.zcml",
    zcml_package=Products.MeetingIDEA,
    additional_z2_products=('imio.dashboard',
                            'Products.MeetingIDEA',
                            'Products.PloneMeeting',
                            'Products.CMFPlacefulWorkflow',
                            'Products.PasswordStrength'),
    gs_profile_id='Products.MeetingIDEA:demo',
    name="MIDEA_TESTING_PROFILE")

MIDEA_TESTING_ROBOT = FunctionalTesting(
    bases=(
        MIDEA_DEMO_TESTING_PROFILE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="MIDEA_TESTING_ROBOT",
)
