from django.shortcuts import render, redirect
from .forms import RecommendationForm
from .Recommender import Recommender

def recommend_music(request):
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            recommender = Recommender(client_id="1ef9dedd385a4b229c1a6b050506eb9d", client_secret="042f18627b5d40f19118c6a3806cfea2")
            # 사용자 입력 추출
            favorite_tracks = [form.cleaned_data[f'track_{i}'] for i in range(1, 6)]
            market = form.cleaned_data['market'] or 'US'

            # ID 기반과 장르 기반 추천 결과 받기
            id_recommendations = recommender.recommend_tracks_by_id(favorite_tracks, market)
            genre_recommendations = recommender.recommend_tracks_by_genre(favorite_tracks, market)

            # 추천 결과 결합 및 중복 제거
            all_recommendations = list(set(id_recommendations + genre_recommendations))
            if len(all_recommendations) > 3:
                all_recommendations = all_recommendations[:3]  # 상위 3개 추천만 선택
            elif len(all_recommendations) < 3:
                all_recommendations.extend(id_recommendations if len(id_recommendations) > len(genre_recommendations) else genre_recommendations)
                all_recommendations = list(set(all_recommendations))[:3]  # 중복 제거 및 최대 3개까지

            # 최종 추천 결과 페이지로 전달
            return render(request, 'result.html', {'recommendations': all_recommendations})
    else:
        form = RecommendationForm()
    return render(request, 'recommend.html', {'form': form})

def home(request):
    return render(request, 'home.html')