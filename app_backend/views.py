from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from .models import *
from .serializers import *



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    profile = user.profile
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([])
def create_user(request):
    user = User.objects.create(
        username = request.data['username']
    )
    user.set_password(request.data['password'])
    user.save()
    profile = Profile.objects.create(
        user = user,
        first_name = request.data['first_name'],
        last_name = request.data['last_name']
    )
    profile.save()
    profile_serialized = ProfileSerializer(profile)
    return Response(profile_serialized.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_post(request):
    user = request.user

    content = request.data.get('content')
    image = request.data.get('image')

    if not content and not image:
        return Response({'error': 'Content or image is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        profile = Profile.objects.get(user=user)
        post = Post.objects.create(profile=profile, content=content, image=image)
        serializer = PostSerializer(post)
        return Response({'message': 'Post created successfully.', 'post': serializer.data}, status=status.HTTP_201_CREATED)
    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_posts(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        posts = Post.objects.filter(profile=profile)
        serialized_post = PostSerializer(posts, many=True)
        return Response(serialized_post.data)
    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=404)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request, pk):
    user = request.user
    profile = user.profile
    try:
        post = Post.objects.get(pk=pk, profile=profile)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'})
    
    serialized_post = PostSerializer(post, data=request.data)
    if serialized_post.is_valid():
        serialized_post.save()
        return Response(serialized_post.data)
    return Response(serialized_post.errors)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'})
    
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)