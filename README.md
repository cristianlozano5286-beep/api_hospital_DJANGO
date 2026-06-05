
# 🏥 API Sistema de Gestión Hospitalaria

API REST construida con **Django 5**, **Django REST Framework** y **PostgreSQL** para la gestión integral de una clínica: pacientes, médicos, especialidades, citas, tratamientos, medicamentos, facturación y pagos.

---

## 📋 Tabla de contenido

1. [Requisitos](#requisitos)
2. [Instalación y configuración](#instalación-y-configuración)
3. [Base de datos](#base-de-datos)
4. [Ejecución](#ejecución)
5. [Endpoints de la API](#endpoints-de-la-api)
6. [Documentación interactiva](#documentación-interactiva)
7. [Modelo de datos](#modelo-de-datos)
8. [Buenas prácticas aplicadas](#buenas-prácticas-aplicadas)
9. [Control de versiones](#control-de-versiones)

---

## Requisitos

| Herramienta | Versión mínima |
|-------------|---------------|
| Python      | 3.11+         |
| PostgreSQL  | 15+           |
| pip         | 23+           |
| Git         | 2.40+         |

---

## Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/hospital-api.git
cd hospital-api
```

### 2. Crear y activar entorno virtual

```bash
# Linux / macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Edite el archivo `.env` con sus credenciales:

```ini
SECRET_KEY=django-insecure-cambie-esta-clave-en-produccion
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=hospital_db
DB_USER=postgres
DB_PASSWORD=su_contraseña
DB_HOST=localhost
DB_PORT=5432
DB_SCHEMA=hospital

PAGE_SIZE=10
```

---

## Base de datos

### 1. Crear la base de datos y el esquema en PostgreSQL

```bash
psql -U postgres -f schema_hospital.sql
```

Este script realiza:
- Crea el esquema `hospital`
- Crea las 8 tablas con sus restricciones e índices
- Agrega trigger automático para `fecha_modificacion`
- Inserta datos iniciales de especialidades

### 2. Ejecutar migraciones de Django

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Crear superusuario (opcional, para el admin)

```bash
python manage.py createsuperuser
```

---

## Ejecución

```bash
python manage.py runserver
```

El servidor inicia en: `http://127.0.0.1:8000/`

---

## Endpoints de la API

Base URL: `http://localhost:8000/api/v1/`

### Especialidades

| Método   | Endpoint                           | Descripción                        |
|----------|------------------------------------|------------------------------------|
| `GET`    | `/especialidades/`                 | Listar todas las especialidades    |
| `POST`   | `/especialidades/`                 | Crear especialidad                 |
| `GET`    | `/especialidades/{id}/`            | Obtener especialidad por ID        |
| `PUT`    | `/especialidades/{id}/`            | Actualizar especialidad completa   |
| `PATCH`  | `/especialidades/{id}/`            | Actualizar parcialmente            |
| `DELETE` | `/especialidades/{id}/`            | Desactivar especialidad (soft)     |
| `PATCH`  | `/especialidades/{id}/activar/`    | Reactivar especialidad             |

### Médicos

| Método   | Endpoint                       | Descripción                          |
|----------|--------------------------------|--------------------------------------|
| `GET`    | `/medicos/`                    | Listar médicos (filtrar por especialidad) |
| `POST`   | `/medicos/`                    | Registrar médico                     |
| `GET`    | `/medicos/{id}/`               | Obtener médico                       |
| `PUT`    | `/medicos/{id}/`               | Actualizar médico                    |
| `PATCH`  | `/medicos/{id}/`               | Actualizar parcialmente              |
| `DELETE` | `/medicos/{id}/`               | Desactivar médico (soft)             |
| `PATCH`  | `/medicos/{id}/activar/`       | Reactivar médico                     |

### Pacientes

| Método   | Endpoint                        | Descripción                        |
|----------|---------------------------------|------------------------------------|
| `GET`    | `/pacientes/`                   | Listar pacientes                   |
| `POST`   | `/pacientes/`                   | Registrar paciente                 |
| `GET`    | `/pacientes/{id}/`              | Obtener paciente                   |
| `PUT`    | `/pacientes/{id}/`              | Actualizar paciente                |
| `PATCH`  | `/pacientes/{id}/`              | Actualizar parcialmente            |
| `DELETE` | `/pacientes/{id}/`              | Desactivar paciente (soft)         |
| `PATCH`  | `/pacientes/{id}/activar/`      | Reactivar paciente                 |
| `GET`    | `/pacientes/{id}/citas/`        | Historial de citas del paciente    |

### Citas

| Método   | Endpoint                        | Descripción                          |
|----------|---------------------------------|--------------------------------------|
| `GET`    | `/citas/`                       | Listar citas (filtrar por estado, médico, paciente) |
| `POST`   | `/citas/`                       | Programar cita                       |
| `GET`    | `/citas/{id}/`                  | Obtener cita                         |
| `PUT`    | `/citas/{id}/`                  | Actualizar cita                      |
| `PATCH`  | `/citas/{id}/`                  | Actualizar parcialmente              |
| `DELETE` | `/citas/{id}/`                  | Cancelar cita (soft)                 |
| `PATCH`  | `/citas/{id}/estado/`           | Cambiar estado de la cita            |

### Medicamentos

| Método   | Endpoint                          | Descripción                    |
|----------|-----------------------------------|--------------------------------|
| `GET`    | `/medicamentos/`                  | Listar catálogo de medicamentos|
| `POST`   | `/medicamentos/`                  | Agregar medicamento            |
| `GET`    | `/medicamentos/{id}/`             | Obtener medicamento            |
| `PUT`    | `/medicamentos/{id}/`             | Actualizar medicamento         |
| `PATCH`  | `/medicamentos/{id}/`             | Actualizar parcialmente        |
| `DELETE` | `/medicamentos/{id}/`             | Desactivar medicamento (soft)  |
| `PATCH`  | `/medicamentos/{id}/activar/`     | Reactivar medicamento          |

### Tratamientos

| Método   | Endpoint                      | Descripción                        |
|----------|-------------------------------|------------------------------------|
| `GET`    | `/tratamientos/`              | Listar tratamientos (filtrar por cita) |
| `POST`   | `/tratamientos/`              | Prescribir tratamiento             |
| `GET`    | `/tratamientos/{id}/`         | Obtener tratamiento                |
| `PUT`    | `/tratamientos/{id}/`         | Actualizar tratamiento             |
| `PATCH`  | `/tratamientos/{id}/`         | Actualizar parcialmente            |
| `DELETE` | `/tratamientos/{id}/`         | Desactivar tratamiento (soft)      |

### Facturas

| Método   | Endpoint                          | Descripción                      |
|----------|-----------------------------------|----------------------------------|
| `GET`    | `/facturas/`                      | Listar facturas                  |
| `POST`   | `/facturas/`                      | Emitir factura                   |
| `GET`    | `/facturas/{id}/`                 | Obtener factura con saldo        |
| `PUT`    | `/facturas/{id}/`                 | Actualizar factura               |
| `PATCH`  | `/facturas/{id}/`                 | Actualizar parcialmente          |
| `DELETE` | `/facturas/{id}/`                 | Anular factura (soft)            |
| `POST`   | `/facturas/{id}/calcular-total/`  | Recalcular total de factura      |

### Pagos

| Método   | Endpoint               | Descripción                        |
|----------|------------------------|------------------------------------|
| `GET`    | `/pagos/`              | Listar pagos (filtrar por factura) |
| `POST`   | `/pagos/`              | Registrar pago                     |
| `GET`    | `/pagos/{id}/`         | Obtener pago                       |
| `PUT`    | `/pagos/{id}/`         | Actualizar pago                    |
| `PATCH`  | `/pagos/{id}/`         | Actualizar parcialmente            |
| `DELETE` | `/pagos/{id}/`         | Desactivar pago (soft)             |

### Parámetros de consulta disponibles

```
?search=texto          Búsqueda por texto en campos configurados
?ordering=campo        Ordenar por campo (- para descendente)
?page=N                Paginación (10 registros por página por defecto)
?activo=true/false     Filtrar por estado activo
?especialidad=ID       Filtrar médicos por especialidad
?estado=programada     Filtrar citas/facturas/pagos por estado
?paciente=ID           Filtrar citas/facturas por paciente
?cita=ID               Filtrar tratamientos por cita
?factura=ID            Filtrar pagos por factura
```

---

## Documentación interactiva

| URL                              | Descripción                    |
|----------------------------------|--------------------------------|
| `http://localhost:8000/api/docs/`  | Swagger UI (interactivo)       |
| `http://localhost:8000/api/redoc/` | ReDoc (documentación limpia)   |
| `http://localhost:8000/api/schema/`| Esquema OpenAPI 3.0 (JSON/YAML)|

---

## Modelo de datos

```
Especialidad ──< Médico
Paciente     ──< Cita >── Médico
Cita         ──< Tratamiento >── Medicamento
Paciente     ──< Factura
Cita         ──< Factura  (opcional)
Factura      ──< Pago
```

### Campos auditables en todas las tablas

Todas las tablas implementan los campos requeridos por la guía:

| Campo               | Tipo          | Descripción                    |
|---------------------|---------------|--------------------------------|
| `activo`            | Boolean       | Soft-delete flag               |
| `fecha_creacion`    | DateTimeField | Timestamp de inserción (auto)  |
| `fecha_modificacion`| DateTimeField | Timestamp de última edición (auto) |

---

## Buenas prácticas aplicadas

- **Modelo base abstracto** (`BaseModel`) con campos auditables heredados por todos los modelos
- **Soft delete** en todos los recursos: nunca se elimina, se desactiva
- **Validaciones en serializers** (médico/paciente activo al crear citas, monto > 0 en pagos)
- **Lógica de negocio en modelos**: actualización automática del estado de factura al registrar pagos
- **select_related / prefetch_related** para evitar el problema N+1
- **Variables de entorno** con `python-decouple` y `.env.example` versionado
- **Esquema PostgreSQL dedicado** (`hospital`) en lugar de `public`
- **Índices** en llaves foráneas y campos de búsqueda frecuente
- **Documentación OpenAPI** generada automáticamente con `drf-spectacular`
- **Paginación** configurable desde variables de entorno
- **Filtros de búsqueda y ordenamiento** en todos los ViewSets
- **Acciones personalizadas** (`@action`) para operaciones de negocio específicas
- **Triggers PostgreSQL** para mantener `fecha_modificacion` sincronizada

---

## Control de versiones

```bash
# Inicializar repositorio
git init
git add .
git commit -m "feat: implementación inicial API Sistema de Gestión Hospitalaria

- 8 modelos con campos auditables (activo, fecha_creacion, fecha_modificacion)
- CRUD completo con Django REST Framework
- Esquema PostgreSQL con 8 tablas, índices y triggers
- Documentación OpenAPI con drf-spectacular
- Configuración por variables de entorno (.env)
- Soft-delete en todos los recursos
- Validaciones de negocio en serializers y modelos"

# (Opcional) Conectar a repositorio remoto
git remote add origin https://github.com/tu-usuario/hospital-api.git
git push -u origin main
```

---

## Estructura del proyecto

```
hospital_api/
├── .env.example              ← Variables de entorno de ejemplo
├── .gitignore
├── manage.py
├── requirements.txt
├── schema_hospital.sql       ← Script SQL de creación de esquema
├── README.md
├── hospital_api/             ← Configuración Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── apps/
    ├── base.py               ← BaseModel abstracto
    ├── especialidades/       ← model · serializer · views · urls
    ├── medicos/
    ├── pacientes/
    ├── citas/
    ├── medicamentos/
    ├── tratamientos/
    ├── facturas/
    └── pagos/
```
=======
# api_hospital_DJANGO
SE CREA EL REPOSITORIO PARA EL API DE HOSPITAL
