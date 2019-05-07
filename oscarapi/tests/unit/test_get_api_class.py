from mock import patch
from oscarapi.tests.utils import APITest
from django.urls import reverse
import oscarapi.utils.loading as loading
from django.contrib.auth import get_user_model

User = get_user_model()

class ApiOverrideTest(APITest):

    def test_login_serializer_can_be_extended(self):
        user = User.objects.first()

        # get the standard serializer
        login_serializer = loading.get_api_class("serializers.login", "LoginSerializer")
        login_data = login_serializer(instance=user).data
        self.assertNotIn("my_extension", login_data, "The serializer should not have any extension")

        # now get the serializer again, but with the OSCARAPI_OVERRIDE_MODULES
        with patch.object(loading, "OSCARAPI_OVERRIDE_MODULES", ["oscarapi.tests"]):
            login_serializer = loading.get_api_class("serializers.login", "LoginSerializer")
            login_data = login_serializer(instance=user).data
            self.assertIn("my_extension", login_data, "The serialzier should have an extension")
