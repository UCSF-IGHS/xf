from django.test import TestCase

from xf.xf_services.xf_model_state_mixin import XFModelState

# This test should eventually move to XF -> and be done on an XF class



class XFModelStateTests(TestCase):
    pass

    # def test_new_model_state_is_new(self):
    #     model = CD4Count()
    #     self.assertTrue(model.is_in_state(XFModelState.NEW))
    #
    # def test_new_model_state_with_more_states_removes_unknown(self):
    #     model = CD4Count()
    #     model._add_state(XFModelState.NEW)
    #     self.assertFalse(model.is_in_state(XFModelState.UNKNOWN))
    #
    # def test_client_is_on_art(self):
    #     new_client = Client()
    #     self.assertTrue(new_client.is_in_state(ClientState.ON_ART))
    #     self.assertTrue(new_client.is_in_state(ClientState.NEW))
    #

#   Business rules
#   1) State
#   2) User rights

#   Can dispense ARVs?
    # If client is on ART
    # If user has permission to enter data for that facility

#   Can dispense this ARV Regimen?
    # If client is on ART
    # If regimen is appropriate for client
    # If user has permission to enter data for that facility

    # def ensure_can_dispense_arv(self):
    #     client = Client()
    #     self.ensure_business_rule(client.is_in_state(ClientState.ON_ART))
    #     self.ensure_security(user.can_add_arvs)
    #     self.ensure_client_belongs_to_users_facility(client, user)
    #
    #     return True
