
from datetime import date
from datetime import datetime 

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from Products.Five.browser import BrowserView

from Products.CMFCore.utils import getToolByName

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

from ageliaco.schoolsite.config import (
      LOCAL_GROUPS,
      LIENS_INSTITUTIONNELS,
)

from ageliaco.schoolsite.interfaces import (
      ISchoolSiteSettings,
)



## Viewlets

class HeaderViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/portal_header.pt')

    def update(self):
        super(HeaderViewlet, self).update()

        site_url = self.portal_state.portal_url()
        self.site_url = site_url 

        # Get Impressum URL (via portal_registry)
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISchoolSiteSettings)
        self.impressum_page_url = settings.impressum_page_url
        #print self.impressum_page_url


# class FooterViewlet(ViewletBase):
#     index = ViewPageTemplateFile('templates/footer.pt')
# 
#     def update(self):
#         super(FooterViewlet, self).update()
#         self.year = date.today().year
# 
#         portal = self.portal_state.portal()
#         sitemap_setting_container = portal.siteadministration.homepage.footer
#         filter = {'portal_type':['Document'], 'review_state':['published']}                                                                                    
#         sitemap_setting_items = sitemap_setting_container.getFolderContents(contentFilter = filter)
#         self.sitemap_setting_items = sitemap_setting_items






## Views        

class SchoolSiteLinks(BrowserView):
    # View for the "Liens institutionnels" page
    
    def links(self):
        return LIENS_INSTITUTIONNELS 
        
#     def link_icon(self, category):
#         icon_type = 'external-link'
#         if category == 'Brochure':
#             icon_type = 'book'
#    
#         return icon_type

    def otherLinksFolders(self):
        return self.context.getFolderContents({'portal_type': 'Folder'})

        
        
        
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
        


