from django.test import TestCase

from xf.xf_crud.model_lists import XFModelList
from xf.xf_crud.models import XFCodeTable


class MyTestCase(TestCase):



    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        self.model_list = XFModelList(model=XFCodeTable)
        super().setUp()

    def test_action_list(self):
        self.assertIsNotNone(self.model_list, "Model list for XF Code Table expected")


