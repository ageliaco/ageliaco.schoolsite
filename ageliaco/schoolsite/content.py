# -*- coding: utf-8 -*-

from .interfaces import (
#    ISchoolGeneralInfo,
    
    IDiscipline,
    IDisciplineContainer,

)

from plone.dexterity.content import Item
from plone.dexterity.content import Container

from Products.CMFCore.utils import getToolByName

from zope.interface import implements



#class SchoolGeneralInfo(Container):
#    implements(ISchoolGeneralInfo)



class Discipline(Container):
    implements(IDiscipline)

class DisciplineContainer(Container):
    implements(IDisciplineContainer)

