from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import ConsentModel
from .serializers import ConsentSerializer
from lyvupapp.pagination import Pagination


class ConsentAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['id','user_id' ]
    ordering_fields = ['id','user_id','consent_status','consent_date' ]
    filterset_fields = ['id','user_id','consent_status','consent_date' ]
    pagination_class = Pagination

    def get(self, request, pk=None):
        try:
            if pk:
                consent = ConsentModel.objects.get(id=pk)
                serializer = ConsentSerializer(consent, context={'request': request})
                return Response({
                    'status': 'success',
                    'message': 'Consent retrieved successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

            consents = ConsentModel.objects.all().order_by('id')
            
            consents = DjangoFilterBackend().filter_queryset(request, consents, self)
            consents = SearchFilter().filter_queryset(request, consents, self)
            consents = OrderingFilter().filter_queryset(request, consents, self)
            paginator = self.pagination_class()
            paginated_consents = paginator.paginate_queryset(consents, request)
            print('data1=>',paginated_consents[0].consent_type)
            serializer = ConsentSerializer(paginated_consents, many=True, context={'request': request})
            print('data2=>',serializer.data[0])
            return paginator.get_paginated_response(serializer.data)

        except ConsentModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'consent not found',
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
            serializer = ConsentSerializer(data=data, context={'request': request})

            if serializer.is_valid():
                consent = serializer.save()
                return Response({
                    'status': 'success',
                    'message': f'{consent} created ',
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
        return self._update_consent(request, pk, partial=False)

    def patch(self, request, pk):
        return self._update_consent(request, pk, partial=True)

    def _update_consent(self, request, pk, partial=False):
        try:
            consent = ConsentModel.objects.get(id=pk)
            serializer = ConsentSerializer(consent, data=request.data, partial=partial, context={'request': request})

            if serializer.is_valid():
                consent = serializer.save()
                return Response({
                    'status': 'success',
                    'message':  f'{consent} updated ',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

            return Response({
                'status': 'error',
                'message': 'Validation error',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except ConsentModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'consent not found',
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
            consent = ConsentModel.objects.get(id=pk)
            consent.delete()
            return Response({
                'status': 'success',
                'message': f'{consent} deleted ',
                'data':'None'
            }, status=status.HTTP_200_OK)

        except ConsentModel.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'consent not found',
                'data': 'None'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'An unexpected internal server error occurred: {str(e)}',
                'data': 'None'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    