from django.shortcuts import render
from .forms import MusicForm

# Create your views here.
from django.http import HttpResponse

def index(request):
    # 사용자가 폼을 제출했을 경우
    if request.method == 'POST':
        form = MusicForm(request.POST)
        if form.is_valid():
            musics = [form.cleaned_data['music1'],
                      form.cleaned_data['music2'],
                      form.cleaned_data['music3'],
                      form.cleaned_data['music4'],
                      form.cleaned_data['music5'],]
            print(musics)
            return render(request, 'music_submitted.html', {'musics': musics})
    else:
        form = MusicForm()

    # form 변수를 템플릿에 전달
    return render(request, 'music_form.html', {'form': form})