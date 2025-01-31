from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import GDPRRequestModel
from .serializers import GDPRSerializer
from lyvupapp.pagination import Pagination


class GDPRAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['id','user_id' ]
    ordering_fields = ['id','user_id','request_status','request_type' ]
    filterset_fields = ['id','user_id','request_status','request_type' ]
    pagination_class = Pagination

    def get(self, request, pk=None):
        try:
            if pk:
                gdpr = GDPRRequestModel.objects.get(id=pk)
                serializer = GDPRSerializer(gdpr, context={'request': request})
                return Response({
                    'status': 'success',
                    'message': 'gdpr retrieved successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

            gdprs = GDPRRequestModel.objects.all().order_by('id')
            
            gdprs = DjangoFilterBackend().filter_queryset(request, gdprs, self)
            gdprs = SearchFilter().filter_queryset(request, gdprs, self)
            gdprs = OrderingFilter().filter_queryset(request, gdprs, self)
            paginator = self.pagination_class()
            paginated_gdprs = paginator.paginate_queryset(gdprs, request)
            serializer = GDPRSerializer(paginated_gdprs, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        except GDPRRequestModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'gdpr Request not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'An unexpected internal server error occurred: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            print('data=',data)
            serializer = GDPRSerializer(data=data, context={'request': request})

            if serializer.is_valid():
                gdpr = serializer.save()
                return Response({
                    'status': 'success',
                    'message': f'{gdpr} created',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

            return Response({
                'status': 'error',
                'message': 'Validation error',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'An unexpected internal server error occurred: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self, request, pk):
        return self._update_gdpr(request, pk, partial=False)

    def patch(self, request, pk):
        return self._update_gdpr(request, pk, partial=True)

    def _update_gdpr(self, request, pk, partial=False):
        try:
            gdpr = GDPRRequestModel.objects.get(id=pk)
            serializer = GDPRSerializer(gdpr, data=request.data, partial=partial, context={'request': request})

            if serializer.is_valid():
                gdpr = serializer.save()
                return Response({
                    'status': 'success',
                    'message':  f'{gdpr} updated ',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

            return Response({
                'status': 'error',
                'message': 'Validation error',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except GDPRRequestModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'gdpr Request not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'An unexpected internal server error occurred: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            gdpr = GDPRRequestModel.objects.get(id=pk)
            # gdpr.is_deleted = True
            gdpr.is_deleted = 1 

            gdpr.delete()
            return Response({
                'status': 'success',
                'message': f'{gdpr} deleted ',
                'data':'None'
            }, status=status.HTTP_200_OK)

        except GDPRRequestModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'gdpr Request not found',
                'data': 'None'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'An unexpected internal server error occurred: {str(e)}',
                'data': 'None'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)