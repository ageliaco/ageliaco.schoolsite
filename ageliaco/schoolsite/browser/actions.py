# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime 

#from zope import component

from Products.Five.browser import BrowserView

from Products.CMFCore.utils import getToolByName

#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.textfield.value import RichTextValue

from ageliaco.schoolsite.config import (
      LOCAL_GROUPS,
)


## Here we define Views for administrative tasks        


# 1) BrowserView class for importing Footer/Doormat initial content

FOOTER_TEXTS_CONFIG = {
'schoolsite-col-1': {
  'title': 'Administration',
  'text':  '''<h3 style="text-align: center; "><a class="internal-link" href="#">Administration</a></h3>
<p style="text-align: center; "><span class="discreet">Infos n&eacute;cessaires et/ou utiles</span></p>'''
},
'schoolsite-col-2': {
  'title': '''Vie Ecole''',
  'text':  '''<h3 style="text-align: center; "><a class="internal-link" href="#">Vie de l'&eacute;cole</a></h3>
<p style="text-align: center; "><span class="discreet">Ce qui fait - aussi - l'&eacute;cole!</span></p>'''
},
'schoolsite-col-3': {
  'title': 'Pedagogie',
  'text':  '''<h3 style="text-align: center; "><a class="internal-link" href="#">P&eacute;dagogie</a></h3>
<p style="text-align: center; "><span class="discreet">Enseigner et apprendre</span></p>'''
},
'schoolsite-col-4': {
  'title': 'Presentation',
  'text':  '''<h3 style="text-align: center; "><a class="internal-link" href="#">Pr&eacute;sentation</a></h3>
<p style="text-align: center; "><span class="discreet">Tout savoir sur le coll&egrave;ge</span></p>'''
},

}


class ImportDoormatContent(BrowserView):
    """
    """

    def __call__(self):

        context = self.context

        if 'doormat' in context.objectIds():
            dm = context['doormat']

            dm.setShowTitle(False)

            for col_id in ['schoolsite-col-1','schoolsite-col-2','schoolsite-col-3','schoolsite-col-4']:
                oid = dm.invokeFactory('DoormatColumn', col_id)
                column = dm[oid]
                column.setTitle('Colonne %s' % col_id)
                column.setShowTitle(False)
                column.reindexObject()
   
                section_id = col_id + '-section1'
                oid = column.invokeFactory('DoormatSection', section_id)
                section = column[oid]
                section.setTitle('Section %s' % section_id)
                section.setShowTitle(False)
                section.reindexObject()

                doc_id = section_id + '-doc1'
                oid = section.invokeFactory("Document", doc_id)
                doc = section[oid]
                doc.title = FOOTER_TEXTS_CONFIG[col_id]['title']
                doc.text = RichTextValue(FOOTER_TEXTS_CONFIG[col_id]['text'], 'text/html', 'text/html')
                doc.reindexObject()
            
        return context.REQUEST.response.redirect(context.absolute_url() + '/webmaster-help')


# 2) BrowserView class for importing the /presentation/liens-institutionnels links folder

class ImportLiensInstitutionnels(BrowserView):
    """
    """

    def __call__(self):

        context = self.context

        if 'presentation' in context.objectIds():
            about_folder = context['presentation']

            if not 'liens-institutionnels' in about_folder.objectIds():
                about_folder.invokeFactory(type_name="Folder",
                                           id='liens-institutionnels',
                                           title='Liens institutionnels')
            
            links_folder = about_folder['liens-institutionnels']
            
            # Ajouter Link --> Relatif à l'école sur le site du DIP
            if not 'infos-relatives-sur-site-du-dip' in links_folder.objectIds():
                links_folder.invokeFactory(type_name="Link",
                                           id='infos-relatives-sur-site-du-dip',
                                           title='''Infos relatives à [mon école] sur le site du DIP''',
                                           remoteUrl='http://url-a-completer.ch')
                                                                                  
            # Set the corresponding layout
            links_folder.setLayout('links')

        return context.REQUEST.response.redirect(context.absolute_url() + '/webmaster-help')
            


# 3) BrowserView class for importing Events
            
# Functions and constants for the import of events

def cleaning(mot):
    # suppression des "
    word = mot
    if word[1]=='"':
        word = word[1:]
    if word[-1]=='"':
        word = word[:-1]
    return word

def multisubject(mot):
    # transforme une liste avec virgule en multiligne
    sujets = mot.split(',')
    word = ''
    for s in sujets:
        if word :
            word += '\n' + s
        else:
            word = s
    return word

def convertCSVEntryToDatetimeObject(entry):
    # get datetime obj from a csv column data (string) of the form: 08/26/2013 07:30
    first_split = entry.split(' ')
    date = first_split[0]
    hour_and_min = first_split[1]

    second_split = date.split('/')
    month = second_split[0]
    day = second_split[1]
    year = second_split[2]

    third_split = hour_and_min.split(':')
    hour = third_split[0]
    min = third_split[1]

    return datetime(int(year), int(month), int(day), int(hour), int(min))


DEFAULT_TIMEZONE = "Europe/Zurich"
CSV_FILE_NAME = 'evenements.csv'

# BrowserView class

class ImportEvents(BrowserView):
    """
    """

    def __call__(self):

        context = self.context
        # recupere chaque ligne du fichier voulu (ici 'evenements')

        events_data_file = context[CSV_FILE_NAME]
        events = events_data_file.data.split('\n')
        nb_lines=len(events)

        # liste tous les objets du dossier et creation d'une liste avec leur id

        existing_objects = context.getFolderContents()
        list_objects_id =[]
        for existing_object in existing_objects:
            this_object=existing_object.getObject()
            this_object_id=this_object.getId()
            list_objects_id.append(this_object_id)

        # boucle sur tous les evenements du fichier CSV, on ne veut pas de la ligne 1 (labels) ni de la derniere (vide a cause du dernier '''\n''')

        for event in events[1:nb_lines-1]:

            # Parsing de chaque ligne ==> liste des attributs de l'objet evenement
            event_fields= event.split(';')

            # Supprimer element dont id identique a celui du fichier csv (si existe)
            if event_fields[0] in list_objects_id:
               context.manage_delObjects(event_fields[0])

            # creation de l'evenement, on insere les proprietes de l'evenement selon la structure du fichier CSV de depart

            event_id = event_fields[0]
            
            event_start = convertCSVEntryToDatetimeObject(event_fields[4])
            event_end = convertCSVEntryToDatetimeObject(event_fields[5])

            context.invokeFactory(type_name="Event",
                      id=event_id,
                      title=event_fields[1],
                      description=event_fields[2],
                      location=event_fields[3],

                      start=event_start,
                      end=event_end,

                      timezone=DEFAULT_TIMEZONE,

                      text=event_fields[6],
                      subject=multisubject(event_fields[7]),

                     # effectiveDate=event_fields[8],
                     # expirationDate=event_fields[9],
                     # creation_date=event_fields[10],
                     # modification_date=event_fields[11],
                     
                      creators=(event_fields[12],)
                      )
            evt = context[event_id]
            evt.reindexObject()
 
        return "DONE"


# 4) BrowserView class for importing initial users and groups
        
class QuickAddUsersGroups(BrowserView):
    """
    """

    def __call__(self):
#         if not self.request.get('do-it-really'):
#             # just a guard for accidental calling
#             return '\n'.join([
#                 'you must provide a "do-it-really" in order to flush!',
#             ])

        context = self.context
        
        result = 'ADDING INITIAL USERS AND GROUPS FOR THE SCHOOLSITE\n\n'

        uf = getToolByName(context, 'acl_users')
        gtool = getToolByName(context, 'portal_groups')
        regtool = getToolByName(context, 'portal_registration')
    
        # Initial Site Admin
        properties = {
                 'username': 'siteadmin',
                 'fullname': u"Site Admin",
                 'email': 'siteadmin@schoolsite.com',
               }
        try:
            member = regtool.addMember('siteadmin', 'admin', properties=properties)
            #gtool.addPrincipalToGroup('siteadmin', 'Site Administrators')
            gtool.addPrincipalToGroup('siteadmin', 'Administrators')
            result += '''Added user 'siteadmin' and affected it in 'Administrors' group\n'''
        except ValueError, e:
            # Give user visual feedback what went wrong
            #IStatusMessage(request).addStatusMessage(_(u"Could not create the user:") + unicode(e), "error")
            result += '''Error: Could not create the admin user or add it to the group: %s\n''' % e 
            
        # Useful initial groups and their related test users
        for groupid, memberid in LOCAL_GROUPS: 
            if not uf.searchGroups(id=groupid):
                gtool.addGroup(groupid, title=groupid,
                               roles=[])
                result += 'Added group: %s\n' % groupid
                       
            # Setup a test user as a member of each group
            member_properties = {
                     'username': memberid,
                     'fullname': memberid,
                     'email': memberid + '@schoolsite.com',
                   }
            try:
                # addMember() returns MemberData object
                member = regtool.addMember(memberid, memberid, properties=member_properties)
                result += 'Added member: %s\n' % member.getUserName()
                gtool.addPrincipalToGroup(memberid, groupid)
                result += '--> Added to the group %s\n' % groupid
            except ValueError, e:
                # Give user visual feedback what went wrong
                #IStatusMessage(request).addStatusMessage(_(u"Could not create the user:") + unicode(e), "error")
                result += '''Error: Could not create the user '%s' or add it to the group: %s\n''' % (memberid, e)
                
        print result
        return context.REQUEST.response.redirect(context.absolute_url() + '/webmaster-help')
