from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Propietario, Mascota
from .serializers import MascotaSerializer, ConsultaSerializer


class MascotaSerializerTestCase(APITestCase):
    def setUp(self):
        self.propietario = Propietario.objects.create(
            identificacion='123456789',
            nombre='Aracely Araya',
        )

    def test_peso_mascota_invalido(self):
        data = {
            'nombre': 'Luca',
            'especie': 'Perro',
            'peso': 0,
            'propietario': self.propietario.id
        }
        serializer = MascotaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('peso', serializer.errors)


class ConsultaSerializerTestCase(APITestCase):
    def setUp(self):
        self.propietario = Propietario.objects.create(
            identificacion='1289',
            nombre='Jimena Fonseca',
        )
        self.mascota = Mascota.objects.create(
            nombre='Paco',
            especie='Gato',
            peso=3.5,
            propietario=self.propietario
        )

    def test_costo_negativo_invalido(self):
        data = {
            'mascota': self.mascota.id,
            'motivo': 'Chequeo general',
            'costo': -50
        }
        serializer = ConsultaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('costo', serializer.errors)         

class PerfilEndPointTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('perfil')

    def test_perfil_sin_autenticacion_rechazado(self): 
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_perfil_autenticado_devuelve_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')       

class EstadisticasEndPointTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='regular', password='regupass')
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', is_staff=True)
        self.url = reverse('estadisticas')

    def test_estadisticas_usuario_regular_rechazado(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_estadisticas_admin_devuelve_200(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)        