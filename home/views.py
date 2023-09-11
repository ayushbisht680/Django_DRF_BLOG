from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BlogSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from.models import Blog
from django.db.models import Q
from django.core.paginator import Paginator


class BlogView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes=[JWTAuthentication]

    def get(self, request):
        try:
            blogs = Blog.objects.filter(user=request.user)

            search_query = request.GET.get('search')
            if search_query:
                blogs = blogs.filter(Q(title__icontains=search_query) | Q(blog_text__icontains=search_query))
            
            page_number=request.GET.get('page',1)
            paginator=Paginator(blogs,2)

            serializer = BlogSerializer(paginator.page(page_number), many=True)

            return Response({
                'data': serializer.data,
                'message': 'Blogs fetched successfully'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'data': {},
                'message': f'Something went wrong: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'data': {},
                    'message': 'Blog created Successfully'
                }, status=status.HTTP_201_CREATED)
            
            else:
                return Response({
                    'data': serializer.errors,
                    'message': 'Validation failed'
                }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'error': str(e),
                'data': {},
                'message': 'Something went wrong as an exception'
            }, status=status.HTTP_400_BAD_REQUEST)

        
    


