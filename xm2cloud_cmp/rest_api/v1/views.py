#! -*- coding: utf-8 -*-


from rest_framework import generics, permissions, authentication


from ... import models
from . import serializers


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return False


class ScriptListApiView(generics.ListCreateAPIView):
    queryset = models.Script.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.ScriptSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]


class ScriptDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Script.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.ScriptSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
