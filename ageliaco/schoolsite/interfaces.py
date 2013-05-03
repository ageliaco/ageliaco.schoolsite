# -*- coding: utf-8 -*-
from plone.supermodel import model

from zope.interface import Interface, Attribute
from zope import schema
from ageliaco.schoolsite import _


class IAgeliacoSchoolSiteLayer(Interface):
    """Marker interface that defines a ZTK browser layer. We can reference
    this in the 'layer' attribute of ZCML <browser:* /> directives to ensure
    the relevant registration only takes effect when this theme is installed.

    The browser layer is installed via the browserlayer.xml GenericSetup
    import step.
    """


# Interfaces for the objects we use to build the About section
class ISchoolGeneralInfo(Interface):
    """
    """


# Interfaces for Disciplines
class IDiscipline(Interface):
    """
    """

class IDisciplineContainer(Interface):
    """
    """


