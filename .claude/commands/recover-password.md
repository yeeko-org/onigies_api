# Skill: recover-password

Documentación para que el **frontend** consuma el flujo de
recuperación de contraseña de la API ONIGIES.

---

## Flujo completo (3 pasos)

```
[1] Usuario ingresa su email
        ↓
POST /api/password-recovery/
        ↓
[2] Usuario recibe correo, hace clic en enlace
    Frontend extrae ?token=<uuid> de la URL
        ↓
GET /api/password-recovery/<uuid>/
        ↓
[3] Usuario ingresa nueva contraseña
        ↓
POST /api/password-recovery/<uuid>/confirm/
        ↓
Respuesta = datos de sesión (auto-login, igual que /login/)
```

---

## Paso 1 — Solicitar recuperación

**Endpoint:** `POST /api/password-recovery/`
**Auth:** No requerida

### Request body
```json
{ "email": "usuario@ejemplo.edu.mx" }
```

### Response (siempre 200, incluso si el email no existe)
```json
{
  "detail": "Si el correo existe, recibirás un enlace de recuperación en breve."
}
```

### Errores posibles
| Status | Causa |
|--------|-------|
| 400 | Body vacío (sin campo `email`) |

### Notas frontend
- Mostrar siempre el mensaje genérico de éxito, **nunca indicar**
  si el correo existe o no (anti-enumeración).
- Deshabilitar el botón después del envío para evitar spam.
- El correo contiene el enlace:
  `{FRONTEND_SITE_URL}/recover-password?token=<uuid>`

---

## Paso 2 — Validar token (opcional pero recomendado)

Antes de mostrar el formulario de nueva contraseña, verifica
que el token siga siendo válido.

**Endpoint:** `GET /api/password-recovery/<uuid>/`
**Auth:** No requerida

### Response 200 (token válido)
```json
{
  "email": "usuario@ejemplo.edu.mx",
  "full_name": "Ana García López",
  "valid": true
}
```

### Response 400 (token inválido / expirado / ya usado)
```json
{
  "detail": "El token ha expirado o ya fue utilizado."
}
```

### Response 404 (UUID no existe)
```json
{ "detail": "Token inválido." }
```

### Flujo frontend recomendado
```
Al cargar la página /recover-password:
  1. Extraer token de query params
  2. GET /api/password-recovery/{token}/
  3a. Si 200 → mostrar formulario, pre-llenar email si quieres
  3b. Si 400 o 404 → mostrar "enlace inválido o expirado"
      + botón para solicitar uno nuevo
```

---

## Paso 3 — Confirmar nueva contraseña

**Endpoint:** `POST /api/password-recovery/<uuid>/confirm/`
**Auth:** No requerida

### Request body
```json
{
  "password": "nueva_contraseña_segura",
  "password_confirm": "nueva_contraseña_segura"
}
```

### Response 200 — contraseña cambiada + sesión iniciada
Mismo formato que `POST /api/login/`. El frontend debe guardar
el token de auth igual que en el login normal.

```json
{
  "id": 42,
  "email": "usuario@ejemplo.edu.mx",
  "username": "ana.garcia",
  "first_name": "Ana",
  "last_name": "García López",
  "token": "9a8b7c6d5e4f...",
  "fullname": "Ana García López",
  "reviewer": false,
  "is_staff": false,
  "is_superuser": false,
  "institution": { "id": 1, "acronym": "UNAM", ... },
  "institution_details": { ... },
  "is_ies": true,
  "is_reviewer": false
}
```

### Response 400 — errores de validación
```json
{
  "errors": {
    "password": "La contraseña debe tener al menos 8 caracteres.",
    "password_confirm": "Las contraseñas no coinciden."
  }
}
```

### Errores posibles
| Status | Causa |
|--------|-------|
| 400 | Token expirado o ya usado |
| 400 | Contraseña muy corta (< 8 chars) |
| 400 | Contraseñas no coinciden |
| 400 | Body vacío |
| 404 | UUID no encontrado |

---

## Manejo de sesión post-confirmación

```javascript
// Ejemplo simplificado (adaptar al store del proyecto)
const resp = await api.post(
  `/password-recovery/${token}/confirm/`,
  { password, password_confirm }
)
if (resp.status === 200) {
  // Guardar token exactamente igual que tras el login
  store.setAuthToken(resp.data.token)
  store.setUser(resp.data)
  router.push('/dashboard')
}
```

---

## Consideraciones de seguridad

| Aspecto | Detalle |
|---------|---------|
| Expiración | Token válido 24 h desde su creación |
| Uso único | El token se invalida al confirmar; no se puede reusar |
| Tokens anteriores | Al solicitar un nuevo enlace, los tokens previos se invalidan |
| Anti-enumeración | El paso 1 siempre devuelve 200 |
| Auth token | El auth token del usuario NO cambia; solo la contraseña |

---

## Endpoints resumen

| Método | URL | Descripción |
|--------|-----|-------------|
| POST | `/api/password-recovery/` | Solicitar correo de recuperación |
| GET | `/api/password-recovery/{uuid}/` | Validar token |
| POST | `/api/password-recovery/{uuid}/confirm/` | Confirmar nueva contraseña |