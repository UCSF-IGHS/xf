from django.core.exceptions import PermissionDenied

from xf.tests.xf_test_case_data import XFTestCaseData


class PermissionMixinTestCase(XFTestCaseData):

    def test_assert_has_perm_returns_false_if_user_has_no_permission(self):

        test_data = self._generate_permissions_test_data()
        user = test_data['user']

        instance = test_data['class_instance']
        instance.set_requesting_user(user)

        self.assertFalse(instance.has_perm('delete'), msg='Should return false if user has no permission')

    def test_assert_has_perm_returns_true_if_user_has_permission(self):

        test_data = self._generate_permissions_test_data()
        user = test_data['user']

        model = test_data['model_class']
        user.assign_model_permission('delete', model)

        instance = test_data['class_instance']
        instance.set_requesting_user(user)

        self.assertTrue(instance.has_perm('delete'),
                        msg='Should return true if user has the given permission')


    def test_ensure_group_or_403_throws_permission_denied_if_user_not_in_group(self):

        test_data = self._generate_permissions_test_data()
        user = test_data['user']

        instance = test_data['class_instance']
        instance.set_requesting_user(user)

        group = test_data['user_group']

        with self.assertRaises(PermissionDenied):
            instance.ensure_group_or_403(group=group)
            # msg = 'Should throw permission denied exception if user is not in the group'


    def test_ensure_group_or_403_does_not_throw_permission_denied_if_user_in_group(self):

        test_data = self._generate_permissions_test_data()
        user = test_data['user']

        instance = test_data['class_instance']
        instance.set_requesting_user(user)

        group = test_data['user_group']
        user.assign_to(group)

        try:
            instance.ensure_group_or_403(group=group)
        except PermissionDenied:
            self.fail('Should not throw permission denied exception if user has permission')


    def test_ensure_groups_or_403_throws_permission_denied_if_user_not_in_groups(self):

        test_data = self._generate_permissions_test_data()
        user = test_data['user']

        instance = test_data['class_instance']
        instance.set_requesting_user(user)

        group_1 = test_data['user_group']
        group_2 = test_data['user_group_2']

        with self.assertRaises(PermissionDenied):
            instance.ensure_groups_or_403(groups=[group_1, group_2])
            # msg = 'Should throw permission denied exception if user is not in at least one of the groups'


    def test_ensure_groups_or_403_does_not_throw_permission_denied_if_user_in_groups(self):

        test_data = self._generate_permissions_test_data()
        user = test_data['user']

        instance = test_data['class_instance']
        instance.set_requesting_user(user)

        group_1 = test_data['user_group']
        group_2 = test_data['user_group_2']
        user.assign_to(group_2)

        try:
            instance.ensure_groups_or_403(groups=[group_1, group_2])
        except PermissionDenied:
            self.fail('Should not throw permission denied exception if user is in at least one of the groups')


    def test_assert_ensure_set_context_perm_throws_permission_denied_if_user_has_permission(self):

        test_data = self._generate_permissions_test_data()
        user = test_data['user']

        instance = test_data['class_instance']
        instance.set_requesting_user(user)

        with self.assertRaises(PermissionDenied):
            instance.ensure_set_context_perm('delete')
            # msg='Should return true if user has the given permission')


    def test_assert_ensure_set_context_perm_sets_permission_in_context(self):

        test_data = self._generate_permissions_test_data()
        user = test_data['user']

        model = test_data['model_class']
        user.assign_model_permission('delete', model)

        instance = test_data['class_instance']
        instance.set_requesting_user(user)

        try:
            instance.ensure_set_context_perm('delete')
        except PermissionDenied:
            self.fail('Should not throw permission denied exception if user has the given permission')

        self.assertTrue(instance.context['delete'], True)