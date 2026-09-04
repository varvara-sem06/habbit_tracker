from rest_framework.pagination import PageNumberPagination


class HabbitPagination(PageNumberPagination):
    page_size = 5
