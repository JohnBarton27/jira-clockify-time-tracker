from abc import ABC, abstractmethod
from enum import Enum

import requests


class RequestTypes(Enum):

    GET = 1
    PUT = 2
    POST = 3
    DELETE = 4

    @property
    def requests_function(self):
        if self.name == "GET":
            return requests.get
        elif self.name == "PUT":
            return requests.put
        elif self.name == "POST":
            return requests.post
        elif self.name == "DELETE":
            return requests.delete


class ApiCall(ABC):

    def __init__(self, req_type: RequestTypes, url: str, data: dict = None):
        self.type = req_type
        self.url = url
        self.data = data

    @abstractmethod
    def validate_environment(self):
        pass

    def exec(self):
        self.validate_environment()

        response = self.type.requests_function(self.url, json=self.data)
        return response