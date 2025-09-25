# Prueba Técnica - CTS Turismo

Aplicación Full Stack para gestionar un sorteo de San Valentín.  
Backend con Django + DRF + Celery/Redis y frontend con Vue 3 + Vite + Pinia.

---

## Tecnologías utilizadas

### Backend
- Python 3.11  
- Django 4.2  
- Django REST Framework 3.14  
- SimpleJWT (autenticación administrador)  
- Celery + Redis (tareas asíncronas para envío de correos)  
- SQLite (para simplicidad en la prueba técnica)  

### Frontend
- Vue 3 + Vite  
- Vue Router  
- Pinia (estado global)  
- Bootstrap 5  

### Infraestructura
- Docker + Docker Compose  
- Variables de entorno con `.env`  
- MailHog (captura correos de prueba en interfaz web; inicialmente se revisaban en consola)  

---

## Instrucciones de instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/lmillar2i2/cts.git
   cd cts


2. **Levantar servicios con Docker**
    ```bash
    docker-compose up --build

Al ejecutar se inicia:
- Backend [http://localhost:8000/admin](http://localhost:8000/admin) (Admin de Django)  
- Frontend [http://localhost:5173](http://localhost:5173)  
- Redis (cola de tareas)  
- Celery Worker  
- MailHog (SMTP y bandeja web) → [http://localhost:8025](http://localhost:8025)  

### 3. Crear superusuario para el panel admin de Django
```bash
docker exec -it cts_backend python manage.py createsuperuser
```


### 4. Variables de entorno en `backend/.env`
```env
DEBUG=True
SECRET_KEY=supersecret
ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOWED_ORIGINS=http://localhost:5173
CSRF_TRUSTED_ORIGINS=http://localhost:5173
TIME_ZONE=America/Santiago

# Celery y Redis
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=mailhog
EMAIL_PORT=1025
DEFAULT_FROM_EMAIL=no-reply@cts-turismo.cl
```

## Flujo del concurso

1. **Registro**  
   - El usuario ingresa nombre, email y teléfono.  
   - Se validan duplicados.  
   - Se envía correo de verificación (asíncrono con Celery).  

2. **Verificación de correo**  
   - El usuario hace clic en el link recibido.  

3. **Creación de contraseña**  
   - El usuario define su clave y queda participando.  
   - Se activa el estado `is_verified=True`.  

4. **Confirmación de participación**  
   - Mensaje en el frontend.  

5. **Login administrador**  
   - Acceso protegido con JWT.  

6. **Panel de administración**  
   - Lista de concursantes (filtro verificados / no verificados).  
   - Sorteo aleatorio con botón **“Realizar sorteo”** que genera un registro en `Winner`.  
   - Notificación automática al ganador (correo enviado por Celery).  



## Endpoints principales

- **Registro**: `POST /api/register/`  
- **Verificación**: `GET /api/verify/<token>/`  
- **Crear contraseña**: `POST /api/set-password/`  
- **Login admin**: `POST /api/admin/login/`  
- **Listar participantes**: `GET /api/admin/participants/` (JWT requerido)  
- **Sortear ganador**: `POST /api/admin/draw/` (JWT requerido, retorna participante ganador y envía correo)  


## Decisiones técnicas

- **SQLite**: Elegido por simplicidad en esta prueba; fácilmente reemplazable por PostgreSQL.  
- **Pinia**: Manejo de estado global más moderno y recomendado que Vuex.  
- **Bootstrap**: Usado para estilos rápidos y estándar; en producción se podría optar por TailwindCSS.  
- **Docker Compose**: Entrega más consistente de backend, frontend, Celery, Redis y MailHog.  
- **Correos**: En este entorno se capturan en [MailHog](http://localhost:8025). En producción se usaría SMTP real.  


## Tests

Incluye un test de registro en `participants/tests.py`:
- Registro exitoso  
- Registro con email duplicado  

**Ejecución de tests:**
```bash
docker exec -it cts_backend python manage.py test
```

## Video Demo
Disponible en YouTube: [https://youtu.be/TwTsxkuHnoA](https://youtu.be/TwTsxkuHnoA)


## Notas de desarrollo
El proyecto fue desarrollado y probado en **WSL2 (Ubuntu 22.04)** con Docker Desktop.  
Sin embargo, la ejecución está contenida en Docker, por lo que debería correr igual en **Linux/Mac/Windows**, siempre que se tenga Docker instalado.  

