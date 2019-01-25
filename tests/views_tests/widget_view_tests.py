import ast
from django.db import connections
from typing import Sequence, Any

from xf.tests.xf_test_case_data import XFTestCaseData
from xf.uc_dashboards.models import Page
from xf.uc_dashboards.models.dataset import DataSet
from xf.uc_dashboards.views.custom_dataset_loader_base import XFCustomDataSetLoaderBase


class WidgetViewTestCase(XFTestCaseData):

    def test_get_context_data(self):

        test_data = self._generate_widget_view_test_data()

        view = test_data['widget_view']
        view.widget = test_data['table_listing_home_page']

        request = self.generate_request(path='/?thetitle=Home Page', user=test_data['user'])
        request = self.setup_request(request, test_data['user'])
        view.request = request

        context = view.get_context_data()

        self.assertEqual(len(view.data_columns), 2, "expected two data columns")
        self.assertTrue(view.data_columns[0]['column_name'] == 'slug', 'expected column name as slug')
        self.assertTrue(view.data_columns[0]['table_column_caption'] == 'The slug',
                        'expected column caption not returned')
        self.assertTrue(view.data_columns[0]['table_column_width'] == '10%', 'expected column width not returned')

        all_pages = Page.objects.count()
        self.assertTrue(all_pages > 1, "There are more than one pages in the database")

        self.assertEqual(len(context['rows']), 1, "Expected only 1 row for the home page returned from database")
        self.assertTrue(context['rows'][0]['title'] == 'Home Page',
                        "Expected the page returned to have title 'Home Page'")
        self.assertTrue(context['rows'][0]['slug'] == 1)

        self.assertTrue(context['paging'] == 'yes', "We should have a context variable called 'paging'")

    def test_get_context_data_from_sql_dataset(self):

        test_data = self._generate_widget_view_test_data()

        view = test_data['widget_view']
        widget = test_data['table_listing_home_page']
        widget.sql_query = widget.filters = widget.database_key = ''

        home_page_dataset = test_data['home_page_dataset']
        widget.dataset = home_page_dataset
        widget.save()
        view.widget = widget

        request = self.generate_request(path='/?thetitle=Home Page')
        request = self.setup_request(request, test_data['user'])
        view.request = request

        context = view.get_context_data()

        self.assertEqual(len(view.data_columns), 2, "expected two data columns")
        self.assertTrue(view.data_columns[0]['column_name'] == 'slug', 'expected column name as slug')
        self.assertTrue(view.data_columns[0]['table_column_caption'] == 'The slug',
                        'expected column caption not returned')
        self.assertTrue(view.data_columns[0]['table_column_width'] == '10%', 'expected column width not returned')

        all_pages = Page.objects.count()
        self.assertTrue(all_pages > 1, "There are more than one pages in the database")

        self.assertEqual(len(context['rows']), 1, "Expected only 1 row for the home page returned from database")
        self.assertTrue(context['rows'][0]['title'] == 'Home Page',
                        "Expected the page returned to have title 'Home Page'")
        self.assertTrue(context['rows'][0]['slug'] == "home")

        self.assertTrue(context['paging'] == 'yes', "We should have a context variable called 'paging'")

    def test_get_context_data_from_custom_dataset(self):

        test_data = self._generate_widget_view_test_data()

        view = test_data['widget_view']
        widget = test_data['table_listing_home_page']
        widget.sql_query = widget.filters = widget.database_key = ''

        home_page_custom_dataset = test_data['home_page_custom_dataset']
        widget.dataset = home_page_custom_dataset
        widget.save()
        view.widget = widget

        request = self.generate_request(path='/?thetitle=Home Page')
        request = self.setup_request(request, test_data['user'])
        view.request = request

        context = view.get_context_data()

        self.assertEqual(len(view.data_columns), 2, "expected two data columns")
        self.assertTrue(view.data_columns[0]['column_name'] == 'slug', 'expected column name as slug')
        self.assertTrue(view.data_columns[0]['table_column_caption'] == 'The slug',
                        'expected column caption not returned')
        self.assertTrue(view.data_columns[0]['table_column_width'] == '10%', 'expected column width not returned')

        all_pages = Page.objects.count()
        self.assertTrue(all_pages > 1, "There are more than one pages in the database")

        self.assertEqual(len(context['rows']), 1, "Expected only 1 row for the home page returned from database")
        self.assertTrue(context['rows'][0]['title'] == 'Home Page',
                        "Expected the page returned to have title 'Home Page'")
        self.assertTrue(context['rows'][0]['slug'] == 1)

        self.assertTrue(context['paging'] == 'yes', "We should have a context variable called 'paging'")

    def test_load_custom_dataset_class(self):

        test_data = self._generate_widget_view_test_data()
        class_full_name = 'xf.tests.views_tests.widget_view_tests.TestableCustomDataSetLoader'

        view = test_data['widget_view']
        loaded_class = view._load_custom_dataset_class(class_full_name)

        self.assertTrue(loaded_class == TestableCustomDataSetLoader, "Expected TestableCustomDataSetLoader class "
                                                                     "to be loaded")

    def test_data_columns_for_template(self):

        test_data = self._generate_widget_view_test_data()
        view = test_data['widget_view']

        two_column_widget = test_data['table_listing_home_page']
        two_column_widget.sql_query = two_column_widget.filters = \
            two_column_widget.database_key = two_column_widget.filters = ''
        two_column_widget.data_columns = \
            "'column_name': 'slug', 'table_column_caption': 'The slug', 'table_column_width': '10%',\n" \
            " 'column_name': 'title', 'table_column_caption': 'The title', 'table_column_width': '10%',"

        seven_column_dataset = test_data['home_page_custom_dataset']
        two_column_widget.dataset = seven_column_dataset
        two_column_widget.save()
        view.widget = two_column_widget

        request = self.generate_request(path='/')
        request = self.setup_request(request, test_data['user'])
        view.request = request

        context = view.get_context_data()

        for row in context['rows']:
            self.assertTrue('title' in row, "Expected the page returned to have title 'Home Page'")
            self.assertTrue('slug' in row)

        self.assertTrue(context['paging'] == 'yes', "We should have a context variable called 'paging'")


class TestableCustomDataSetLoader(XFCustomDataSetLoaderBase):

    def load_dataset(self, dataset: DataSet, request, **kwargs) -> Sequence[Any]:

        conn = connections[dataset.database_key]
        filters = ast.literal_eval(dataset.filters)

        with conn.cursor() as cursor:
            cursor.execute("select * from uc_dashboards_page where title=%s", [request.GET.get(filters[0])])
            rows = cursor.fetchall()

        return rows
