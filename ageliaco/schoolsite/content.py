# -*- coding: utf-8 -*-

from .interfaces import (
    IDiscipline,
    IDisciplineContainer,

)

from plone.dexterity.content import Item
from plone.dexterity.content import Container

from Products.CMFCore.utils import getToolByName

from zope.interface import implements


class Discipline(Container):
    implements(IDiscipline)

class DisciplineContainer(Container):
    implements(IDisciplineContainer)

