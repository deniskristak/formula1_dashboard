from crispy_forms.bootstrap import FormActions
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Hidden
from django.db.utils import OperationalError, ProgrammingError

from tips_input.models import Player, Race, Driver, RaceTip


class F1DriversForm(forms.Form):
    players = Player.objects.all()
    races = Race.objects.all()
    # todo: solve this bug when performing `migrate`
    try:
        players_names = [(player.id, player.nickname) for player in players]
        races_names = [(race.id, race.name) for race in races]
    except OperationalError:
        players_names = []
        races_names = []
    except ProgrammingError:
        players_names = []
        races_names = []
    player_formfield = forms.ChoiceField(choices=players_names, label="Who are you?")
    race_formfield = forms.ChoiceField(choices=races_names, label="What Grandprix are you betting on?")
    race_type_formfield = forms.ChoiceField(choices=[("race", "Race"), ("quali", "Qualification")],
                                            label="Quali or race?")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.form_action = "tips_input/"
        self.helper.layout = Layout(
            Row(
                Column('player_formfield', css_class='form-group col-md-6 mb-0'),
                Column('race_formfield', css_class='form-group col-md-6 mb-0'),
                Column('race_type_formfield', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                FormActions(Submit('continue', 'Continue')),
            ),

        )


class DriverExtrasForm(forms.Form):
    # workaround to weird migration import trouble
    try:
        players = Player.objects.all()
        races = Race.objects.all()
        drivers = Driver.objects.all()

        choices_default = []
        for driver in drivers:
            choices_default.append((driver.id, driver.name))

    except OperationalError:
        players = []
        races = []
        drivers = []
    except ProgrammingError:
        players = []
        races = []
        drivers = []

    dnf_select_1 = forms.ChoiceField(
        choices=choices_default,
        label="DNF driver #1",
    )
    dnf_select_2 = forms.ChoiceField(
        choices=choices_default,
        label="DNF driver #2"
    )
    dnf_select_3 = forms.ChoiceField(
        choices=choices_default,
        label="DNF driver #3"
    )
    dotd_select = forms.ChoiceField(
        choices=choices_default,
        label="Driver of the day",
    )
    fastest_lap_select = forms.ChoiceField(
        choices=choices_default,
        label="Fastest Lap"
    )

    def __init__(self, curr_player, curr_race, race_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.form_action = "ordering/"
        self.helper.layout = Layout(
            Row(
                Column('dnf_select_1',css_class='form-group col-md-6 mb-0'),
                Column('dnf_select_2',css_class='form-group col-md-6 mb-0'),
                Column('dnf_select_3',css_class='form-group col-md-6 mb-0'),
                Column('dotd_select',css_class='form-group col-md-6 mb-0'),
                Column('fastest_lap_select',css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                FormActions(Submit('continue', 'Continue')),
            ),
            Hidden('player_formfield', curr_player),
            Hidden('race_formfield', curr_race),
            Hidden('race_type_formfield', race_type),
        )
        # todo: make form validation / dynamic input selection so that user can't put the same driver in all 3 dnfs
        # setting initially displayed values for all the selectboxes
        # 1. get current user's three tips concerning dnf
        curr_dnf_tips = RaceTip.objects.filter(player=curr_player, race=curr_race, dnf=True)
        # 2. set initial values equal to corresponding drivers' ids
        if len(curr_dnf_tips) >= 1:
            self.fields['dnf_select_1'].initial=curr_dnf_tips[0].driver.id
        if len(curr_dnf_tips) >= 2:
            self.fields['dnf_select_2'].initial=curr_dnf_tips[1].driver.id
        if len(curr_dnf_tips) >= 3:
            self.fields['dnf_select_3'].initial=curr_dnf_tips[2].driver.id
        # same for dotd and fastest_lap
        curr_dotd_tip = RaceTip.objects.get(player=curr_player, race=curr_race, dotd=True)
        self.fields['dotd_select'].initial=curr_dotd_tip.driver.id
        curr_fastest_lap_tip = RaceTip.objects.get(player=curr_player, race=curr_race, fastest_lap=True)
        self.fields['fastest_lap_select'].initial=curr_fastest_lap_tip.driver.id
