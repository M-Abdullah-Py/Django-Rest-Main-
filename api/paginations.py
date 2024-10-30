from rest_framework.pagination import PageNumberPagination,  LimitOffsetPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    # request
    # ?page_size=2&page_number=1
    page_size = 3 # if this is not set it will use the global page set number 
    page_size_query_param = 'page_size'  # how many items per page
    page_query_param = "page_number" # which page the client wants eg page_number 2 
    max_page_size = 4  # maximum number of items  if the clients made request ----- 

    def get_paginated_response(self, data):
        return Response(
            {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'page_size': self.page_size, # returns the number of items per page
                'results': data # current page items are returned             
                }
        )

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3  # Default number of items per page
    max_limit = 5     # Maximum number of items allowed per page

    def get_paginated_response(self, data):
        return super().get_paginated_response(data)



