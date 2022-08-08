from http import HTTPStatus

from marshmallow import ValidationError


class Response:
    """
    Responsible for generating success or error response for apis
    """

    def __init__(self, status_code=HTTPStatus.OK, message=None, errors=None, data=None, ):
        self.status_code = status_code
        self.message = message
        self.data = data
        self.errors = errors

    def send_error_response(self):
        """
        generate response with error message and status code
        :return: send error response
        """
        response = {'error': self.status_code.description if not self.message else self.message}
        if self.errors:
            response = self.errors
        return response, self.status_code

    def send_success_response(self):
        """
        generate response with  message ,status code and data (if applicable)
        :return: send error response
        """
        response = {'message': 'Success' if not self.message else self.message}
        if self.data:
            response["data"] = self.data
        return response, self.status_code


class Serializer:
    @staticmethod
    def load(request_data, request_schema):
        """
        it load requested_data and Validate it by validation define in request_schema
        :param instance:
        :param request_data: data received from request body
        :param request_schema: marshmallow schema to be used
        :return:
        """
        request_data = request_data.get_json()

        if (request_data is None) or (not request_data):
            return False, None
        try:
            data = request_schema.load(request_data)
            return True, data
        except ValidationError as e:
            return False, e.messages

    @staticmethod
    def dump(data=None, schema=None, extra_data=None):
        """
        it dump the data(python object to json data)
        :param extra_data: if there is extra_data to be dumped
        :param schema: Marshmallow schema
        :param data: any python object
        :return: data in json format
        """
        data = schema.dump(data)
        if extra_data:
            data.update(extra_data)
        return data
