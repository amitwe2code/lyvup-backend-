from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import AccountModel
from userapp.models import UserModel
from rest_framework import status
from userapp.serializers import UserSerializer

from useraccount.models import UserAccountModel
from useraccount.serializers import UserAccountSerializer
# Create your views here.
class AccountUserView(APIView):
    def get(self,request,pk):
        print("pk=>",pk)
        account=AccountModel.objects.get(id=pk)
        if account:
            user_accounts=UserAccountModel.objects.filter(account=account)
            serializer=UserAccountSerializer(user_accounts,many=True)
            
            # Get all connected user IDs
            connected_user_ids = user_accounts.values_list('user_id', flat=True)
            
            unconnected_users = UserModel.objects.exclude(id__in=connected_user_ids)
            unconnected_serializer = UserSerializer(unconnected_users, many=True)
            
            response_data = {
                "connected_users": serializer.data,
                "unconnected_users": unconnected_serializer.data
            }
            return Response(response_data,status=status.HTTP_200_OK)
        return Response({
            "message":"Account not found",
            "status":"404 not found",
        },status=status.HTTP_404_NOT_FOUND)
    
   
class UserAccountView(APIView):
    def get(self,request,pk):
        user=UserModel.objects.get(id=pk)
        user_accounts=UserAccountModel.objects.filter(user=user)
        serializer=UserAccountSerializer(user_accounts,many=True)
        if serializer.data:
            return Response(serializer.data)
        return Response({
            "message":"User account not found",
            "status":"404 not found",
        },status=status.HTTP_404_NOT_FOUND)
    

class UserAccountCreateView(APIView):
    def post(self, request):
        try:
            
            user_ids = request.data.get('users', [])  
            account_id = request.data.get('account')
            print('user_ids',user_ids)
           
            if not user_ids or not account_id:
                return Response({
                    "message": " required Users list and account ID",
                    "status": "400 bad request"
                }, status=status.HTTP_400_BAD_REQUEST)

            created_connections = []
            already_connected = []

           
            for user_id in user_ids:
                # Check if connection already exists
                existing = UserAccountModel.objects.filter(
                    user_id=user_id,
                    account_id=account_id
                ).exists()

                if existing:
                    already_connected.append(user_id)
                    continue

                # Create new connection
                user_account = UserAccountModel.objects.create(
                    user_id=user_id,
                    account_id=account_id
                )
                created_connections.append(user_account)

            # Serialize created connections
            serializer = UserAccountSerializer(created_connections, many=True)
            
            response_data = {
                "created_connections": serializer.data,
                "already_connected": already_connected
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)

        except UserModel.DoesNotExist:
            return Response({
                "message": "User not found",
                "status": "404 not found"
            }, status=status.HTTP_404_NOT_FOUND)
            
        except AccountModel.DoesNotExist:
            return Response({
                "message": "Account not found",
                "status": "404 not found"
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                "message": str(e),
                "status": "400 bad request"
            }, status=status.HTTP_400_BAD_REQUEST)



class UserAccountDeleteView(APIView):
    def delete(self,request,pk):
        user_account=UserAccountModel.objects.get(id=pk)
        # user_account.delete()
        user_account.is_deleted = 1
            # intervention.is_active = 0  
        user_account.save()
        return Response({
            "message":"User account deleted successfully",
            "status":"success"
            },status=status.HTTP_200_OK)

