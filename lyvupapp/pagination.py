from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
            'status': 'success',
            'message': 'Data retrieved successfully',
            'data': {
                'results': data,
                'pagination': {
                    'count': self.page.paginator.count,
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link(),
                    'current_page': self.page.number,
                    'total_pages': self.page.paginator.num_pages,
                }
            }
        })