from rest_framework import serializers

from balance.models import Invested


class InvestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invested
        fields = "__all__"