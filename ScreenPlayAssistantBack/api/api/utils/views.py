# Rest framework
from rest_framework import status
from rest_framework.response import Response


class BaseViewSet:
    
    url_kwarg_attrs = dict()
    serializer_classes = dict()

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_permissions(self):
        self.set_extra_data(self.request)
        return super().get_permissions()
    
    def set_extra_data(self, request):
        # remember old state
        if not hasattr(request, "data"):
            return
        has_mutable = False
        if hasattr(request.data, "_mutable"):
            has_mutable = True
            _mutable = request.data._mutable
            # set to mutable and mutate
            request.data._mutable = True

        for attr in self.url_kwarg_attrs:
            request.data[self.url_kwarg_attrs[attr]] = self.kwargs.get(attr)
        
        # back to prev state
        if has_mutable:
            request.data._mutable = _mutable
        
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset_kwarg = {}
        for attr in self.url_kwarg_attrs:
            queryset_kwarg[self.url_kwarg_attrs[attr]] = self.kwargs.get(attr)
        return self.model.get_read_queryset(queryset, self.request.user, **queryset_kwarg).distinct()
    
    def get_serializer_class(self):
        serializer_class = None
        if self.action in self.serializer_classes:
            serializer_class = self.serializer_classes[self.action]
        elif self.action == 'update' and 'partial_update' in self.serializer_classes:
            serializer_class = self.serializer_classes['partial_update']
        elif self.action == 'partial_update' and 'update' in self.serializer_classes:
            serializer_class = self.serializer_classes['update']
        elif self.action in ['list', 'retrieve'] and 'read' in self.serializer_classes:
            serializer_class = self.serializer_classes['read']
        elif self.action == 'list' and 'retrieve' in self.serializer_classes:
            serializer_class = self.serializer_classes['retrieve']
        elif self.action == 'retrieve' and 'list' in self.serializer_classes:
            serializer_class = self.serializer_classes['list']
        else:
            serializer_class = super().get_serializer_class()
        return serializer_class

    def get_serializer_context(self):
        context = super().get_serializer_context()
        for attr in self.url_kwarg_attrs:
            context[self.url_kwarg_attrs[attr]] = self.kwargs.get(attr)
        return context
    
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.deleted = True
    #     instance.save()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    