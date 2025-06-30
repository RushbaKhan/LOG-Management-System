"""
URL configuration for LOG project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf import settings
from home import views
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("", views.user_login, name='user_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/add_player/', views.add_player, name='add_player'),
    path('dashboard/view_players/', views.view_players, name='view_players'),
    path('dashboard/player/<player_id>/edit/', views.edit_player, name='edit_player'),
    path('dashboard/player/<player_id>/delete/', views.delete_player, name='delete_player'),

    path('dashboard/stats/<str:house_name>/', views.house_stats, name='house_stats'),
    path('dashboard/stats/ares/', views.house_stats, {'house_name': 'Ares'}, name='ares_stats'),
    path('dashboard/stats/kronos/', views.house_stats, {'house_name': 'Kronos'}, name='kronos_stats'),
    path('dashboard/stats/zeus/', views.house_stats, {'house_name': 'Zeus'}, name='zeus_stats'),
    path('dashboard/stats/apollo/', views.house_stats, {'house_name': 'Apollo'}, name='apollo_stats'),
    path('dashboard/schedule_match/', views.schedule_match, name='schedule_match'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    path('dashboard/schedule/edit/<int:pk>/', views.edit_schedule, name='edit_schedule'),
    path('dashboard/add_match/', views.add_match, name='add_match'),  
    path('dashboard/matches/', views.view_matches, name='view_matches'),

    path('dashboard/add_game/', views.add_game, name='add_game'),
    path('dashboard/view_game/', views.view_game, name='view_game'),

    path('dashboard/matches/edit/<int:match_id>/', views.edit_match, name='edit_match'),
    path('dashboard/matches/delete/<int:match_id>/', views.delete_match, name='delete_match'),

    path('dashboard/games/edit/<int:game_id>/', views.edit_game, name='edit_game'),
    path('dashboard/games/delete/<int:game_id>/', views.delete_game, name='delete_game'),

    path('dashboard/view_teams/', views.view_teams, name='view_teams'),

    path('dashboard/add_player_stats/', views.add_player_stats, name='add_player_stats'),

    path('dashboard/elog_mvp/', views.elog_mvp, name='elog_mvp'),

    

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
