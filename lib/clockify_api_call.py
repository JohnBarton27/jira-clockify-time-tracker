from lib.api_call import ApiCall
from lib.exceptions import ClockifyApiKeyNotSetException
from lib.variable import Variable


class ClockifyApiCall(ApiCall):

    # Environment Variable Names
    clockify_key_var_name = "CLOCKIFY_API_KEY"

    @property
    def clockify_api_key(self):
        return Variable(ClockifyApiCall.clockify_key_var_name).value

    def validate_environment(self):
        # Clockify Token
        if not self.clockify_api_key:
            raise ClockifyApiKeyNotSetException("{} environment variable not set - unable to perform Clockify REST "
                                                "API calls!".format(ClockifyApiCall.clockify_key_var_name))

    def exec(self):
        self.validate_environment()

        header = {"X-Api-Key": self.clockify_api_key}
        full_url = "https://api.clockify.me/api/v1/{}".format(self.url)

        response = self.type.requests_function(full_url, headers=header, json=self.data)
        return response
