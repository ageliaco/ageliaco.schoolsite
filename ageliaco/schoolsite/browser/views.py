
from datetime import date
from datetime import datetime 

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from Products.Five.browser import BrowserView

from Products.CMFCore.utils import getToolByName

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

from ageliaco.schoolsite.config import (
      DOCUMENTATION_SITE_URL,
)

#from ageliaco.schoolsite.links_config import (
#      INSTITUTIONNELS,
#      REGLEMENTS,
#      PLANS_ETUDES_PROGRAMMES,
#)

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



## Views        

class MainTemplateFullWidth(BrowserView):
    
    pass      


class FullWidthSlider(BrowserView):
    
    pass      



class SchoolSiteLinks(BrowserView):
    # View for the links collections. One of the use cases is for the "Liens institutionnels" page.
    
#     def showInstitutionLinks(self):
#         links = []
#         context = self.context
#         
#         if context.getId() == 'liens-institutionnels':
#             links = INSTITUTIONNELS['commun']
#         return links
        
    def contextualLinks(self):
        return self.context.getFolderContents({'portal_type': 'Link'})
        
        
    #def subFolders(self):
    #    return self.context.getFolderContents({'portal_type': 'Folder'})

        
class WebmasterHelp(BrowserView):

    def hello(self):
        return "Hello"            


    def documentationSiteURL(self):
        return DOCUMENTATION_SITE_URL


    def isFooterContentsAdded(self):

        context = self.context

        if not 'doormat' in context.objectIds():  
            return False
        dm = context.doormat
        if len(dm.objectIds('DoormatColumn')) < 2:
            return False
        return True


#     def isLiensInstitutionnelsFolderAdded(self):
# 
#         context = self.context
# 
#         if not 'presentation' in context.objectIds('Dexterity Container'):  
#             return False
#         about_folder = context.presentation
#         if not 'liens-institutionnels' in about_folder.objectIds('Dexterity Container'):
#             return False
#         return True
            
            
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
        


