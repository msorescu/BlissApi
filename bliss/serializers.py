__author__ = 'msorescu'

from django.forms import widgets
from rest_framework import serializers
from .models import Picture


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture

