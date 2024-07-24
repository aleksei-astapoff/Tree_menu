from django import template
from menus.models import MenuItem

register = template.Library()


@register.inclusion_tag('menus/draw_menu.html', takes_context=True)
def draw_menu(context, menu_name) -> dict:
    """
    Функция для построения дерева меню
    Принемает:
    :param context: контекст
    :param menu_name: название меню
    Возвращае словарь:
    :return: tree - дерево меню
    :return: current_path - текущий путь
    :return: active_item - активный пункт меню
    :return: active_parents - родители активного пункта меню
    """

    request = context['request']
    current_path = request.path

    # Запрос для получения всех элементов меню
    menu_items = MenuItem.objects.filter(
        menu_name=menu_name
        ).select_related('parent')

    # Словарь для хранения пунктов меню по их ID
    menu_dict = {}
    for item in menu_items:
        item.children_list = []
        menu_dict[item.id] = item

    for item in menu_items:
        if item.parent_id:
            menu_dict[item.parent_id].children_list.append(item)

    def build_tree(item, active_parents) -> dict:
        """
        Функция для построения дерева меню
        Принемает:
        :param item: элемент меню
        :param active_parents: активные родители
        Возвращае словарь:
        :return: tree - дерево меню
        """
        tree = {
            'item': item,
            'children': []
        }

        # Разворачиваем если элемент в активных родителях или сам активный.
        if item in active_parents or item == active_item:
            for child in item.children_list:
                tree['children'].append(build_tree(child, active_parents))

        # Разворачиваем первый уровень вложенности под активным элементом
        elif item == active_item:
            for child in item.children_list:
                tree['children'].append({'item': child, 'children': []})
        return tree

    def find_active_parents(item, parents=None) -> list:
        """
        Функция для поиска родителей активного пункта меню
        Принемает:
        :param item: элемент меню
        :param parents: родители
        Возвращае список:
        :return: parents - родители активного пункта меню
        """
        if parents is None:
            parents = []
        parents.append(item)
        if item.parent:
            find_active_parents(item.parent, parents)
        return parents

    # Определяем активный пункт меню
    active_item = None
    for item in menu_items:
        if item.get_absolute_url() == current_path:
            active_item = item
            break

    # Определяем родителей активного пункта меню
    active_parents = []
    if active_item:
        active_parents = find_active_parents(active_item)

    # Строим дерево меню
    menu_tree = []
    for item in menu_items:
        if not item.parent:
            menu_tree.append(build_tree(item, active_parents))

    return {
        'menu_tree': menu_tree,
        'current_path': current_path,
        'active_item': active_item,
        'active_parents': active_parents
        }
