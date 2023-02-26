from crispy_forms.bootstrap import FormActions
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

from tips_input.models import Player, Race

STATES = (
    ('', 'Choose...'),
    ('MG', 'Minas Gerais'),
    ('SP', 'Sao Paulo'),
    ('RJ', 'Rio de Janeiro')
)


class F1DriversForm(forms.Form):
    players = Player.objects.all()
    races = Race.objects.all()
    players_names = [(player.id, player.nickname) for player in players]
    races_names = [(race.id, race.name) for race in races]

    player_formfield = forms.ChoiceField(choices=players_names, label="Who are you?")
    race_formfield = forms.ChoiceField(choices=races_names, label="What Grandprix are you betting on?")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.form_action = "ordering"
        self.helper.layout = Layout(
            Row(
                Column('player_formfield', css_class='form-group col-md-6 mb-0'),
                Column('race_formfield', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                FormActions(Submit('continue', 'Continue')),
            ),
        )
