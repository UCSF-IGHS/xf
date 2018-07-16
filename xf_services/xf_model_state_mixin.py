from enum import Flag, auto

from django.db import models


class XFModelState:
    UNKNOWN = 1
    NEW = 2
    EXISTING = 3
    DEACTIVATED = 4


class XFModelStateMixIn:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._model_state = []
        self._add_state(XFModelState.UNKNOWN)

    def _add_state(self, state_to_add):
        if not self._has_state(state_to_add):
            self._model_state.append(state_to_add)
            self._verify_state_without_unknown()

    def _remove_state(self, state_to_remove):
        if self._has_state(state_to_remove):
            self._model_state.remove(state_to_remove)

    def _has_state(self, state_to_check):
        return state_to_check in self._model_state

    def _clear_state(self):
        self._model_state = []

    def _verify_state_without_unknown(self):
        if len(self._model_state) > 1:
            self._remove_state(XFModelState.UNKNOWN)

    def _update_crud_state(self):

        if self.pk:
            self._add_state(XFModelState.EXISTING)
        else:
            self._add_state(XFModelState.NEW)


    def compute_model_state(self, hint_for_state_requested = None):
        """
        Must override. Prepares the model state for this model. You may specify an optional hint that would
        focus only on updating that specific state
        :return:
        """
        self._update_crud_state()
        pass

    def is_in_state(self, model_state):
        """
        Checks whether a model is in a particular state.
        :param model_state:
        :return:
        True if the model is in that state, otherwise False.
        """
        self.compute_model_state(model_state)
        return self._has_state(model_state)


