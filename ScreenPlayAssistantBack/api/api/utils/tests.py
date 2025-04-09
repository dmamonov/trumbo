from functools import wraps

from django.conf import settings


def response_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if response.status_code >= 400:
            print('Request Error:', response.code, response.data)
        return response

    return wrapper


class DefaultTestHelper:
    default_path = ''
    model_class = None
    factory = None
    sample_data = {
        'default': {}
    }

    general_path = '/' + settings.API_URI + '/{default_path}/'
    specific_path = '/' + settings.API_URI + '/{default_path}/{id}/'

    @classmethod
    def get_sample_data(cls, sample_name='default'):
        if sample_name in cls.sample_data:
            return cls.sample_data[sample_name]
        raise Exception(f'"{sample_name}" not in sample data')

    @classmethod
    def _get_data(cls, data, sample_name):
        if not data and not sample_name:
            raise Exception('either data or sample_name should be specified')
        if not data and sample_name:
            return cls.get_sample_data(sample_name)
        return data

    @classmethod
    def force_create(cls, sample_name='default'):
        # Create new Object with the given data
        sample = cls.get_sample_data(sample_name)
        obj = cls.factory(**sample)

        return obj

    @classmethod
    def _specific_call(cls, client, action_name, obj_id, data=None):
        # Patch new Object with the given data
        uri = cls.specific_path.format(default_path=cls.default_path, id=obj_id)
        print('calling', action_name, uri)
        args = [data] if data else []
        if action_name == 'patch':
            action = client.patch
        if action_name == 'get':
            action = client.get
        if action_name == 'delete':
            action = client.delete
        request = action(uri, *args, format='json')
        return request

    @classmethod
    def _general_call(cls, client, action_name, data=None):
        # Patch new Object with the given data
        uri = cls.general_path.format(default_path=cls.default_path)
        print('calling', action_name, uri)
        args = [data] if data else []
        if action_name == 'post':
            action = client.post
        if action_name == 'get':
            action = client.get
        request = action(uri, *args, format='json')
        return request

    @classmethod
    def partially_update(cls, client, obj_id, data=None, sample_name='default'):
        data = cls._get_data(data, sample_name)
        return cls._specific_call(client, 'patch', obj_id, data)

    @classmethod
    def retrieve(cls, client, obj_id):
        return cls._specific_call(client, 'get', obj_id)

    @classmethod
    def delete(cls, client, obj_id):
        return cls._specific_call(client, 'delete', obj_id)

    @classmethod
    def create(cls, client, data=None, sample_name='default'):
        data = cls._get_data(data, sample_name)
        return cls._general_call(client, 'post', data)

    @classmethod
    def list(cls, client):
        return cls._general_call(client, 'get')

    @classmethod
    def non_deleted_objects_count(cls, exclude_deleted=True, **filters):
        if exclude_deleted:
            filters['deleted'] = False
        return cls.model_class.objects.filter(**filters).count()
