from rest_framework.pagination import PageNumberPagination, _positive_int


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'  # items per page

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                return _positive_int(
                    request.query_params[self.page_size_query_param],
                    strict=True,
                    cutoff=self.max_page_size
                )
            except ValueError:
                return 1000000
            except KeyError:
                pass
        return self.page_size
