Prueba Técnica - CTS Turismo

Aplicación Full Stack para gestionar un sorteo de San Valentín.
Backend con Django + DRF + Celery/Redis y frontend con Vue 3 + Vite + Pinia.


***Tecnologías utilizadas***
Backend
-Python 3.11
-Django 4.2
-Django REST Framework 3.14
-SimpleJWT (autenticación administrador)
-Celery + Redis (tareas asíncronas para envío de correos)
-SQLite (para simplicidad en la prueba técnica)

Frontend
-Vue 3 + Vite
-Vue Router
-Pinia (estado global)
-Bootstrap 5

Infraestructura
-Docker + Docker Compose
-Variables de entorno con .env

***Instrucciones de instalación***
1-Clonar el repositorio:
git clone https://github.com/lmillar2i2/cts.git

2-Levantar servicios con Docker:
docker-compose up --build

Al ejecutar se inicia:
Backend en http://localhost:8000
Frontend en http://localhost:5173
Redis (cola de tareas)
Celery Worker

3-Crear superusuario para el panel admin de Django:
docker exec -it cts_backend python manage.py createsuperuser

4-Variables de entorno en backend/.env:
DEBUG=True
SECRET_KEY=supersecret
ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOWED_ORIGINS=http://localhost:5173

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=no-reply@cts-turismo.cl


***Flujo del concurso***

1-Registro: 
-El usuario ingresa nombre, email y teléfono.
-Valida duplicados.
-Envía correo de verificación (asíncrono con Celery).

2-Verificación de correo: 
-El usuario hace clic en el link recibido.

3-Creación de contraseña: 
-El usuario define su clave y queda participando.
-Activa estado is_verified=True.

4-Confirmación de participación: 
-Mensaje en frontend.
5-Login administrador: 
-Acceso protegido con JWT.
6-Panel de administración:
-Lista de concursantes (filtro verificados / no verificados).
-Sorteo aleatorio con botón (Realizar sorteo) que genera un registro en Winner.
-Notificación automática al ganador (correo enviado por Celery).


***Endpoints principales***
Registro: POST /api/register/
Verificación: GET /api/verify/<token>/
Crear contraseña: POST /api/set-password/
Login admin: POST /api/admin/login/
Listar participantes: GET /api/admin/participants/ (JWT requerido)
Sortear ganador: POST /api/admin/draw/ (JWT requerido)
Retorna participante ganador y envía correo.


***Decisiones técnicas***
SQLite: elegido por simplicidad en esta prueba; fácilmente reemplazable por PostgreSQL.
Pinia: manejo de estado global más moderno y recomendado que Vuex.
Bootstrap: usado para estilos rápidos y estándar; en producción se podría optar por TailwindCSS.
Docker Compose: entrega consistente de backend, frontend, Celery y Redis.
Correos: backend configurado con console.EmailBackend para debug; en producción se reemplazaría por SMTP real.

***Tests***
Incluye un test de registro en participants/tests.py:
-Registro exitoso
-Registro con email duplicado
Ejecución de tests:
-docker exec -it cts_backend python manage.py test