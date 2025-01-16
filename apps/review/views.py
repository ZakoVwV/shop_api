from readline import get_endidx

from rest_framework import generics, permissions

from apps.review.serializers import RatingSerializer, CommentSerializer
from apps.review.models import Comment, Rating
from apps.generals.permissions import IsOwner


class RatingCreateView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RatingDeleteViwe(generics.DestroyAPIView):
    queryset = Rating.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def query_set(self):
        return Rating.objects.filter(owner=self.request.user)


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Rating.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner ]

    def query_set(self):
        return Comment.objects.filter(owner=self.request.user)
