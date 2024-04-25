from django import forms

class MusicForm(forms.Form):
    music1 = forms.CharField(label='Music 1', max_length= 100)
    music2 = forms.CharField(label='Music 2', max_length= 100)
    music3 = forms.CharField(label='Music 3', max_length= 100)
    music4 = forms.CharField(label='Music 4', max_length= 100)
    music5 = forms.CharField(label='Music 5', max_length= 100)