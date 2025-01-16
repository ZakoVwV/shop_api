from django.urls import path

from apps.review.views import RatingCreateView, RatingDeleteViwe, CommentCreateView, CommentDeleteView

urlpatterns = [
    path('rating/', RatingCreateView.as_view()),
    path('rating-delete/<int:pk>/', RatingDeleteViwe.as_view()),
    path('comment/', CommentCreateView.as_view()),
    path('comment-delete/<int:pk>/', CommentDeleteView.as_view()),
]