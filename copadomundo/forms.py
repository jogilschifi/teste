from django.forms import ModelForm
from .models import Palpites

# Create the form class.
class PalpitesForm(ModelForm):
    class Meta:
        model = Palpites
        fields = '__all__'

        def __init__(self):
            self.request = None

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['PalpitesForm'] = context['PalpitesForm'].filter(user=self.request.user)
            return context