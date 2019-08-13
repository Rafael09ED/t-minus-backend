from rest_framework import serializers
from api.models import Countdown, CountdownEvent
from django.utils import timezone


def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

class CountdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countdown
        fields = ('id','name', 'time', 'key')


class CountdownEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountdownEvent
        fields = ('id', 'name', 'countdown', 'text', 'time')

        
class CountdownPublicSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    time = serializers.DateTimeField()
    name = serializers.CharField()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        events = CountdownEvent.objects.filter(countdown=instance).order_by('time')
        current_time = timezone.now()
        current_e = None
        next_e = None
        for event in events:
            if (event.time < current_time):
                current_e = event
            else:
                next_e = event
                break
        if current_e is not None:
            ret['event_text'] = current_e.text
        if next_e is not None:
            ret['next_event'] = next_e.time
        return ret
