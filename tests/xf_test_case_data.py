import uuid
from django.contrib.auth.models import Permission, User, Group
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.test import RequestFactory

from xf.tests.xf_test_case import XFTestCase
from xf.uc_dashboards.models import Page, Widget, Template
from xf.uc_dashboards.models.dataset import DataSet
from xf.uc_dashboards.views.widget_view import WidgetView
from xf.xf_crud.model_forms import XFModelForm
from xf.xf_crud.permission_mixin import XFPermissionMixin


class XFTestCaseData(XFTestCase):

    def _generate_permissions_test_data(self):

        test_data = {}

        class TestClassExtendsMixin(XFPermissionMixin):
            def __init__(self, model: Model):
                self.request =  RequestFactory().get('/')
                self.context = {}
                self.model = model
            def set_requesting_user(self, user: User):
                self.request.user = user
            class Meta:
                model = Page

        class TestForm(XFModelForm):
            class Meta:
                model = Page
                fields = '__all__'

        test_data['model_class'] = Page
        test_data['model_instance'] = Page.objects.first()
        test_data['permission_mixin_class'] = TestClassExtendsMixin
        test_data['user'] = self.generate_user()
        test_data['user_group'], created = Group.objects.get_or_create(name='Test')
        test_data['user_group_1'], created = Group.objects.get_or_create(name='Test 1')
        test_data['user_group_2'], created = Group.objects.get_or_create(name='Test 2')
        test_data['class_instance'] = TestClassExtendsMixin(Page)
        test_data['model_content_type'] = ContentType.objects.filter(model='page', app_label='uc_dashboards').first()
        test_data['model_delete_permission'], created = Permission.objects.get_or_create(
            content_type=test_data['model_content_type'],
            codename='delete_page',
            defaults={'name': "Can delete page"},
        )

        test_data['model_form'] = TestForm
        test_data['model_form_instance'] = TestForm()

        return test_data

    def _generate_widget_view_test_data(self):
        test_data = {}

        template = Template(
            name='Table template',
        )
        template.save()

        table_widget = Widget(
            title='Table data',
            slug='table-data',
            widget_type=Widget.TABLE,
            sql_query="select * from uc_dashboards_page where title=@thetitle",
            filters="'thetitle',",
            database_key='default',
            data_columns="'column_name' : 'slug', 'table_column_caption': 'The slug', 'table_column_width': '10%',\n"
                         "'column_name' : 'title', 'table_column_caption': 'The title', 'table_column_width': '10%',",
            custom_attributes="'paging':'yes',",
            allow_anonymous=False,
            template_id=template.id
        )
        table_widget.save()

        test_data['template'] = template
        test_data['table_listing_home_page'] = table_widget
        test_data['user'] = self.generate_user()

        home_page_dataset = DataSet(
            name='Dataset with homepage data',
            code=str(uuid.uuid4()),
            dataset_type=DataSet.SQL,
            sql_query="select slug, title, main_title, text, page_id, allow_anonymous, about "
                      "from uc_dashboards_page "
                      "where title=@thetitle",
            filters="'thetitle',",
            database_key='default',
            custom_attributes="'paging':'yes',",
            allow_anonymous=False,
            data_columns="'column_name' : 'slug', 'table_column_caption': 'The slug',\n"
                         "'column_name' : 'title', 'table_column_caption': 'The title',\n"
                         "'column_name' : 'main_title', 'table_column_caption': 'Main title',\n"
                         "'column_name' : 'text', 'table_column_caption': 'The text',\n"
                         "'column_name' : 'page_id', 'table_column_caption': 'Page ID',\n"
                         "'column_name' : 'allow_anonymous', 'table_column_caption': 'Open?',\n"
                         "'column_name' : 'about', 'table_column_caption': 'About',"
        )
        home_page_dataset.save()
        test_data['home_page_dataset'] = home_page_dataset

        home_page_custom_dataset = DataSet(
            name='Custom dataset with homepage data',
            code=str(uuid.uuid4()),
            dataset_type=DataSet.CUSTOM,
            custom_daset_loader="xf.tests.views_tests.widget_view_tests.TestableCustomDataSetLoader",
            filters="'thetitle',",
            database_key='default',
            custom_attributes="'paging':'yes',",
            allow_anonymous=False
        )
        home_page_custom_dataset.save()
        test_data['home_page_custom_dataset'] = home_page_custom_dataset

        view = WidgetView()
        view.perspective = None
        view.kwargs = {}
        test_data['widget_view'] = view

        return test_data
