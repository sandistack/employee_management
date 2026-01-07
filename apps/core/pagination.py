from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per_page'
    max_page_size = 100
    
    def get_pagination_info(self):
        return {
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'per_page': self.page_size,
            'total_items': self.page.paginator.count,
            'has_next': self.page.has_next(),
            'has_previous': self.page.has_previous(),
        }