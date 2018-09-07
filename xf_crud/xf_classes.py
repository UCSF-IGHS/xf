from enum import Enum
#from xf.xf_crud.crud_url_builder import XFCrudURLBuilder


"""
Represents the type of action, which can be either on a new entity, an entity instance, or a list of entities.
For example, details, edit, delete are entity instance actions. New is a new entity instance action. Search is
based on a list of entities. This value determines whether an action requires a primary key or not.
"""
ACTION_NEW_INSTANCE = 1
ACTION_ROW_INSTANCE = 2
ACTION_LIST_ENTITIES = 3
ACTION_PREINITIALISED_RELATED_INSTANCE = 4
ACTION_RELATED_INSTANCE = 5
ACTION_OPEN_LINK = 6
ACTION_OPEN_LINK_NEW_WINDOW = 7





class XFUIAction:
    """
    Represents an action that the user can perform from a list of objects, typically under the "Actions" dropdown.
    """

    def __init__(self,
                 action_name, # Name of the action
                 action_caption, # Test of the action
                 permission_required,
                 url_name = None, # Leave None to create %s_%s_action_name
                 use_ajax = True,
                 action_type = ACTION_ROW_INSTANCE,
                 column_index = None,
                 user = None,
                 next_url = None,
                 default_action = False,
                 related_field = None,
                 url = None,
                 ):
        self.use_ajax = use_ajax
        self.permission_required = permission_required
        self.action_caption = action_caption
        self.action_name = action_name
        self.related_field = related_field
        self.url = url
        if url_name is None:
            self.url_name = "%s_%s_" + action_name
        else:
            self.url_name = url_name

        # Will be called after an action is completed, if set. Should be a URL name
        self.next_url = next_url

        # Can be used to pre-populate an action with data.
        self.initial_data = None
        self.action_type = action_type

        # To attach this action to a column index, set its number
        self.column_index = column_index

        # In case the user is needed
        self.user = user

        # When shown as a button, makes the button btn-primary
        self.default_action = default_action
