from django import forms
from .models import Player, House, Game, Match

class PlayerForm(forms.ModelForm):
    house = forms.ModelChoiceField(
        queryset=House.objects.all(),  # Fetch all house names
        empty_label="Select a house",  # Placeholder for dropdown
        required=True
    )
    
    game = forms.ModelChoiceField(
        queryset=Game.objects.all(),  # Fetch all game names
        empty_label="Select a game",  # Placeholder for dropdown
        required=True
    )

    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'house', 'game']




from django import forms
from .models import Game, House

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['game_name', 'type', 'description', 'house1', 'house2', 'score']

    house1 = forms.ModelChoiceField(queryset=House.objects.all(), empty_label="Select House")
    house2 = forms.ModelChoiceField(queryset=House.objects.all(), empty_label="Select House")


# forms.py
from django import forms
from .models import Team, Player, House

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['house', 'players']  # Only house and players fields

    # Automatically filter players based on selected house
# forms.py
class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'house', 'game']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


#Adding Player Stats Form

from django import forms
from .models import PlayerStatistic, Player

class PlayerStatisticForm(forms.ModelForm):
    class Meta:
        model = PlayerStatistic
        fields = ['player', 'goals', 'assists', 'fouls', 'yellow_cards', 'red_cards']
        widgets = {
            'player': forms.Select(attrs={'class': 'form-control'}),
            'goals': forms.NumberInput(attrs={'class': 'form-control'}),
            'assists': forms.NumberInput(attrs={'class': 'form-control'}),
            'fouls': forms.NumberInput(attrs={'class': 'form-control'}),
            'yellow_cards': forms.NumberInput(attrs={'class': 'form-control'}),
            'red_cards': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate the player dropdown with available players
        self.fields['player'].queryset = Player.objects.all()

    def clean(self):
        cleaned_data = super().clean()

        player = cleaned_data.get('player')
        goals = cleaned_data.get('goals')
        assists = cleaned_data.get('assists')
        fouls = cleaned_data.get('fouls')
        yellow_cards = cleaned_data.get('yellow_cards')
        red_cards = cleaned_data.get('red_cards')

        # Add any additional validation logic here if needed
        if not player:
            raise forms.ValidationError("Player is required.")
        if goals < 0 or assists < 0 or fouls < 0 or yellow_cards < 0 or red_cards < 0:
            raise forms.ValidationError("Stat values cannot be negative.")
        
        return cleaned_data
