from django import forms

class RecommendationForm(forms.Form):
    market = forms.CharField(label='Music Market(US/KR)', max_length=2, initial='US', required=False)
    track_1 = forms.CharField(label='Track 1', max_length=100)
    artist_1 = forms.CharField(label='Artist 1', max_length=100, required=False)
    track_2 = forms.CharField(label='Track 2', max_length=100)
    artist_2 = forms.CharField(label='Artist 2', max_length=100, required=False)
    track_3 = forms.CharField(label='Track 3', max_length=100)
    artist_3 = forms.CharField(label='Artist 3', max_length=100, required=False)
    track_4 = forms.CharField(label='Track 4', max_length=100)
    artist_4 = forms.CharField(label='Artist 4', max_length=100, required=False)
    track_5 = forms.CharField(label='Track 5', max_length=100)
    artist_5 = forms.CharField(label='Artist 5', max_length=100, required=False)
