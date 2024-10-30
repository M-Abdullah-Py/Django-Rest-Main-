from rest_framework import serializers
from .models import Blog, Comment, Review

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Review


class BlogSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only = True)
    reviews = ReviewSerializer(many= True,read_only = True)
    class Meta:
        model = Blog
        fields = "__all__"