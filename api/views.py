from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from rest_framework.views import APIView
from rest_framework import status
from api.models import Countdown, CountdownEvent
from api.serializers import CountdownSerializer, CountdownEventSerializer, CountdownPublicSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


def hello_world(request):
    return HttpResponse("Hello World")


@method_decorator(csrf_exempt, name='dispatch')
class CountdownList(APIView):
    def get(self, request, format=None): #todo: remove key from list view
        countdowns = Countdown.objects.all().order_by('-id')[:10]
        serializer = CountdownSerializer(countdowns, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        serializer = CountdownSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class CountdownDetail(APIView):
    def get_object(self, id):
        try:
            return Countdown.objects.get(pk=id)
        except Countdown.DoesNotExist:
            raise Http404

    def get(self, request, countdown_id, format=None):
        countdown = self.get_object(countdown_id)
        serializer = None
        if countdown.key != request.GET.get("key", ''):
            serializer = CountdownPublicSerializer(countdown)
        else:
            serializer = CountdownSerializer(countdown)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, countdown_id, format=None):
        snippet = self.get_object(countdown_id)
        if snippet.key != request.GET["key"]:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)
        serializer = CountdownSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, countdown_id, format=None):
        snippet = self.get_object(countdown_id)
        if snippet.key != request.GET["key"]:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@method_decorator(csrf_exempt, name='dispatch')
class CountdownEventList(APIView):
    def get(self, request, format=None):
        countdown_id = request.GET.get('countdown_id', '')
        if countdown_id == '':
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        countdown_events = CountdownEvent.objects.filter(countdown=request.GET.get('countdown_id', ''))
        serializer = CountdownSerializer(countdown_events, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        serializer = CountdownEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)