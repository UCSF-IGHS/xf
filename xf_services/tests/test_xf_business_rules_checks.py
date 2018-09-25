from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from xf.xf_services import XFBusinessRuleViolationException, \
    XFInvalidModelStateException, XFPermissionDeniedException
from xf.xf_services.tests.test_xf_services_test_case import XFServicesTestCase
from xf.xf_services.xf_business_rules_checks import XFBusinessRulesChecks


class XFBusinessRulesChecksTests(XFServicesTestCase):


    def test_ensure_business_rule_check_raises_xf_rule_violation_exception_when_condition_is_false(self):

        false_condition = False

        with self.assertRaises(XFBusinessRuleViolationException):
            XFBusinessRulesChecks.ensure_business_rule(false_condition,
                                                       'Should throw rule violation exception if condition is false')


    def test_ensure_business_rule_check_no_xf_rule_violation_exception_raised_when_condition_is_true(self):

        try:
            true_condition = True
            XFBusinessRulesChecks.ensure_business_rule(true_condition)
        except XFBusinessRuleViolationException:
            self.fail('Should not throw rule violation exception if condition is true')


    def test_ensure_model_is_in_state_check_does_not_raise_xf_invalid_model_state_exception_when_valid_model_state_(self):

        test_data = self._generate_model_state_test_data()

        model = test_data['dummy_stateful_model_instance']
        state_12 = test_data['model_states'].STATE_12
        model.add_state(state_12)

        try:
            XFBusinessRulesChecks.ensure_model_is_in_state(model, state_12)
        except XFInvalidModelStateException:
            self.fail('Should not throw invalid model state exception if model is in provided state')


    def test_ensure_model_is_in_state_check_raises_xf_invalid_model_state_exception_when_in_invalid_model_state(self):

        test_data = self._generate_model_state_test_data()

        model = test_data['dummy_stateful_model_instance']
        state_13 = test_data['model_states'].STATE_13
        model.add_state(state_13)

        with self.assertRaises(XFInvalidModelStateException):
            other_state = test_data['model_states'].STATE_12
            XFBusinessRulesChecks.ensure_model_is_in_state(model, other_state,
                                                           'Should throw invalid model state exception if model is not in provided state')


    def test_ensure_model_is_in_states_check_does_not_raise_xf_invalid_model_state_exception_when_in_valid_model_states(self):

        test_data = self._generate_model_state_test_data()

        model = test_data['dummy_stateful_model_instance']
        model.add_state(test_data['model_states'].STATE_12)
        model.add_state(test_data['model_states'].STATE_14)

        valid_model_states = [
            test_data['model_states'].STATE_12,
            test_data['model_states'].STATE_14
        ]

        try:
            XFBusinessRulesChecks.ensure_model_is_in_states(model, valid_model_states)
        except XFInvalidModelStateException:
            self.fail('Should not throw invalid model state exception if model is in provided states')


    def test_ensure_model_is_in_states_check_raises_xf_invalid_model_state_exception_when_in_invalid_model_states_(self):

        test_data = self._generate_model_state_test_data()

        model = test_data['dummy_stateful_model_instance']
        model.add_state(test_data['model_states'].STATE_12)
        model.add_state(test_data['model_states'].STATE_14)

        invalid_model_states = [
            test_data['model_states'].STATE_12,
            test_data['model_states'].STATE_13
        ]

        with self.assertRaises(XFInvalidModelStateException):
            XFBusinessRulesChecks.ensure_model_is_in_states(model, invalid_model_states,
                                                           'Should throw invalid model state exception if model is not in provided states')

    def test_ensure_user_has_model_permission_check_raises_xf_permission_denied_exception_if_user_lacks_permission(self):

        test_data = self._generate_model_state_test_data()

        user = test_data['user']
        model = test_data['model_class']

        with self.assertRaises(
                XFPermissionDeniedException, message='Should throw xf permission denied exception if user has no permission for model'):
            XFBusinessRulesChecks.ensure_user_has_model_permission(model, user, 'delete')

    def test_ensure_user_has_model_permission_check_does_not_raise_xf_permission_denied_exception_if_user_has_permission(self):

        test_data = self._generate_model_state_test_data()
        user = test_data['user']
        model = test_data['model_class']
        permission = test_data['model_delete_permission'].codename
        user.assign_model_permission(permission, model)

        try:
            XFBusinessRulesChecks.ensure_user_has_model_permission(model, user, 'delete')
        except XFPermissionDeniedException:
            self.fail('Should not throw xf permission denied exception if user has permission for model')


