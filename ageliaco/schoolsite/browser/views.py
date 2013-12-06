
#from zope import component

from Products.Five.browser import BrowserView

from Products.CMFCore.utils import getToolByName

from ageliaco.schoolsite.config import (
      LOCAL_GROUPS,
)



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
            