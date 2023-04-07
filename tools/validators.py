from core.models import Car
from rest_framework import serializers

# def is_car_specification_valid(json_dict):
#     key_set = set(json_dict.keys())
#     fields_set = {i.name for i in Car._meta.get_fields()}
#     if not fields_set.issuperset(key_set):
#         raise serializers.ValidationError("Json string fields are invalid")
