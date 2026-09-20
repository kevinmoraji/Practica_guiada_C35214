## Instalación y ejecución

1. Clonar el repositorio y entrar a la carpeta del proyecto
2. Crear el entorno virtual: `python -m venv .venv`
3. Activar el entorno virtual: `.venv\Scripts\activate` (Windows)
4. Instalar dependencias: `pip install "Django>=5.2,<5.3" djangorestframework`
5. Aplicar migraciones: `python manage.py migrate`
6. Crear un superusuario (que es opcional, para el admin): `python manage.py createsuperuser`
7. Levantar el servidor: `python manage.py runserver`
8. La API queda en `http://127.0.0.1:8000/clinica/`


## Usuarios de prueba

- usuario1 / Vetclinica2026 - usuario regular
- adminvet / AdminVet2026 - administrador

##Documentacion de las consultas

## Bloque 3 – ORM aplicado al dominio veterinario

### 1. Listar todas las mascotas
\```python
Mascota.objects.all()
\```
Resultado:
\```
<QuerySet [<Mascota: Bolita>, <Mascota: Folsi>, <Mascota: Garfiel>, <Mascota: Koral>,
<Mascota: Loki>, <Mascota: Paco>, <Mascota: Rocky>, <Mascota: Zooe>]>
\```

### 2. Ordenar las mascotas alfabéticamente por nombre
\```python
Mascota.objects.order_by('nombre')
\```
Resultado:
\```
<QuerySet [<Mascota: Bolita>, <Mascota: Folsi>, <Mascota: Garfiel>, <Mascota: Koral>,
<Mascota: Loki>, <Mascota: Paco>, <Mascota: Rocky>, <Mascota: Zooe>]>
\```

### 3. Obtener únicamente mascotas activas
\```python
Mascota.objects.filter(activo=True)
\```
Resultado:
\```
<QuerySet [<Mascota: Loki>, <Mascota: Bolita>, <Mascota: Paco>, <Mascota: Garfiel>,
<Mascota: Rocky>, <Mascota: Folsi>, <Mascota: Zooe>]>
\```
(Koral queda excluida por estar inactiva)

### 4. Obtener mascotas cuyo peso sea mayor que 10
\```python
Mascota.objects.filter(peso__gt=10)
\```
Resultado:
\```
<QuerySet [<Mascota: Loki>, <Mascota: Paco>, <Mascota: Rocky>, <Mascota: Koral>]>
\```

### 5. Buscar mascotas cuya especie sea 'Perro'
\```python
Mascota.objects.filter(especie='Perro')
\```
Resultado:
\```
<QuerySet [<Mascota: Loki>, <Mascota: Paco>, <Mascota: Rocky>, <Mascota: Koral>, <Mascota: Zooe>]>
\```

### 6. Buscar propietarios cuyo nombre contenga una palabra, sin distinguir mayúsculas/minúsculas
\```python
Propietario.objects.filter(nombre__icontains='fonseca')
\```
Resultado:
\```
<QuerySet [<Propietario: Pedro Fonseca Araya>, <Propietario: Aracely Araya Fonseca>,
<Propietario: Jimena Fonseca Alvarado>]>
\```

### 7. Obtener todas las mascotas de un propietario específico utilizando la relación
\```python
propietario = Propietario.objects.get(nombre='Kevin Mora Jimenez')
propietario.mascotas.all()
\```
Resultado:
\```
<QuerySet [<Mascota: Loki>, <Mascota: Rocky>, <Mascota: Folsi>]>
\```

### 8. Actualizar el peso de una mascota
\```python
mascota = Mascota.objects.get(nombre='Loki')
mascota.peso = 27.50
mascota.save()
mascota.peso
\```
Resultado:
\```
27.5
\```

### 9. Eliminar una consulta veterinaria de prueba
\```python
ConsultaVeterinaria.objects.count()   # 8
consulta = ConsultaVeterinaria.objects.filter(mascota__nombre='Rocky').first()
consulta.delete()
ConsultaVeterinaria.objects.count()   # 7
\```
Resultado:
\```
(1, {'clinica.ConsultaVeterinaria': 1})
\```

### Pregunta de análisis
**¿Qué significa `peso__gt=10` y qué representa el doble guion bajo en los lookups del ORM?**

El doble guion bajo es la sintaxis que Django ORM tiene para usar un operador
de comparación sobre un campo del modelo. En `peso__gt=10`, peso es el campo y gt significa mayor que


**Explique la diferencia entre autenticación y autorización utilizando los dos endpoints anteriores**

La autenticación verifica quién es el usuario que hace la petición mediante un token válido enviado en el header Authorization. Si no hay token o es inválido, la petición es rechazada antes de saber siquiera qué permisos tiene esa persona ,cualquier usuario autenticado sin importar su rol puede acceder. La autorización determina que puede hacer ese usuario ya autenticado


**Explique por qué una sesión permite mantener estado aunque HTTP sea un protocolo sin estado.**

HTTP no recuerda nada entre peticiones Django usa sesiones para solucionar esto guarda datos en el servidor y le da al cliente una cookie con un id. En cada petición el cliente manda esa cookie y el servidor busca los datos guardados con ese id, entonces se simula memoria aunque HTTP no la tenga




## Documentacion de la API

- GET `/clinica/` - verifica que la API está activa. Respuesta: texto plano. Código: 200
- GET `/clinica/api/mascotas/` - lista mascotas, paginado de a 5. Query params opcionales: page, especie, activas, propietario. Código: 200
- POST `/clinica/api/mascotas/` - registra una mascota. Body: nombre, especie, raza, fecha_nacimiento, peso, activo, propietario. Códigos: 201 / 400
- GET `/clinica/api/mascotas/<id>/` - detalle de una mascota. Códigos: 200 / 404
- PUT `/clinica/api/mascotas/<id>/` - actualiza una mascota completa. Códigos: 200 / 400 / 404
- PATCH `/clinica/api/mascotas/<id>/` - actualiza parcialmente una mascota. Códigos: 200 / 400 / 404
- DELETE `/clinica/api/mascotas/<id>/` - elimina una mascota. Códigos: 204 / 404
- GET `/clinica/api/propietarios/` - lista propietarios. Código: 200
- POST `/clinica/api/propietarios/` - registra un propietario. Body: identificacion, nombre, telefono, email. Códigos: 201 / 400
- GET `/clinica/api/consultas/` - lista consultas. Código: 200
- POST `/clinica/api/consultas/` - registra una consulta. Body: mascota, motivo, diagnostico, tratamiento, costo. Códigos: 201 / 400
- POST `/clinica/api/token/` - obtiene un token de autenticacion. Body: username, password. Códigos: 200 / 400
- GET `/clinica/api/perfil/` - devuelve datos del usuario autenticado. Requiere header Authorization: Token. Códigos: 200 / 401
- GET `/clinica/api/estadisticas/` - totales del sistema, solo administradores. Requiere header Authorization: Token. Códigos: 200 / 401 / 403
- GET `/clinica/api/sesion/` - contador de accesos via sesion. Código: 200


## Reflexión final

1. Postman manda un POST a `/clinica/api/consultas/` con los datos en JSON
2. La URL redirige la petición a la View
3. La View le pasa los datos al Serializer
4. El Serializer valida que el costo no sea negativo y el motivo no esté vacío
5. Si algo está mal, devuelve 400 con el error. Si todo está bien, sigue
6. El Serializer usa el Model para guardar el registro con el ORM
7. Django devuelve la Response con los datos guardados y el código 201