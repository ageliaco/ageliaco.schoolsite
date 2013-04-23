# -*- coding: utf-8 -*-

# import logging
# 
# from zope.component import (
#     getUtility,
#     queryUtility,
#     getMultiAdapter,
#     queryMultiAdapter,
# )
# from zope.component.hooks import getSite
# from zope.i18n.locales import locales
# from zope.interface import implements
# from Acquisition import aq_base, aq_inner
# #from AccessControl import Unauthorized
# from plone.i18n.normalizer.interfaces import IURLNormalizer
# from plone.dexterity.utils import createContent
# from plone.dexterity.fti import IDexterityFTI
# #from plone.app.textfield.value import RichTextValue
# #from plone.portlets.interfaces import (
# #    ILocalPortletAssignmentManager, IPortletManager,)
# 
# #from Products.PythonScripts.PythonScript import PythonScript
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import INonInstallable
# from Products.CMFPlone.utils import _createObjectByType
# #from Products.CMFDefault.utils import bodyfinder
# #from Products.CMFPlone.Portal import member_indexhtml

from plone.app.contenttypes.setuphandlers import (
    _publish,
    _translate,
    addContentToContainer,
    _get_locales_info,
#    _set_language_settings,
#    _setup_visible_ids,
#    #_setup_calendar,
)

from collective.makesitestructure.utils import (
      setLanguageInfo,
      createDXSubcontainer, createATSubcontainer,
      createSectionWithAggregator,
      batchCreateSubcontainers,
      createCommonSectionsAndContents,
)

from .config import (
      SCHOOL,
)


# class HiddenProfiles(object):
#     implements(INonInstallable)
# 
#     def getNonInstallableProfiles(self):
#         """
#         Prevents uninstall profile from showing up in the profile list
#         when creating a Plone site.
#         """
#         return [u'plone.app.contenttypes:uninstall']



## Import functions

def importContent(context):
    """Import base content into the Plone site."""
    if context.readDataFile('ageliaco_schoolsite.txt') is None:
        return
    portal = context.getSite()
    target_language, is_combined_language, locale = _get_locales_info(portal)

    # Set up Language specific information
    setLanguageInfo(portal, locale, is_combined_language, target_language)

    # Default sections and content, at the 1st level
    createCommonSectionsAndContents(portal, target_language)
    
    ## 1st level - Other sections
    batchCreateSubcontainers(portal,
                             SCHOOL['MAIN_SECTIONS'], 
                             'Folder', 
                             target_language)     

    ## 2nd level
    aboutSection = portal['presentation']
    batchCreateSubcontainers(aboutSection,
                             SCHOOL['ABOUT_SUBSECTIONS'], 
                             'Folder', 
                             target_language)     
                             
    pedagoSection = portal['espace-pedagogique']
    batchCreateSubcontainers(pedagoSection,
                             SCHOOL['PEDAGO_SUBSECTIONS'], 
                             'Folder', 
                             target_language)     

    adminSection = portal['espace-administratif']
    batchCreateSubcontainers(adminSection,
                             SCHOOL['ADMIN_SUBSECTIONS'], 
                             'Folder', 
                             target_language)
    # The Booking Center  --> Probably need to externalise to another package cause specific!!!
#     createATSubcontainer(adminSection, 
#                       'BookingCenter', 
#                       'reservation-des-salles', 
#                       u'Reservation des salles', 
#                       u'reservation-des-salles-title', 
#                       target_language)
    
    ## 3nd level...
    disciplinesSection = portal['espace-pedagogique']['disciplines']
    batchCreateSubcontainers(disciplinesSection,
                             SCHOOL['DISCIPLINES'], 
                             'Folder', 
                             target_language)

    # 2 or 3 additional subfolders for documents/files...
    createDXSubcontainer(disciplinesSection, 
                         'Folder', 
                         'documents-pv', 
                         u'Documents - PVs', 
                         u'documents-pv-title', 
                         target_language)
    createDXSubcontainer(disciplinesSection, 
                         'Folder', 
                         'documents-decisions', 
                         u'''Documents - Décisions''', 
                         u'documents-decisions-title', 
                         target_language)
    # ...



