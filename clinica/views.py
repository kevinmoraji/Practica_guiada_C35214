from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import Propietario, Mascota, ConsultaVeterinaria
from .serializers import PropietarioSerializer, MascotaSerializer, ConsultaSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

def inicio(request):
    return HttpResponse("API de Gestión Veterinaria activa")

class MascotaListCreateView(generics.ListCreateAPIView):
    serializer_class = MascotaSerializer

    def get_queryset(self):
        queryset = Mascota.objects.all()

        especie = self.request.query_params.get('especie')
        if especie:
            queryset = queryset.filter(especie__iexact=especie)

        activas = self.request.query_params.get('activas')
        if activas is not None:
            valor= activas.lower() == 'true'
            queryset = queryset.filter(activo=valor)

        propietario= self.request.query_params.get('propietario')
        if propietario:
            queryset = queryset.filter(propietario_id=propietario)

        return queryset     
            
class MascotaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer

class PropietarioListCreateView(generics.ListCreateAPIView):
    queryset = Propietario.objects.all()
    serializer_class = PropietarioSerializer

class ConsultaListCreateView(generics.ListCreateAPIView):
    queryset = ConsultaVeterinaria.objects.all()
    serializer_class = ConsultaSerializer  


@api_view(['GET'])
@permission_classes([IsAdminUser])
def estadisticas(request):
    total_mascotas = Mascota.objects.count()
    total_propietarios = Propietario.objects.count()
    mascotas_activas = Mascota.objects.filter(activo=True).count()
    total_consultas = ConsultaVeterinaria.objects.count()

    return Response({
        'total_mascotas': total_mascotas,
        'total_propietarios': total_propietarios,
        'mascotas_activas': mascotas_activas,
        'total_consultas': total_consultas
    })          

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
    })

@api_view(['GET'])
def sesion(request):
    contador = request.session.get('contador', 0)
    contador += 1
    request.session['contador'] = contador

    return Response({'contador': contador})