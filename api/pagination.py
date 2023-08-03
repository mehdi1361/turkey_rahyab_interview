from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status


class CustomPaginations(PageNumberPagination):

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response(
            {
                'current': self.page.number,
                'page_count': self.page.paginator.num_pages,
                'page_size': self.page_size,
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'results': data,
            },
            status=status.HTTP_200_OK)
