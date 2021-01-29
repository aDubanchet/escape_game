from django.forms import ModelForm
from core.models import Game


# Widgets 
from django.forms.widgets import Widget
from django.template import loader
from django.utils.safestring import mark_safe


# Custom Widget for Form
class CreateTimerWidget(Widget):
    template_name = 'account/set_timer.html.html'

    def get_context(self, name, value, attrs=None):
        return {'widget': {
            'name': name,
            'value': value,
        }}

    def render(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['timer']
