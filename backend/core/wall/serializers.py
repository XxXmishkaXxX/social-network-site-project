from rest_framework import serializers

from .models import Post, CommentPostModel, LikePostModel, ImagePost


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentPostModel
        fields = ['id', 'post', 'author', 'content', 'created_at']

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePost
        fields = ['id', 'post', 'image']

class PostSerializer(serializers.ModelSerializer):
    MAX_FILES = 5

    comment = CommentSerializer(many=True, read_only=True)
    images = PhotoSerializer(many=True, read_only=True)

    def create(self, validated_data):
        images_data = self.context['request'].FILES.getlist('images')
        if len(images_data) > self.MAX_FILES:
            raise serializers.ValidationError(f"Максимальное количество изображений для загрузки - {self.MAX_FILES}.")

        post = Post.objects.create(**validated_data)

        for image_data in images_data:
            ImagePost.objects.create(post=post, image=image_data)

        return post

    def validate_images(self):
        images = self.data.getlist('images')
        if images and len(images) > self.MAX_FILES:
            raise serializers.ValidationError(f"Максимальное количество изображений для загрузки - {self.MAX_FILES}.")
        return images

    class Meta:
        model = Post
        fields = ['id', 'content', 'created_at', 'author', 'comment', 'images']