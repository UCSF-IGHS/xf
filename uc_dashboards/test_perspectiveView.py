from django.test import TestCase
#from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings


#import os

#os.environ['DJANGO_SETTINGS_MODULE'] = 'mainsite.settings.dev'
from xf.uc_dashboards.models import Perspective


class TestPerspectiveView(TestCase):
    fixtures = ['test_fixtures/auth.json', 'test_fixtures/uc_dashboards.json', ]

    def setUp(self):
        # Test definitions as before.
        self.national_perspective = Perspective.objects.get(id=2)
        self.assertEqual(self.national_perspective.id, 2)
        self.district_perspective = Perspective.objects.get(id=3)
        self.assertEqual(self.district_perspective.id, 3)

        self.national_user = User.objects.get(id=3)
        self.assertEqual(self.national_user.id, 3)
        self.district_user = User.objects.get(id=5)
        self.assertEqual(self.district_user.id, 5)

        self.natdis_user = User.objects.get(id=7)
        self.assertEqual(self.natdis_user.username, "natdis")

        self.admin_user = User.objects.get(username='admin')
        self.assertTrue(self.admin_user.is_superuser)

        return


    def test_load_perspectives(self):

        'Loading the district user 5, which has one perspective'
        self.assertEqual(self.district_user.id, 5)
        self.district_user.load_perspectives()
        self.assertEqual(len(self.district_user.perspectives), 1)
        self.assertEqual(self.district_user.perspectives[0].id, 3)

        # Loading the natdis user which has 2 perspectives attached through National and District
        self.natdis_user.load_perspectives()
        self.assertEqual(len(self.natdis_user.perspectives), 2)

        # Check that the method correctly loads all perspectives for an admin
        perspectives = Perspective.objects.all()
        self.admin_user.load_perspectives()
        self.assertEqual(len(perspectives), len(self.admin_user.perspectives))
        #print len(self.admin_user.group_perspectives)

        print("load_perspectives OK")

        return


    def test_load_perspective(self):
        'Loading the district user 5, which has one perspective'

        national_perspective = Perspective.objects.get(name = 'National')
        district_perspective = Perspective.objects.get(name='District')
        district_user = User.objects.get(username = 'dis1')
        national_user = User.objects.get(username='nat1')
        natdis_user = User.objects.get(username='natdis')

        self.assertIsNone(national_user.load_perspective(district_perspective, False))
        self.assertIsNotNone(national_user.load_perspective(national_perspective, False))

        print("load_perspective OK")
        return

