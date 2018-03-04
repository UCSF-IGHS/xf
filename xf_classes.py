from enum import Enum
#from xf_crud.crud_url_builder import XFCrudURLBuilder


"""
Represents the type of action, which can be either on a new entity, an entity instance, or a list of entities.
For example, details, edit, delete are entity instance actions. New is a new entity instance action. Search is
based on a list of entities. This value determines whether an action requires a primary key or not.
"""
ACTION_NEW_INSTANCE = 1
ACTION_ROW_INSTANCE = 2
ACTION_LIST_ENTITIES = 3
ACTION_RELATED_INSTANCE = 4



class XFUIBuilder:
    """
    Class is not currently used, and will be deprecated
    """
    def __init__(self,
                 url_app_name,
                 model_type,
                 form_class_type,
                 list_class_type,
                 url_model_name=None
                 ):
        self.url_model_name = url_model_name if url_model_name else model_type.__name__.lower()
        self.list_class_type = list_class_type
        self.form_class_type = form_class_type
        self.model_type = model_type
        self.url_app_name = url_app_name
        #self.url_builder = XFCrudURLBuilder(url_app_name=self.url_app_name, url_model_name=self.url_model_name,
        #                                    model_type=self.model_type)

    def generate_action(self,
                        action_type,
                        action_name,
                        action_caption):

        action = XFUIAction(self, action_type, action_name, action_caption)
        return action

    def generate_url(self, action_name):
        #if action_name == 'add':
        #    return self.url_builder.get_new_url(form_class_type=self.form_class_type)
        #elif action_name == 'change':
        #    return self.url_builder.get_edit_url(form_class_type=self.form_class_type)
        pass



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
                 action_type = ACTION_ROW_INSTANCE
                 ):
        self.use_ajax = use_ajax
        self.permission_required = permission_required
        self.action_caption = action_caption
        self.action_name = action_name
        if url_name is None:
            self.url_name = "%s_%s_" + action_name
        else:
            self.url_name = url_name

        # Will be called after an action is completed, if set. Should be a URL name
        self.next_url = None

        # Can be used to pre-populate an action with data.
        self.initial_data = None
        self.action_type = action_type
