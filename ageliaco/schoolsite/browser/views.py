
from datetime import date
from datetime import datetime 

#from zope import component

from Products.Five.browser import BrowserView

from Products.CMFCore.utils import getToolByName

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

from ageliaco.schoolsite.config import (
      LOCAL_GROUPS,
)



## Viewlets

class HeaderViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/portal_header.pt')

    def update(self):
        super(HeaderViewlet, self).update()

        site_url = self.portal_state.portal_url()
        self.site_url = site_url 


class FooterViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/footer.pt')

    def update(self):
        super(FooterViewlet, self).update()
        self.year = date.today().year

        portal = self.portal_state.portal()
        sitemap_setting_container = portal.siteadministration.homepage.footer
        filter = {'portal_type':['Document'], 'review_state':['published']}                                                                                    
        sitemap_setting_items = sitemap_setting_container.getFolderContents(contentFilter = filter)
        self.sitemap_setting_items = sitemap_setting_items






## Views        

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
            gtool.addPrincipalToGroup('siteadmin', 'Site Administrators')
            result += '''Added user 'siteadmin' and affected it in 'Site Administrors' group\n'''
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
                
        return result



class WebmasterHelp(BrowserView):

    def hello(self):
        return "Hello"            
            
            
    def isInitialAdminUserAdded(self):

        context = self.context        
    
        uf = getToolByName(context, 'acl_users')
        #gtool = getToolByName(context, 'portal_groups')

        results = uf.searchUsers(id='siteadmin')
        for res in results:
            if res['userid'] == 'siteadmin':
                #print res['userid']
                return True
        return False
        
    def isInitialGroupsAdded(self):

        context = self.context        
    
        uf = getToolByName(context, 'acl_users')
        #gtool = getToolByName(context, 'portal_groups')

        # For now, for simplicity, we only test the first group created in the initial phase: 'DirectionGroup'
        results = uf.searchGroups(id='DirectionGroup')
        for res in results:
            if res['groupid'] == 'DirectionGroup':
                #print res['groupid']
                return True
        return False
        





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

def getDateParts(datestring):
    # date parts from a string of the form: 08/26/2013 07:30
    first_split = datestring.split(' ')
    date = first_split[0]
    hour_and_min = first_split[1]

    second_split = date.split('/')
    month = second_split[0]
    day = second_split[1]
    year = second_split[2]

    third_split = hour_and_min.split(':')
    hour = third_split[0]
    min = third_split[1]

    return int(year), int(month), int(day), int(hour), int(min)



class ImportEvents(BrowserView):
    """
    """

    def __call__(self):

        context = self.context
        # recupere chaque ligne du fichier voulu (ici 'evenements')

        events = context.evenements.data.split('\n')
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

            event_start_datestr = event_fields[4]
            event_start_dateparts = getDateParts(event_start_datestr)
            event_start = datetime(event_start_dateparts[0],
                                   event_start_dateparts[1],
                                   event_start_dateparts[2],
                                   event_start_dateparts[3],
                                   event_start_dateparts[4])

            event_end_datestr = event_fields[5]
            event_end_dateparts = getDateParts(event_end_datestr)
            event_end = datetime(event_end_dateparts[0],
                                   event_end_dateparts[1],
                                   event_end_dateparts[2],
                                   event_end_dateparts[3],
                                   event_end_dateparts[4])

            #print "%s, %s" % (event_start_str, event_end_str)

            context.invokeFactory(type_name="Event",
                      id=event_id,
                      title=event_fields[1],
                      description=event_fields[2],
                      location=event_fields[3],

                      #startDate=event_fields[4],
                      #endDate=event_fields[5],

                      start=event_start,
                      end=event_end,

                      timezone="Europe/Vienna",

                      text=event_fields[6],
                      subject=multisubject(event_fields[7]),

                     # effectiveDate=event_fields[8],
                     # expirationDate=event_fields[9],
                     # creation_date=event_fields[10],
                     # modification_date=event_fields[11],
                     # creators=event_fields[12]
                      )
            evt = context[event_id]
            evt.reindexObject()
 
        return "DONE"
