# -*- coding: utf-8 -*-

import logging

from Products.CMFPlone.utils import _createObjectByType

from plone.dexterity.utils import createContent
from plone.app.textfield.value import RichTextValue

from plone.app.contenttypes.setuphandlers import (
    _publish,
    _translate,
    addContentToContainer,
    _get_locales_info,
    _set_language_settings,
    _setup_visible_ids,
    #_setup_calendar,
)


## Reused functions

def setLanguageInfo(portal, locale, is_combined_language, target_language):
    # Set up Language specific information
    _set_language_settings(portal, is_combined_language)
    #_setup_calendar(locale)
    _setup_visible_ids(target_language, locale)

# Most of our contents are DX-based, but we could have AT-based ones,
# hence, two different functions...
def createDXSubcontainer(container, type, id, title, title_msgid, target_language):
    existing_content = container.keys()
    if id not in existing_content:
        title = _translate(title_msgid, target_language, title)
        #description = _translate(u'about-description', target_language,
        #                         u"About us.")
        
        subcontainer = createContent(type, id=id,
                                     title=title,
                                     #description=description
                                     )
        subcontainer = addContentToContainer(container, subcontainer)
        
        subcontainer.setOrdering('unordered')
        subcontainer.reindexObject()
        _publish(subcontainer)

def createATSubcontainer(container, type, id, title, title_msgid, target_language):
    existing_content = container.keys()
    if id not in existing_content:
        title = _translate(title_msgid, target_language, title)
        #description = _translate(u'about-description', target_language,
        #                         u"About us.")
        
        _createObjectByType(type, container, id=id,
                            title=title, 
                            #description=description
                            )

        subcontainer = getattr(container, id)
        subcontainer.setOrdering('unordered')
        subcontainer.reindexObject()
        _publish(subcontainer)


def createDXDocument(container, id, title, title_msgid, text, target_language):
    existing_content = container.keys()
    if id not in existing_content:
        title = _translate(title_msgid, target_language, title)
        #description = _translate(u'about-description', target_language,
        #                         u"About us.")
        
        item = createContent('Document', id=id,
                             title=title,
                             #description=description,
                          ##   text = text
                             )
        item = addContentToContainer(container, item)
        item.text = RichTextValue(
                           text,
                           'text/html',
                           'text/x-html-safe'
                         )
        
        #item.setOrdering('unordered')
        _publish(item)
        item.reindexObject()


def batchCreateSubcontainers(container, items, target_language):
    for item in items:
       # if item[3] in ('BookingCenter',):   # Handle here the cases where we are still using AT !!!
       #     createATSubcontainer(container, 
       #                          item[3],   # The content type.
       #                          item[0], 
       #                          item[1], 
       #                          item[2],  
       #                          target_language)
        if item[3] in ('Document',):   # Handle here the case of the standard Document (DX) !!!
            createDXDocument(container, 
                                 item[0], 
                                 item[1], 
                                 item[2],  
                                 item[4],  # The text 
                                 target_language)
        else:
            createDXSubcontainer(container, 
                                 item[3],
                                 item[0], 
                                 item[1], 
                                 item[2],  
                                 target_language)
                           
def createSectionWithAggregator(container, added_content_types, id, title, title_msgid, 
                                target_language):
    # Exemple: added_content_types = ['News Item']
    createDXSubcontainer(container, 
                         'Folder', 
                         id, 
                         title, 
                         title_msgid, 
                         target_language)
                         
    section = getattr(container, id)
    if 'aggregator' not in section.keys():
        _createObjectByType('Collection', section,
                                id='aggregator', 
                                title=title,
                                #description=description
                                )
                                                    
    aggregator = section['aggregator']

    section.setOrdering('unordered')
    section.setDefaultPage('aggregator')
    _publish(section)

    # Set the Collection criteria.
    #: Sort on the Effective date
    aggregator.sort_on = u'effective'
    aggregator.reverse_sort = True
    #: Query by Type, Review State, Date, etc.
    query = [
            {'i': u'portal_type',
             'o': u'plone.app.querystring.operation.selection.is',
             'v': added_content_types,
             },
            {'i': u'review_state',
             'o': u'plone.app.querystring.operation.selection.is',
             'v': [u'published'],
             },
        ]
    if added_content_types == ['Event']:
        query.insert(1, 
            {'i': 'start',
              'o': 'plone.app.querystring.operation.date.afterToday',
              'v': ''
              },
            )
    aggregator.query = query

    aggregator.setLayout('summary_view')

    _publish(aggregator)


def createCommonSectionsAndContents(portal, target_language):

    ## 1st level - Default News and Events sections    
    # News topic
    createSectionWithAggregator(portal, 
                                ['News Item'], 
                                'news', 
                                u'News', 
                                u'news-title', 
                                target_language)
    # Events topic
    createSectionWithAggregator(portal, 
                                ['Event'],
                                'events', 
                                u'Events', 
                                u'events-title', 
                                target_language)

    ## 1st level - Add a media repository for images
    createDXSubcontainer(portal, 
                         'Folder',
                         'images', 
                         u'Images', 
                         u'images-title', 
                         target_language)
