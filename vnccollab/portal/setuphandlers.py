from zope.component import getUtility
from OFS.interfaces import IPropertyManager

from plone import api
from plone.app.controlpanel.filter import IFilterSchema
from plone.app.controlpanel.security import SecurityControlPanelAdapter

from Products.CMFCore.utils import getToolByName

from collective.documentviewer.async import QUOTA_NAME
from collective.documentviewer.settings import GlobalSettings

try:
    # AsyncService only for zeo deploymnet
    from plone.app.async.interfaces import IAsyncService
except ImportError:
    IAsyncService = None


def initialSetup(context):
    if context.readDataFile('vnccollab.portal.txt') is None:
        # our add-on isn't being intalled
        return

    portal = api.portal.get()
    tinymce_allow_color_style(portal)
    tinymce_allow_flash(portal)
    configureHomePage(portal)
    disableSelfRegistration(portal)
    enableUserFolders(portal)
    setupDashboard(portal)
    configureAsyncQuota(portal)
    configureLanguages(portal)


def tinymce_allow_color_style(context):
    html_filter = IFilterSchema(context)
    attrs = html_filter.stripped_attributes

    if 'style' in attrs:
        attrs.pop(attrs.index('style'))
        html_filter.stripped_attributes = attrs
    styles = html_filter.style_whitelist

    if 'color' not in styles:
        html_filter.style_whitelist = list(styles) + ['color']


def tinymce_allow_flash(context):
    html_filter = IFilterSchema(context)
    tags = html_filter.nasty_tags

    if 'applet' in tags:
        tags.pop(tags.index('applet'))
    if 'embed' in tags:
        tags.pop(tags.index('embed'))
    if 'object' in tags:
        tags.pop(tags.index('object'))
    if 'param' in tags:
        tags.pop(tags.index('param'))

    html_filter.nasty_tags = tags
    tags = html_filter.stripped_tags

    if 'applet' in tags:
        tags.pop(tags.index('applet'))
    if 'embed' in tags:
        tags.pop(tags.index('embed'))
    if 'object' in tags:
        tags.pop(tags.index('object'))
    if 'param' in tags:
        tags.pop(tags.index('param'))

    html_filter.stripped_tags = tags


def configureHomePage(portal):
    removeProperty(portal, 'default_page')


def disableSelfRegistration(portal):
    schema = SecurityControlPanelAdapter(portal)
    schema.enable_self_reg = False


def enableUserFolders(portal):
    schema = SecurityControlPanelAdapter(portal)
    schema.enable_user_folders = True


def enableSelfRegistration(portal):
    app_perms = portal.rolesOfPermission(permission='Add portal member')
    reg_roles = []
    for appperm in app_perms:
        if appperm['selected'] == 'SELECTED':
            reg_roles.append(appperm['name'])
    if 'Anonymous' not in reg_roles:
        portal.manage_permission('Add portal member',
                                 roles=reg_roles + ['Anonymous'], acquire=0)


def setupDashboard(portal):
    # configure dashboard
    #  * create dashboard folder in private state
    #  * exclude from navigation
    #  * add Reader role for Loggin-in users
    #  * add layout property set to 'dashboard' view
    if 'dashboard' not in portal.objectIds():
        portal.invokeFactory('Folder', 'dashboard', title='Dashboard')
        dashboard = portal.dashboard
        dashboard.update(excludeFromNav=True)
        setProperty(dashboard, 'layout', 'string', 'dashboard')

        # set local roles
        dashboard.manage_setLocalRoles('AuthenticatedUsers',
                                       ['Reader'])
        dashboard.reindexObjectSecurity()


def configureAsyncQuota(portal):
    # set default Quota for async jobs queue
    if IAsyncService is None:
        return

    queue = getUtility(IAsyncService).getQueues()['']
    if QUOTA_NAME not in queue.quotas:
        settings = GlobalSettings(portal)
        queue.quotas.create(QUOTA_NAME, size=settings.async_quota_size)


def configureLanguages(portal):
    langs = getToolByName(portal, 'portal_languages')

    # no flags
    langs.display_flags = 0

    # we need en and de, en is default
    langs.manage_setLanguageSettings('en', ['en', 'de'], setCookieN=True,
                                     setUseCombinedLanguageCodes=False)


def cleanRegistry(context, reg_id):
    if context.readDataFile('vnccollab.portal.txt') is None:
        return

    portal = context.getSite()
    reg = getToolByName(portal, reg_id)
    reg.clearResources()


def cleanCSSRegistry(context):
    cleanRegistry(context, 'portal_css')


def cleanJSRegistry(context):
    cleanRegistry(context, 'portal_javascripts')


def cleanKSSRegistry(context):
    cleanRegistry(context, 'portal_kss')


def disableVirtualGroupsOnCreation(context):
    activatable = ['IGroupEnumerationPlugin',
                   'IGroupsPlugin',
                   'IPropertiesPlugin']
    setAutoGroupPlugin(context, activatable)


def enableVirtualGroupsOnCreation(context):
    activatable = ['IGroupEnumerationPlugin',
                   'IGroupIntrospection',
                   'IGroupsPlugin',
                   'IPropertiesPlugin']
    setAutoGroupPlugin(context, activatable)


def setAutoGroupPlugin(context, activatable):
    pas = context.acl_users
    plugin = 'members_auto_group_plugin'
    plugin_obj = pas.get(plugin)
    if plugin_obj:
        plugin_obj.manage_activateInterfaces(activatable)


# support

def removeProperty(obj, pname):
    """Removes given property (IPropertyManager interface) by name from
    object.

    Returns True on successfull removal.
    """
    if not IPropertyManager.providedBy(obj):
        return False

    if not obj.hasProperty(pname):
        return False

    obj.manage_delProperties(ids=[pname])
    return True


def setProperty(obj, pname, ptype, value):
    """Adds or updates given property of a given type to given object using
    IPropertyManager interface.

    Returns True on successfull addition.
    """
    if not IPropertyManager.providedBy(obj):
        return False

    if obj.hasProperty(pname):
        # update existing one
        obj.manage_changeProperties(**{pname:value})
    else:
        # otherwise add a new one
        obj.manage_addProperty(pname, value, ptype)

    return True
