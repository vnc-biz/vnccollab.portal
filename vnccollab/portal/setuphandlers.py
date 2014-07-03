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


def initial_setup(context):
    """Initial set up after add-oninstallation."""
    if context.readDataFile('vnccollab.portal.txt') is None:
        # our add-on isn't being intalled
        return

    portal = api.portal.get()
    tinymce_allow_color_style(portal)
    tinymce_allow_flash(portal)
    configure_homepage(portal)
    disable_self_registration(portal)
    enable_user_folders(portal)
    setup_async_quota(portal)
    configure_languages(portal)
    uninstall_kupu()
    set_external_editor()


def tinymce_allow_color_style(context):
    """Allows style in tinyMCE attributes."""
    html_filter = IFilterSchema(context)
    attrs = html_filter.stripped_attributes

    if 'style' in attrs:
        attrs.pop(attrs.index('style'))
        html_filter.stripped_attributes = attrs
    styles = html_filter.style_whitelist

    if 'color' not in styles:
        html_filter.style_whitelist = list(styles) + ['color']


def tinymce_allow_flash(context):
    """Allows flash content in tinyMCE."""
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


def configure_homepage(portal):
    """Removes default_page property from portal, disabling home page."""
    remove_property(portal, 'default_page')


def enable_user_folders(portal):
    """Enables User Folders."""
    schema = SecurityControlPanelAdapter(portal)
    schema.enable_user_folders = True


def disable_self_registration(portal):
    """Disables User self-registration."""
    schema = SecurityControlPanelAdapter(portal)
    schema.enable_self_reg = False


def enable_self_registration(portal):
    """Enables User self-registration."""
    app_perms = portal.rolesOfPermission(permission='Add portal member')
    reg_roles = []
    for appperm in app_perms:
        if appperm['selected'] == 'SELECTED':
            reg_roles.append(appperm['name'])
    if 'Anonymous' not in reg_roles:
        portal.manage_permission('Add portal member',
                                 roles=reg_roles + ['Anonymous'], acquire=0)


def setup_async_quota(portal):
    """Set default Quota for async jobs queue."""
    if IAsyncService is None:
        return

    queue = getUtility(IAsyncService).getQueues()['']
    if QUOTA_NAME not in queue.quotas:
        settings = GlobalSettings(portal)
        queue.quotas.create(QUOTA_NAME, size=settings.async_quota_size)


def configure_languages(portal):
    """Configures languages."""
    langs = getToolByName(portal, 'portal_languages')

    # no flags
    langs.display_flags = 0

    # we need en and de, en is default
    langs.manage_setLanguageSettings('en', ['en', 'de'], setCookieN=True,
                                     setUseCombinedLanguageCodes=False)


def clean_registry(portal, reg_id):
    """Cleans Registry Resource."""
    if portal.readDataFile('vnccollab.portal.txt') is None:
        return

    reg = getToolByName(portal, reg_id)
    reg.clearResources()


def clean_css_registry(context):
    """Cleans CSS registry."""
    clean_registry(context, 'portal_css')


def clean_js_registry(context):
    """Cleans JS registry."""
    clean_registry(context, 'portal_javascripts')


def clean_kss_registry(context):
    """Cleans KSS registry."""
    clean_registry(context, 'portal_kss')


def disable_virtual_groups(context):
    """Disables auto group plugins."""
    activatable = ['IGroupEnumerationPlugin',
                   'IGroupsPlugin',
                   'IPropertiesPlugin']
    set_autogroup_plugin(context, activatable)


def enable_virtual_groups(context):
    """Enables auto group plugins."""
    activatable = ['IGroupEnumerationPlugin',
                   'IGroupIntrospection',
                   'IGroupsPlugin',
                   'IPropertiesPlugin']
    set_autogroup_plugin(context, activatable)


def set_autogroup_plugin(context, activatable):
    """Enables auto group plug-in."""
    pas = context.acl_users
    plugin = 'members_auto_group_plugin'
    plugin_obj = pas.get(plugin)
    if plugin_obj:
        plugin_obj.manage_activateInterfaces(activatable)


def uninstall_kupu():
    """Uninstall kupu, if present"""
    try:
        uninstall_product('kupu')
    except AttributeError:
        # We started with a plone version without kupu
        pass

def set_external_editor():
    """Enables External Editor for all users."""
    mtool = api.portal.get_tool('portal_membership')
    for user in mtool.listMembers():
        try:
            user.setMemberProperties({'ext_editor': True})
        except:
            pass

# support

def remove_property(obj, pname):
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


def set_property(obj, pname, ptype, value):
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


def uninstall_product(name):
    """Uninstall the given product."""
    installer = api.portal.get_tool('portal_quickinstaller')
    installer.uninstallProducts([name])

