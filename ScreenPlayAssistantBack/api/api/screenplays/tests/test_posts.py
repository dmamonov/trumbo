# """Post tests."""
#
# # Models
# from api.posts.models import Post
#
# # Utils
# from api.posts.factories import PostFactory
# from api.users.tests.test_users import UserTestHelper
# from api.utils.tests import DefaultTestHelper
# from rest_framework.test import APITestCase
# from rest_framework import status
#
#
# # Post helper
# class PostTestHelper(DefaultTestHelper):
#     default_path='posts'
#     model_class = Post
#     factory = PostFactory
#     sample_data = {
#         'default': {}
#     }
#
#
# class AdminUserPostApiTestCase(APITestCase):
#
#     def setUp(self):
#         # Create user
#         self.admin = UserTestHelper.force_create(client=self.client, sample_name='super_admin', force_auth=True)
#
#     def test_endpoint_responses_code(self):
#         creation_request = PostTestHelper.create(self.client)
#         self.assertEqual(creation_request.status_code, status.HTTP_201_CREATED)
#
#         list_request = PostTestHelper.list(self.client)
#         self.assertEqual(list_request.status_code, status.HTTP_200_OK)
#
#         retrieve_request = PostTestHelper.retrieve(self.client, creation_request.data['id'])
#         self.assertEqual(retrieve_request.status_code, status.HTTP_200_OK)
#
#         patch_request = PostTestHelper.partially_update(self.client, creation_request.data['id'])
#         self.assertEqual(patch_request.status_code, status.HTTP_200_OK)
#
#     def test_object_creation(self):
#         self.assertEqual(PostTestHelper.non_deleted_objects_count(), 0)
#         creation_request = PostTestHelper.create(self.client)
#         self.assertEqual(PostTestHelper.non_deleted_objects_count(), 1)
#         PostTestHelper.delete(self.client, creation_request.data['id'])
#         self.assertEqual(PostTestHelper.non_deleted_objects_count(), 0)
