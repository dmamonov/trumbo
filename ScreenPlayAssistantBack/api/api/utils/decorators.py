from functools import wraps
from rest_framework.response import Response


def validate_data(in_serializer_class=None, out_serializer_class=None):
    def decorator(func, *args):
        @wraps(func)
        def wrapper(view, request, *args, **kwargs):
            # In data
            is_detail_request = 'pk' in request.parser_context['kwargs']

            if in_serializer_class:
                in_serializer = in_serializer_class
            else:
                if is_detail_request:
                    obj = view.get_object()
                    view.check_object_permissions(request, obj)
                    in_serializer = view.get_serializer(obj, data=request.data)
                else:
                    in_serializer = view.get_serializer(data=request.data)
            in_serializer.is_valid(raise_exception=True)
            validated_data = in_serializer.validated_data

            # Process
            result = func(
                view, request, validated_data=validated_data, *args, **kwargs)

            # Out data
            if isinstance(result, Response):
                result_data = result.data
                out_data = validate_out_data(
                    result_data, out_serializer_class, view)
                result.data = out_data
                return result
            else:
                result_data = result.pop('data')
                out_data = validate_out_data(
                    result_data, out_serializer_class, view)
                return Response(out_data, **result)
        return wrapper
    return decorator


def validate_out_data(result_data, out_serializer_class, view):
    if out_serializer_class:
        out_serializer = out_serializer_class(result_data)
    else:
        out_serializer = view.get_serializer(result_data)
    return out_serializer.data
