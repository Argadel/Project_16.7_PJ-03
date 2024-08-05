from django.urls import path
from .views import (
        NoticeListView,
        NoticeDetailView,
        NoticeCreateView,
        NoticeUpdateView,
        NoticeDeleteView,
        UserNoticeListView,
        CategoryListView,
        OneCategoryListView,
        ReplyDetailView,
        ReplyCreateView,
        ReplyUpdateView,
        ReplyDeleteView,
        accept,
        subscriptions,
        my_notices,
)
from . import views

urlpatterns = [
    path('', NoticeListView.as_view(), name='noticeboard-home'),
    path('user/<str:username>', UserNoticeListView.as_view(), name='users-notices'),
    path('notice/<int:pk>/', NoticeDetailView.as_view(), name='notice-detail'),
    path('notice/new/', NoticeCreateView.as_view(), name='notice-create'),
    path('notice/<int:pk>/update/', NoticeUpdateView.as_view(), name='notice-update'),
    path('notice/<int:pk>/delete/', NoticeDeleteView.as_view(), name='notice-delete'),
    path('reply/<int:pk>/', ReplyDetailView.as_view(), name='reply-detail'),
    path('reply/<int:pk>/accepted', accept, name='accepted'),
    path('notices_and_replies/', my_notices, name='my-notices'),
    path('notice/<int:pk>/new/', ReplyCreateView.as_view(), name='reply-create'),
    path('reply/<int:pk>/update/', ReplyUpdateView.as_view(), name='reply-update'),
    path('reply/<int:pk>/delete/', ReplyDeleteView.as_view(), name='reply-delete'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('category/<int:pk>', OneCategoryListView.as_view(), name='category'),
    path('about/', views.about, name='about-noticeboard'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]
