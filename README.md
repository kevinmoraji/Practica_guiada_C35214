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

La autenticación verifica quién es el usuario que hace la petición mediante un token válido enviado en el header Authorization. Si no hay token o es inválido, la petición es rechazada antes de saber siquiera qué permisos tiene esa persona ,cualquier usuario autenticado, sin importar su rol, puede acceder. La autorización determina qué puede hacer ese usuario ya autenticado.


**Explique por qué una sesión permite mantener estado aunque HTTP sea un protocolo sin estado.**

HTTP no recuerda nada entre peticiones. Django usa sesiones para solucionar esto: guarda datos en el servidor y le da al cliente una cookie con un id. En cada petición, el cliente manda esa cookie y el servidor busca los datos guardados con ese id. Así se simula memoria aunque HTTP no la tenga.




## Documentacion de la API

| Método | URL | Descripción | Parámetros/Body | Respuesta | Códigos 
| GET | `/clinica/` | Verifica que la API está activa | Ninguno | Texto plano | 200 |
| GET | `/clinica/api/mascotas/` | Lista mascotas (paginado, 5 por página) | Query params opcionales: `page`, `especie`, `activas`, `propietario` | Objeto con `count`, `next`, `previous`, `results` | 200 |
| POST | `/clinica/api/mascotas/` | Registra una nueva mascota | Body JSON: `nombre`, `especie`, `raza`, `fecha_nacimiento`, `peso`, `activo`, `propietario` | Objeto de la mascota creada | 201 / 400 |
| GET | `/clinica/api/mascotas/<id>/` | Detalle de una mascota | Ninguno | Objeto de la mascota | 200 / 404 |
| PUT | `/clinica/api/mascotas/<id>/` | Actualiza una mascota (todos los campos) | Body JSON completo | Objeto actualizado | 200 / 400 / 404 |
| PATCH | `/clinica/api/mascotas/<id>/` | Actualiza parcialmente una mascota | Body JSON con los campos a cambiar | Objeto actualizado | 200 / 400 / 404 |
| DELETE | `/clinica/api/mascotas/<id>/` | Elimina una mascota | Ninguno | Sin contenido | 204 / 404 |
| GET | `/clinica/api/propietarios/` | Lista propietarios | Ninguno | Lista de propietarios | 200 |
| POST | `/clinica/api/propietarios/` | Registra un propietario | Body JSON: `identificacion`, `nombre`, `telefono`, `email` | Objeto creado | 201 / 400 |
| GET | `/clinica/api/consultas/` | Lista consultas veterinarias | Ninguno | Lista de consultas | 200 |
| POST | `/clinica/api/consultas/` | Registra una consulta | Body JSON: `mascota`, `motivo`, `diagnostico`, `tratamiento`, `costo` | Objeto creado | 201 / 400 |
| POST | `/clinica/api/token/` | Obtiene un token de autenticacion | Body JSON: `username`, `password` | `{ "token": "..." }` | 200 / 400 |
| GET | `/clinica/api/perfil/` | Devuelve datos del usuario autenticado | Header: `Authorization: Token <token>` | `id`, `username`, `email` | 200 / 401 |
| GET | `/clinica/api/estadisticas/` | Totales del sistema (solo administradores) | Header: `Authorization: Token <token>` | Totales de propietarios, mascotas, activas y consultas | 200 / 401 / 403 |
| GET | `/clinica/api/sesion/` | Contador de accesos via sesion | Ninguno | `{ "contador": n }` | 200 |