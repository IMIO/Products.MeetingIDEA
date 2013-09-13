# -*- coding: utf-8 -*-
from plone.testing import z2, zca
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import FunctionalTesting
import Products.MeetingIDEA


MC_ZCML = zca.ZCMLSandbox(filename="testing.zcml",
                          package=Products.MeetingIDEA,
                          name='MC_ZCML')

MC_Z2 = z2.IntegrationTesting(bases=(z2.STARTUP, MC_ZCML),
                              name='MC_Z2')

MC_TESTING_PROFILE = PloneWithPackageLayer(
    zcml_filename="testing.zcml",
    zcml_package=Products.MeetingIDEA,
    additional_z2_products=('Products.MeetingIDEA',
                            'Products.PloneMeeting',
                            'Products.CMFPlacefulWorkflow'),
    gs_profile_id='Products.MeetingIDEA:testing',
    name="MC_TESTING_PROFILE")

MC_TESTING_PROFILE_FUNCTIONAL = FunctionalTesting(
    bases=(MC_TESTING_PROFILE,), name="MC_TESTING_PROFILE_FUNCTIONAL")
