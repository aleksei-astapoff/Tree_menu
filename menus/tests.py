from django.test import TestCase, RequestFactory
from django.template import Context, Template
from django.core.management import call_command


class DrawMenuTagTest(TestCase):
    """
    Тесты тега draw_menu (отрисовка меню).
    А также тесты на развертывание меню, поиска активного пункта
    в меню. Отрисовка меню с вложенными пунктами. Согласно ТЗ
    """
    def setUp(self) -> None:
        """
        Загружаем тестовые данные,
        После тестирования данные удаляются автоматически.
        """

        self.factory = RequestFactory()
        call_command('loaddata', 'test_data.json', verbosity=0)

    def render_template(self, template_string, context) -> str:
        """
        Функция для отрисовки шаблона
        Принемает параметры:
        :param template_string: шаблон
        :param context: контекст
        Возвращае строку:
        :return: отрисованный шаблон
        """

        template = Template(template_string)
        return template.render(Context(context))

    def test_draw_menu_with_active_item(self) -> None:
        """Тестирование отрисовки меню с активным пунктом."""

        request = self.factory.get('/services/web-development/')
        context = {'request': request}
        rendered = self.render_template(
            "{% load menu_tags %}{% draw_menu 'main_menu' %}", context
        )

        self.assertIn(
            'href="/services/web-development/" class="active"', rendered
            )
        self.assertIn('href="/services/"', rendered)
        self.assertIn('<ul>', rendered)
        self.assertIn('href="/services/seo/"', rendered)
        self.assertIn('href="/services/marketing/"', rendered)
        self.assertNotIn('href="/services/seo/level-2/"', rendered)

    def test_draw_menu_with_nested_active_item(self) -> None:
        """Тестирование отрисовки меню с вложенными активными пунктами."""

        request = self.factory.get('/services/seo/')
        context = {'request': request}
        rendered = self.render_template(
            "{% load menu_tags %}{% draw_menu 'main_menu' %}", context
        )

        self.assertIn('href="/services/seo/" class="active"', rendered)
        self.assertIn('href="/services/"', rendered)
        self.assertIn('<ul>', rendered)
        self.assertIn('href="/services/seo/level-2/"', rendered)
        self.assertNotIn('href="/services/seo/level-3/"', rendered)

    def test_draw_menu_with_top_level_active_item(self) -> None:
        """Тестирование отрисовки меню с активным первым уровнем пункта."""

        request = self.factory.get('/services/')
        context = {'request': request}
        rendered = self.render_template(
            "{% load menu_tags %}{% draw_menu 'main_menu' %}", context
        )

        self.assertIn('href="/services/" class="active"', rendered)
        self.assertIn('<ul>', rendered)
        self.assertIn('href="/services/web-development/"', rendered)
        self.assertIn('href="/services/seo/"', rendered)
        self.assertIn('href="/services/marketing/"', rendered)
        self.assertNotIn('href="/services/seo/level-2/"', rendered)

    def test_draw_menu_with_non_active_item(self) -> None:
        """Тестирование отрисовки меню с неактивным пунктом."""

        request = self.factory.get('/about/')
        context = {'request': request}
        rendered = self.render_template(
            "{% load menu_tags %}{% draw_menu 'main_menu' %}", context
        )

        # Проверяем, что неактивный элемент не развернут
        self.assertIn('href="/about/"', rendered)
        self.assertIn('class="active"', rendered)

        # Проверка наличия <ul> только после активного элемента
        about_index = rendered.index('href="/about/"')
        ul_index = rendered.find('<ul>', about_index)
        self.assertEqual(ul_index, -1)

    def test_draw_multiple_menus(self) -> None:
        """Тестирование отрисовки двух меню на одной странице."""

        request = self.factory.get('/services/web-development/')
        context = {'request': request}
        template_string = '''
            {% load menu_tags %}
            {% draw_menu "main_menu" %}
            {% draw_menu "secondary_menu" %}
        '''
        rendered = self.render_template(template_string, context)

        self.assertIn(
            'href="/services/web-development/" class="active"', rendered
            )
        self.assertIn('href="/overview/"', rendered)
        self.assertIn('href="/team/"', rendered)

    def test_single_query(self) -> None:
        """
        Тестирование запросов к базе данных.
        Проверяем количество запрошенных запросов, не более одного.
        """
        request = self.factory.get('/services/web-development/')
        context = {'request': request}
        template_string = '''
            {% load menu_tags %}
            {% draw_menu "main_menu" %}
        '''

        with self.assertNumQueries(1):
            self.render_template(template_string, context)
