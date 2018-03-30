



class XFCRUDUnit:
    pass

    def __init__(self):
        self.crud_actions = []

        pass


class XFCrudAction:


    def __init2__(self, *args, **kwargs):
        self.action = kwargs['action'] if 'action' in kwargs else ''
        self.reverse_url = kwargs['reverse_url'] if 'reverse_url' in kwargs else ''
        self.fixed_url = kwargs['fixed_url'] if 'fixed_url' in kwargs else ''
        self.popup_in_ajax_form = kwargs['popup_in_ajax_form'] if 'popup_in_ajax_form' in kwargs else True
        pass

    def __init__(self):
        self.action = ''
        self.reverse_url = ''
        self.fixed_url = ''
        self.popup_in_ajax_form = True
        pass

    def generate_url(self):
        return ""

    def generate_edit_url(self):
        return ""

    def generate_create_url(self):
        return ''

    def generate_delete_url(self):
        return ''

    def generate_list_url(self):
        return ''

