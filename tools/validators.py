from requests import Response
from rest_framework import status


def is_valid_id(model_id):
    if not model_id.isnumeric():
        return Response(
            {"error": "ID must be a number"}, status=status.HTTP_400_BAD_REQUEST
        )
