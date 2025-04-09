# Rest Framework
import math
# Utilities
from urllib.parse import urlencode, urlparse, urlunparse, parse_qs

from rest_framework import pagination
from rest_framework.response import Response


class OffsetPagination(pagination.LimitOffsetPagination):
    def get_paginated_response(self, data):
        u = urlparse(self.request.get_full_path())
        query = parse_qs(u.query, keep_blank_values=True)

        query['limit'] = self.limit
        first = u._replace(query=urlencode(query, True))
        next_offset = (self.offset + self.limit) if (self.offset + self.limit) < self.count else None
        previous_offset = (self.offset - self.limit) if (self.offset - self.limit) > 0 else None
        last = u._replace(query=urlencode(query, True))

        if self.offset == 0:
            first = None
        else:
            first = self.request._current_scheme_host + urlunparse(first)

        if self.offset == (self.count // self.limit) * self.limit:
            last = None
        else:
            last = self.request._current_scheme_host + urlunparse(last)

        current_items = min(self.count - self.offset, 12)
        current_page = math.ceil((self.offset - 1) / self.limit) + 1
        return Response({
            'previous_offset': previous_offset,
            'offset': self.offset,
            'next_offset': next_offset,
            'count': self.count,
            'limit': self.limit,
            'page_count': math.ceil(self.count / self.limit),
            'current_page': current_page,
            'current_items': current_items * current_page,
            'results': data
        })


class StartEndPagination(pagination.LimitOffsetPagination):
    def get_paginated_response(self, data):
        u = urlparse(self.request.get_full_path())
        query = parse_qs(u.query, keep_blank_values=True)

        query['offset'] = 0
        query['limit'] = self.limit
        first = u._replace(query=urlencode(query, True))
        query['offset'] = (self.count // self.limit) * self.limit
        last = u._replace(query=urlencode(query, True))

        if self.offset == 0:
            first = None
        else:
            first = self.request._current_scheme_host + urlunparse(first)

        if self.offset == (self.count // self.limit) * self.limit:
            last = None
        else:
            last = self.request._current_scheme_host + urlunparse(last)

        return Response({
            'links': {
                'first': first,
                'previous': self.get_previous_link(),
                'current': self.request._current_scheme_host + self.request.get_full_path(),
                'next': self.get_next_link(),
                'last': last,
            },
            'count': self.count,
            'results': data
        })
