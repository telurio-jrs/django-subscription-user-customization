from django.urls import path

from longevity_app.views import (dashboard_detaisl_view, dashboard_view,
                                 index_view, logout_view)

app_name = 'longevity_app'

urlpatterns = [
    # INDEX
    path('index/', index_view.IndexView.as_view()),
    path('', index_view.IndexView.as_view(), name='index'),
    path('index/auth/', index_view.IndexView.as_view(), name='index_auth'),

    # DASHBOARD
    path(
        'dashboard/',
        dashboard_view.DashboardView.as_view(),
        name='dashboard'
    ),
    path(
        'dashboard/remove/',
        dashboard_view.DashboardView.as_view(),
        name='dashboard_remove'
    ),
    path(
        'dashboard/detail/<int:article>',
        dashboard_detaisl_view.DashboardDetailView.as_view(),
        name='dashboard_detail'
    ),

    # LOGOUT
    path('logout/', logout_view.LogoutView.as_view(), name='logout')
]
