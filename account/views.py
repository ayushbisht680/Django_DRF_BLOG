from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer,LoginSerializer
from rest_framework import status

# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=RegisterSerializer(data=data)
            if not serializer.is_valid():
              return Response({
                'data':serializer.errors,
                'message':'Something went wrong'
               },status.HTTP_400_BAD_REQUEST)
            serializer.save()

            return Response({
                'data':{},
                'message':'Your Acount have been created'
               },status=status.HTTP_201_CREATED)
            
            
        except Exception as e:
            return Response({
                'data':{},
                'message':'Something went wrong as exception'
               },status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=LoginSerializer(data=data)
            if not serializer.is_valid():
              print(serializer.data)
            #   print(data)
              return Response({
                'data':serializer.errors,
                'message':'Something went wrong here'
               },status.HTTP_400_BAD_REQUEST)
            
            response=serializer.get_jwt_token(serializer.data)

            return Response(response, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({
                'data':serializer.errors,
                'message':'Something went wrong while making a login'
               },status=status.HTTP_400_BAD_REQUEST)
        
        
    

        

    

