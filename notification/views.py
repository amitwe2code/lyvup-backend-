# notifications/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class NotificationListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request,pk=None):
        try:
            id=pk
            notifications = Notification.objects.filter(to_id=id)
            serializer = NotificationSerializer(notifications, many=True)

            return Response({
                'status':'success',
                'message':'notifications get successfully',
                'data':serializer.data,
            },status=status.HTTP_200_OK)    
               
          
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'An unexpected internal server error occurred: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self,request,pk):
        try:
            if pk:
                data=request.data
                print('update notification come ')
                notification =Notification.objects.get(id=pk)
                notification.is_read=True
                notification.save()
                # NotificationSerializer(notification,data=data)
                return Response({
                    'status':'success',
                },status=status.HTTP_204_NO_CONTENT)
        except Notification.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'notification not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'An unexpected internal server error occurred: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)