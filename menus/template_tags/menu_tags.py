from django import template

from menus.models import MenuItem

register = template.Library()


@register.inclusion_tag('menus/draw_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path

    menu_items = MenuItem.objects.filter(
        menu_name=menu_name
        ).select_related('parent')

    menu_dict = {}
    for item in menu_items:
        if item.parent:
            if item.parent.id not in menu_dict:
                menu_dict[item.parent.id] = []
            menu_dict[item.parent.id].append(item)
        else:
            menu_dict[item.id] = []

    def build_tree(parent_id=None, active_parents=None):
        if active_parents is None:
            active_parents = []
        tree = []
        children = menu_dict.get(parent_id, [])
        for item in children:
            tree.append({
                'item': item,
                'children': build_tree(
                    item.id, active_parents
                    ) if (
                        item in active_parents
                        or item.parent in active_parents
                        ) else []
            })
        return tree

    def find_active_parents(item, parents=None):
        if parents is None:
            parents = []
        parents.append(item)
        if item.parent:
            parents.append(item.parent)
            find_active_parents(item.parent, parents)
        return parents

    active_item = []
    for item in menu_items:
        if item.get_absolute_url() == current_path:
            active_item = item
            break

    active_parents = []
    if active_item:
        active_parents = find_active_parents(active_item)

    return {
        'menu_tree': build_tree(None, active_parents),
        'active_item': active_item,
        'active_parents': active_parents
    }
