# -*- coding: utf-8 -*-

import transaction

# import logging

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import INonInstallable

from plone.app.contenttypes.setuphandlers import (
    _publish,
    _translate,
    addContentToContainer,
    _get_locales_info,
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
      SITEADMIN_CONTENT,
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

    ########################
    
    ### Site Administration part of the site structure
    
    ## 1st & 2nd levels

    createDXSubcontainer(portal, 
                         'Folder',
                         'siteadministration', 
                         u'SITE ADMINISTRATION', 
                         u'site-administration-title', 
                         target_language)
    siteadmin_root_folder = portal['siteadministration']
    siteadmin_root_folder.exclude_from_nav = True
    siteadmin_root_folder.reindexObject()
    
    batchCreateSubcontainers(siteadmin_root_folder,
                             SITEADMIN_CONTENT['MAIN_SECTIONS'], 
                             target_language)     

    # make _p_jar on content, before next batch of objects creation
    transaction.savepoint(optimistic=True)

    ## 3rd level
    for folder_id, folder_contents_key in [
                                            ('homepage','HOMEPAGE_CHILDREN'),
                                         ]:
        folder = siteadmin_root_folder[folder_id]
        batchCreateSubcontainers(folder,
                                 SITEADMIN_CONTENT[folder_contents_key], 
                                 target_language)     

    # make _p_jar on content, before next batch of objects creation
    transaction.savepoint(optimistic=True)

    ########################

    ### Editorial part of the site structure
    
    ## 1st level - Other sections
    batchCreateSubcontainers(portal,
                             CONTENT['MAIN_SECTIONS'], 
                             target_language)     

    # make _p_jar on content, before next batch of objects creation
    transaction.savepoint(optimistic=True)

    ## 2nd level
    for folder_id, folder_contents_key in [
                                            ('presentation','ABOUT_CHILDREN'),
                                            ('vie-ecole','VIE_ECOLE_CHILDREN'),
                                            ('espace-pedagogique','PEDAGOGIQUE_CHILDREN'),
                                            ('espace-administratif','ADMINISTRATIF_CHILDREN'),
                                         ]:
        folder = portal[folder_id]
        batchCreateSubcontainers(folder,
                                 CONTENT[folder_contents_key], 
                                 target_language)     

    # make _p_jar on content, before next batch of objects creation
    transaction.savepoint(optimistic=True)
                             
    ## 3nd level...
    # Let's disable the 3rd level for now!
#     for folder_id, subfolder_id, subfolder_contents_key in [
#                                                ('presentation','ecole','PRESENTATION_ECOLE_CHILDREN'),
#                                                ('presentation','etudes','PRESENTATION_ETUDES_CHILDREN'),
#                                                ('presentation','personnes','PRESENTATION_PERSONNES_CHILDREN'),
#                                                   
#                                                  ]:
#         subfolder = portal[folder_id][subfolder_id]
#         batchCreateSubcontainers(subfolder,
#                                  CONTENT[subfolder_contents_key], 
#                                  target_language)     
# 
#     # make _p_jar on content, before proceeding to various changes on the content
#     transaction.savepoint(optimistic=True)

    ########################

    ### Additional adjustments
    
    # Hide some top-level folders from navigation
    HIDDEN_FOLDERS = ['news', 'events', 'images',]
    for folderid in HIDDEN_FOLDERS:
        folder = portal[folderid]
        folder.exclude_from_nav = True
        folder.reindexObject()
    
    # News Aggregator: Query by Type and Review State: We also want to list contents with 'visible' state
    news_folder = portal['news']
    news_aggregator = news_folder['aggregator']
    news_aggregator.query = [
            {'i': u'portal_type',
             'o': u'plone.app.querystring.operation.selection.is',
             'v': [u'News Item'],
             },
            {'i': u'review_state',
             'o': u'plone.app.querystring.operation.selection.is',
             'v': [u'published', 'visible'],
             },
        ]

    # Events Aggregator: Query by Type, Review State and Event start date after today: We also want to list contents with 'visible' state
    events_folder = portal['events']
    events_aggregator = events_folder['aggregator']
    events_aggregator.query = [
            {'i': 'portal_type',
             'o': 'plone.app.querystring.operation.selection.is',
             'v': ['Event']
             },
            {'i': 'start',
             'o': 'plone.app.querystring.operation.date.afterToday',
             'v': ''
             },
            {'i': 'review_state',
             'o': 'plone.app.querystring.operation.selection.is',
             'v': ['published', 'visible']
             },
        ]
