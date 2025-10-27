# Portal del Lago — Versión Mejorada (Full‑Stack)

Stack:
- **Frontend**: React + Vite + TypeScript + TailwindCSS
- **Backend**: Django 5 + Django REST Framework + SimpleJWT + Channels (WebSockets) + drf-spectacular (OpenAPI) + Redis
- **DB**: PostgreSQL
- **Realtime**: WebSockets (Channels)
- **Emails**: SMTP (en dev: consola); en prod: Setear SMTP real (.env)
- **Web Push**: pywebpush + Service Worker (VAPID)
- **Docker**: docker-compose con backend, frontend, db y redis

Roles: **SUPERADMIN**, **RECEPCION**, **MUCAMA**, **MANTENIMIENTO**

Módulos principales:
- **Incidentes** (reporte/estado/derivación)
- **Objetos Perdidos** (registro y entrega)
- **Tareas de Mantenimiento** (asignación/seguimiento)
- **Notificaciones** (email + push + realtime)
- **Autenticación** (registro, login, recuperación de contraseña)

---

## 1) Requisitos

- Docker + Docker Compose (recomendado)
- (Opcional modo local) Python 3.11+, Node 18+

## 2) Variables de entorno

Copiar `.env.example` a `.env` en la raíz y completar:

```
cp .env.example .env
```

Luego, **(opcional)** copiar también los ejemplos por servicio:
```
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

## 3) Ejecutar en desarrollo con Docker

```bash
docker compose up --build
# backend: http://localhost:8000
# frontend: http://localhost:5173
# OpenAPI: http://localhost:8000/api/schema/swagger/
```

Crear tablas y datos demo (primera vez en dev):
```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py loaddata fixtures/demo_users.json
docker compose exec backend python manage.py loaddata fixtures/demo_data.json
```

Crear superusuario:
```bash
docker compose exec backend python manage.py createsuperuser
```

## 4) Ejecutar sin Docker (modo local)
Backend:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```
Frontend:
```bash
cd frontend
npm i
cp .env.example .env
npm run dev
```

## 5) Despliegue en producción

### Opción A: VPS con Docker Compose (simple)
- Asegurar puertos 80/443 abiertos, y configurar un proxy (Nginx/Traefik) si deseas dominio HTTPS.
- Exportar variables reales en `.env` (DB, SECRET_KEY, CORS/CSRF, VAPID, SMTP, etc.).
- Ejecutar:
```bash
docker compose -f docker-compose.prod.yml up -d --build
```

### Opción B: Frontend en Vercel + Backend en Render/Railway
- **Frontend**: subí `/frontend` a Vercel (build: `npm run build`, output: `dist`).
- **Backend**: subí `/backend` a Render/Railway con Dockerfile o `gunicorn+daphne`. Añadir Redis & Postgres gestionados.
- Configurar CORS y CSRF en backend con el dominio del frontend.

## 6) Documentación de API
- **Swagger UI**: `/api/schema/swagger/`
- **OpenAPI JSON**: `/api/schema/`

## 7) Notificaciones Push
- Generar llaves VAPID (p. ej., con `web-push` o librería equivalente) y pegarlas en `.env` y `frontend/.env`.
- El frontend registra la suscripción y el backend la guarda en `core.NotificationSubscription`.
- Endpoint para disparar push: `POST /api/push/test/`.

## 8) Seguridad
- Django SecurityMiddleware, CSRF, CORS listo.
- Validación de datos en serializers.
- Rate limit sencillo (DRF throttling) pre-configurado.
- Cabeceras seguras (CSP/CORS configurables).

## 9) Datos de ejemplo (demo)
Usuarios (tras cargar fixtures):
- superadmin@example.com / `SuperAdmin123!`
- recepcion@example.com / `Recep123!`
- mucama@example.com / `Mucama123!`
- mantenimiento@example.com / `Mante123!`

## 10) Estructura general
```
PortalDelLagoImproved/
  backend/        # Django + DRF + Channels
  frontend/       # React + Vite + TS + Tailwind
  infra/          # (espacio para Nginx/CI/CD extra)
  docker-compose.yml
  docker-compose.prod.yml
  .env.example
  README.md
```
