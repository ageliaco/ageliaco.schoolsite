# -*- coding: utf-8 -*-

import transaction

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

from ageliaco.schoolsite.config import (
      CONTENT,
      LOCAL_GROUPS,
)

from ageliaco.schoolsite import _


# class HiddenProfiles(object):
#     implements(INonInstallable)
# 
#     def getNonInstallableProfiles(self):
#         """
#         Prevents uninstall profile from showing up in the profile list
#         when creating a Plone site.
#         """
#         return [u'plone.app.contenttypes:uninstall']


## Reused functions for the "setup various" part

def setupGroups(site):
    """
    Create our specific set of groups.
    """
    uf = getToolByName(site, 'acl_users')
    gtool = getToolByName(site, 'portal_groups')
    regtool = getToolByName(site, 'portal_registration')
    
    for groupid, memberid in LOCAL_GROUPS: 
        if not uf.searchGroups(id=groupid):
            gtool.addGroup(groupid, title=groupid,
                       roles=[])
                       
        # Setup a test user as a member of each group
        member_properties = {
                 'username': memberid,
                 'fullname': memberid,
                 'email': memberid + '@schoolsite.com',
               }
        try:
            # addMember() returns MemberData object
            member = regtool.addMember(memberid, memberid, properties=member_properties)
            print "Added member: " + member.getUserName()
            gtool.addPrincipalToGroup(memberid, groupid)
        except ValueError, e:
            # Give user visual feedback what went wrong
            #IStatusMessage(request).addStatusMessage(_(u"Could not create the user:") + unicode(e), "error")
            print u"Could not create the user or add it to the group:" + unicode(e), "error"

def setupInitialSiteAdmin(site):
    """
    Initial Site Admin.
    """
    uf = getToolByName(site, 'acl_users')
    gtool = getToolByName(site, 'portal_groups')
    regtool = getToolByName(site, 'portal_registration')

    properties = {
                 'username': 'siteadmin',
                 'fullname': u"Site Admin",
                 'email': 'siteadmin@schoolsite.com',
               }
    try:
        member = regtool.addMember('siteadmin', 'admin', properties=properties)
        print "Added siteadmin"
        gtool.addPrincipalToGroup('siteadmin', 'Site Administrators')
    except ValueError, e:
        # Give user visual feedback what went wrong
        #IStatusMessage(request).addStatusMessage(_(u"Could not create the user:") + unicode(e), "error")
        print u"Could not create the siteadmin user or add it to the group:" + unicode(e), "error"

## Setup various function

def setupVarious(context):
    """Import step for configuration that is not handled in xml files.
    """
    # Only run step if a flag file is present
    if context.readDataFile('ageliaco.schoolsite_various.txt') is None:
        return
    logger = context.getLogger('ageliaco.schoolsite')
    site = context.getSite()
    #add_catalog_indexes(site, logger)    # Initial code copied from p.a.multilingual
    
    setupGroups(site)
    setupInitialSiteAdmin(site)


## Reused functions for the content import

def addBookingCenter(container, target_language):
    # First, install the PloneBooking product if not yet !!!
    
    qi = getToolByName(container, 'portal_quickinstaller')
    if not qi.isProductInstalled('PloneBooking'):
        #qi.installProduct('PloneBooking', locked=0)    
        qi.installProduct('PloneBooking')
    
    # Add the Booking Center
    createATSubcontainer(container, 
                         'BookingCenter', 
                         'reservation-des-salles', 
                         u'Reservation des salles', 
                         u'reservation-des-salles-title', 
                         target_language)


## Import function

def importContent(context):
    """Import base content into the Plone site."""
    if context.readDataFile('ageliaco.schoolsite_content.txt') is None:
        return
    portal = context.getSite()
    target_language, is_combined_language, locale = _get_locales_info(portal)

    # Set up Language specific information
    setLanguageInfo(portal, locale, is_combined_language, target_language)

    # Default sections and content, at the 1st level
    createCommonSectionsAndContents(portal, target_language)
    
    ## 1st level - Other sections
    batchCreateSubcontainers(portal,
                             CONTENT['MAIN_SECTIONS'], 
                             target_language)     

    ## 2nd level
    for folder_id, folder_contents_config_key in [('presentation','ABOUT_SUBSECTIONS'),
                                                  ('vie-ecole','VIE_ECOLE_SUBSECTIONS'),
                                                  ('espace-pedagogique','PEDAGOGIQUE_SUBSECTIONS'),
                                                  ('espace-administratif','ADMINISTRATIF_SUBSECTIONS'),
                                         ]:
        folder = portal[folder_id]
        batchCreateSubcontainers(folder,
                                 CONTENT[folder_contents_config_key], 
                                 target_language)     
                             
    # Special case (for now) - Add the Booking Center to the 'espace-administratif' section
    addBookingCenter(portal['espace-administratif'], target_language)
        
    ## 3nd level...
#     disciplinesSection = portal['espace-pedagogique']['disciplines']
#     batchCreateSubcontainers(disciplinesSection,
#                              CONTENT['DISCIPLINES'], 
#                              target_language)
# 
#     # 2 or 3 additional subfolders for documents/files...
#     createDXSubcontainer(disciplinesSection, 
#                          'Folder', 
#                          'documents-pv', 
#                          u'Documents - PVs', 
#                          u'documents-pv-title', 
#                          target_language)
#     createDXSubcontainer(disciplinesSection, 
#                          'Folder', 
#                          'documents-decisions', 
#                          u'''Documents - Décisions''', 
#                          u'documents-decisions-title', 
#                          target_language)


    # make _p_jar on content, before proceeding to various changes on the content
    transaction.savepoint(optimistic=True)
    
    # Hide some top-level folders from navigation
    HIDDEN_FOLDERS = ['news', 'events', 'images',]
    for folderid in HIDDEN_FOLDERS:
        folder = portal[folderid]
        folder.exclude_from_nav = True
        folder.reindexObject()
    
