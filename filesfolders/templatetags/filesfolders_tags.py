from django import template

# Projectroles dependency
from projectroles.project_settings import get_project_setting

from ..models import File, Folder, HyperLink, FILESFOLDERS_FLAGS


APP_NAME = 'filesfolders'


register = template.Library()


@register.filter
def get_class(obj):
    return obj.__class__.__name__


@register.filter
def force_wrap(obj, length):
    # If string contains spaces, leave wrapping to browser
    if obj.find(' ') == -1 and len(obj) > length:
        return '<wbr />'.join(
            [obj[i:i + length] for i in range(0, len(obj), length)])

    return obj


@register.simple_tag
def get_details_items(project):
    """Return recent files/links for card on project details page"""
    files = File.objects.filter(
        project=project).order_by('-date_modified')[:5]
    links = HyperLink.objects.filter(
        project=project).order_by('-date_modified')[:5]
    ret = list(files) + list(links)
    ret.sort(key=lambda x: x.date_modified, reverse=True)
    return ret[:5]


@register.simple_tag
def allow_public_links(project):
    """Return the boolean value for allow_public_links in project settings"""
    return get_project_setting(project, APP_NAME, 'allow_public_links')


@register.simple_tag
def find_filesfolders_items(search_term, user, search_type, keywords):
    """Return files, folders and/or links based on a search term, user and
    possible type/keywords"""
    ret = None

    if not search_type:
        files = File.objects.find(search_term, keywords)
        folders = Folder.objects.find(search_term, keywords)
        links = HyperLink.objects.find(search_term, keywords)
        ret = list(files) + list(folders) + list(links)
        ret.sort(key=lambda x: x.name.lower())

    elif search_type == 'file':
        ret = File.objects.find(search_term, keywords).order_by('name')

    elif search_type == 'folder':
        ret = Folder.objects.find(search_term, keywords).order_by('name')

    elif search_type == 'link':
        ret = HyperLink.objects.find(search_term, keywords).order_by('name')

    if ret:
        ret = [
            x for x in ret if
                user.has_perm('filesfolders.view_data', x.project)]
        return ret

    return None


@register.simple_tag
def get_file_icon(file):
    mt = file.file.file.mimetype

    if mt == 'application/pdf':
        return 'file-pdf-o'

    elif mt == 'application/vnd.openxmlformats-officedocument.' \
               'presentationml.presentation':
        return 'file-powerpoint-o'

    elif 'compressed' in mt or 'zip' in mt:
        return 'file-archive-o'

    elif ('excel' in mt or
            mt == 'application/vnd.openxmlformats-'
                  'officedocument.spreadsheetml.sheet'):
        return 'file-excel-o'

    elif 'image/' in mt:
        return 'file-image-o'

    elif 'text/' in mt:
        return 'file-text-o'

    # Default if not found
    return 'file-o'


@register.simple_tag
def get_flag(item):
    if not item.flag:
        return''

    f = FILESFOLDERS_FLAGS[item.flag]

    return '<i class="fa fa-{} fa-fw text-{} omics-ff-flag-icon" ' \
           'title="{}" data-toggle="tooltip" data-placement="top">' \
           '</i>'.format(
                f['icon'], f['color'], f['label'])