# API de Invitaciones — Guía para Frontend

## Conceptos

Existen dos tipos de invitaciones:

| Tipo | Descripción |
|------|-------------|
| **IES** | Tiene `institution` asignada. El usuario que se registra queda vinculado a esa institución. |
| **Genérica** | Sin institución. Los campos `reviewer`, `is_staff` e `is_superuser` del token se transfieren al usuario al registrarse. |

En ambos casos se genera una `destination_url` que el frontend usa para el
registro. Si el token tiene `email`, el sistema envía el correo automáticamente
al crearlo.

---

## Endpoints

Base URL: `/api/invitation/`

---

### 1. Crear invitación

**Requiere:** token de autenticación de un usuario **reviewer**.

```
POST /api/invitation/
Authorization: Token <auth_token>
Content-Type: application/json
```

**Body — invitación IES** (solo campo obligatorio: `institution`):
```json
{
  "institution": 3,
  "email": "contacto@universidad.mx"
}
```

**Body — invitación genérica** (`email` obligatorio, sin `institution`):
```json
{
  "email": "nueva.revisora@ejemplo.mx",
  "reviewer": true,
  "is_staff": false,
  "is_superuser": false
}
```

**Respuesta 201:**
```json
{
  "key": "550e8400-e29b-41d4-a716-446655440000",
  "email": "contacto@universidad.mx",
  "institution": 3,
  "institution_full": { "id": 3, "name": "UNAM", "acronym": "UNAM" },
  "created_at": "2026-02-27T10:00:00Z",
  "viewed_at": null,
  "used_at": null,
  "reviewer": false,
  "is_staff": false,
  "is_superuser": false,
  "destination_url": "https://app.onigies.mx/register?token=550e8400-..."
}
```

> Si el token tiene `email`, el sistema envía el correo automáticamente.
> Si no tiene `email`, el admin debe compartir `destination_url` manualmente.

---

### 2. Listar invitaciones

**Requiere:** token de reviewer.

```
GET /api/invitation/
Authorization: Token <auth_token>
```

**Filtros opcionales:**

| Query param | Efecto |
|-------------|--------|
| `?institution=<id>` | Solo tokens de esa institución |
| `?no_institution=true` | Solo tokens sin institución |
| (ninguno) | Todos los tokens |

**Respuesta 200:** lista de objetos con el mismo formato que la creación.

---

### 3. Consultar token de invitación

**Requiere:** ninguno (público). Úsalo cuando el usuario llega al frontend
con `?token=<uuid>` en la URL.

```
GET /api/invitation/<uuid>/
```

- Actualiza `viewed_at` la primera vez que se consulta.
- Devuelve 400 si el token ya fue utilizado (`used_at` no es nulo).

**Respuesta 200:**
```json
{
  "key": "550e8400-e29b-41d4-a716-446655440000",
  "email": "contacto@universidad.mx",
  "institution": 3,
  "institution_full": { "id": 3, "name": "UNAM", "acronym": "UNAM" },
  "created_at": "2026-02-27T10:00:00Z",
  "viewed_at": "2026-02-27T11:00:00Z",
  "used_at": null,
  "reviewer": false,
  "is_staff": false,
  "is_superuser": false,
  "destination_url": "https://app.onigies.mx/register?token=550e8400-..."
}
```

**Respuesta 400 (ya utilizado):**
```json
{ "detail": "La invitación ya ha sido utilizada." }
```

**Respuesta 404 (no existe):**
```json
{ "detail": "No encontrado." }
```

---

### 4. Registrar usuario con token

**Requiere:** ninguno (público). El usuario completa el formulario de registro.

```
POST /api/invitation/<uuid>/register/
Content-Type: application/json
```

**Body:**
```json
{
  "first_name": "Ana",
  "last_name": "García",
  "email": "ana@universidad.mx",
  "password": "contraseña123",
  "password_confirm": "contraseña123"
}
```

> El `email` puede diferir del que tiene la invitación.

**Respuesta 201** — igual al response de `/api/login/`, listo para auto-login:
```json
{
  "id": 42,
  "email": "ana@universidad.mx",
  "username": "ana@universidad.mx",
  "first_name": "Ana",
  "last_name": "García",
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "fullname": "Ana García",
  "reviewer": false,
  "is_staff": false,
  "is_superuser": false,
  "institution": { "id": 3, "acronym": "UNAM" },
  "institution_details": { ... },
  "is_ies": true,
  "is_reviewer": false
}
```

**Errores posibles:**

| Status | Causa |
|--------|-------|
| 400 | Token ya utilizado |
| 400 | `email` ya registrado en el sistema |
| 400 | Contraseñas no coinciden o < 8 caracteres |
| 404 | Token no existe |

---

### 5. Eliminar invitación

**Requiere:** token de administrador (`is_staff` o `is_superuser`).

```
DELETE /api/invitation/<uuid>/
Authorization: Token <auth_token>
```

**Respuesta 204** sin cuerpo.

---

## Flujos completos

### Flujo A — Invitación IES (con email)

```
Admin (reviewer)                    Sistema                  Contacto IES
     |                                 |                          |
     |-- POST /api/invitation/ ------->|                          |
     |   { institution: 3,             |                          |
     |     email: "..." }              |                          |
     |                                 |-- Envía correo --------->|
     |<-- 201 { destination_url } ------|                          |
     |                                 |       (correo recibido)  |
     |                                 |                          |
     |                     GET /register?token=<uuid>  <---------|
     |                                 |                          |
     |              GET /api/invitation/<uuid>/  <----------------|
     |                                 |-- 200 { institution... } |
     |                                 |                          |
     |           POST /api/invitation/<uuid>/register/  <---------|
     |                                 |   { first_name, ... }    |
     |                                 |-- 201 { token, user } -->|
     |                                 |        (auto-login)      |
```

### Flujo B — Invitación IES (sin email)

El admin crea el token sin `email`, copia `destination_url` de la respuesta
y la comparte manualmente (Slack, correo institucional, etc.). El resto del
flujo es igual desde el paso GET del frontend.

### Flujo C — Invitación genérica (reviewer/staff)

Igual que Flujo A pero con `reviewer: true` en el body y sin `institution`.
El usuario registrado adquiere los permisos del token.

---

## Notas de implementación

- **Auto-login**: el endpoint `register` devuelve el mismo formato que
  `/api/login/`, incluyendo el `token` de autenticación. El frontend puede
  guardarlo directamente y redirigir al dashboard.
- **Token UUID**: el `key` es un UUID v4. Úsalo directamente en la URL.
- **`viewed_at`**: se establece solo en la primera llamada GET. Las
  siguientes no lo modifican (idempotente).
- **Correos**: el backend busca los `TemplateBase` por nombre en la base de
  datos. Si no existen, el token se crea igualmente pero sin correo. El
  administrador debe crear en `/admin/email_send/templatebase/`:
  - `email/invitation_institution.html`
  - `email/invitation_generic.html`