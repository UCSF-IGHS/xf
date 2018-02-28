from enum import Enum
from xf_crud.crud_url_builder import XFCrudURLBuilder




class XFActionType(Enum):
    SINGLE_ENTITY_NEW = 1,
    SINGLE_ENTITY_PK = 2,
    LIST_ENTITIES = 3


class XFUIBuilder:

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
        self.url_builder = XFCrudURLBuilder(url_app_name=self.url_app_name, url_model_name=self.url_model_name,
                                            model_type=self.model_type)

    def generate_action(self,
                        action_type,
                        action_name,
                        action_caption):

        action = XFModelListAction(self, action_type, action_name, action_caption)
        return action

    def generate_url(self, action_name):
        if action_name == 'add':
            return self.url_builder.get_new_url(form_class_type=self.form_class_type)
        elif action_name == 'change':
            return self.url_builder.get_edit_url(form_class_type=self.form_class_type)



class XFModelListAction:

    def __init__(self,
                 ui_builder,
                 action_type,
                 action_name,
                 action_caption):

        self.action_caption = action_caption
        self.action_name = action_name
        self.action_type = action_type
        self.ui_builder = ui_builder
        self.url_name = "%s_%s_%s" % (self.ui_builder.url_app_name, self.ui_builder.url_model_name, self.action_name)





