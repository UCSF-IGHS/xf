from dal import autocomplete
from django.apps import apps
from django.db.models import QuerySet, Model


class XFAutoCompleteView(autocomplete.Select2QuerySetView):

    def get_queryset(self) -> QuerySet:

        self.process_forwarded_parameters()

        if self.model is None:
            return Model.objects.none()

        if not self.request.user.is_authenticated:
            return self.model.objects.none()

        self.queryset = self.model.objects.all()
        search_string = self.q

        kwargs = {}
        if search_string:
            kwargs = {
                '{0}__{1}'.format(self.model_field_name, 'icontains'): search_string,
            }

        if self.forwarded:
            for key, value in self.forwarded.items():
                kwargs['{0}__{1}'.format(key, 'exact')] = value

        self.queryset = self.queryset.filter(**kwargs)

        return self.queryset

    def process_forwarded_parameters(self):
        self._set_model_from_model_name()
        self._set_model_field_name()

    def _set_model_from_model_name(self):

        model_name = None

        for key, value in self.forwarded.items():
            if key.endswith('model'):
                model_name = value
                self.forwarded.pop(key)
                break

        if model_name is not None:
            app_label = model_name.split(".")[0]
            model_name = model_name.split(".")[1]

            self.model = apps.get_model(app_label=app_label, model_name=model_name)

    def _set_model_field_name(self):

        for key, value in self.forwarded.items():
            if key.endswith('search_field'):
                self.model_field_name = value
                self.forwarded.pop(key)
                break
