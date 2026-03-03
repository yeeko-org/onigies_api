# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run dev server (default port 8018)
python manage.py runserver

# Run tests
pytest

# Run a single test file
pytest ies/tests.py
```

## Environment setup

```env
POSTRGRESQL_DB=True
DATABASE_NAME=onigies-local
FRONTEND_SITE_URL=https://localhost:3018
```

## Architecture

Django REST Framework API for managing the views, the serializers is the core of the validations and API contents. Settings live in `core/settings/__init__.py`; root URLs in `core/urls.py`; API endpoints registered in `api/urls.py`.

### Usage of Serializers for the ViewSets of models:
Use the file `api/mixins.py`, there are the next mixins:
MultiSerializerViewSet
MultiSerializerListRetrieveMix
MultiSerializerListRetrieveDeleteMix
MultiSerializerListRetrieveUpdateMix
MultiSerializerListCreateRetrieveUpdateMix
MultiSerializerCreateRetrieveMix
MultiSerializerListCreateRetrieveMix
ListMix
CreateMix
CreateRetrieveMix
ListCreateAPIView
MultiSerializerModelViewSet

### Apps and responsibilities

| App | Responsibility |
|-----|---------------|
| `ies` | User (custom AbstractUser), Institution, Period, StatusControl, InvitationToken, PasswordRecoveryToken |
| `indicator` | Axis → Component → Observable hierarchy; Sector, GeneralGroup |
| `question` | Question definitions by type (A, B, Reach, Plan, Special) with weights |
| `survey` | Survey per Institution-Period; AxisValue, ComponentValue, PopulationQuantity |
| `answer` | ObservableResponse, GroupResponse, attachments, comments |
| `example` | Good practices: GoodPracticePackage → GoodPractice → Feature → FeatureGoodPractice, Evidence |
| `ps_schema` | Schema/collection metadata for dynamic catalog and filter configuration |
| `email_send` | EmailProfile (SMTP config), TemplateBase (template path + profile FK), EmailRecord (log of sends). Service: send_template_email(template, email, context) and send_simple_email(email, subject, html). Templates in email_send/templates/email/. |


### Key base classes (api/views/common_views.py)

- `BaseViewSet` — extends `ModelViewSet` with `CustomPagination`, `UnaccentSearchFilter`, `DjangoFilterBackend`, `OrderingFilter`, and a custom delete confirmation mixin.
- `UnaccentSearchFilter` — uses `unaccent__icontains` lookup for accent-insensitive search (PostgreSQL only; falls back gracefully on SQLite).
- `AdvancedConditionalFieldsViewMixin` — excludes serializer fields based on `field_permissions` dict keyed by role (`anonymous`, `authenticated`, `staff`).


### Creating new Views

- **APIView vs ViewSet**: Use `views.APIView` for non-model or custom
  auth endpoints (login, recovery, etc.). Use `BaseViewSet` /
  `BaseGenericViewSet` (from `api/views/common_views.py`) for standard
  model CRUD.
- **Request validation**: Always validate `request.data` through a DRF
  serializer — never access it directly via `.get()`. Use
  `serializer.is_valid(raise_exception=True)` so DRF handles the 400
  response automatically.
- **Error response format**:
  - Field errors (auto via `raise_exception=True`): serializer errors
    dict returned directly → HTTP 400
  - Single non-field message: `{'detail': '...'}` → appropriate status
- **Serializer location**: Place serializers for a given sub-package in
  `api/views/{sub-package}/serializers.py`
  (e.g., auth views → `api/views/auth/serializers.py`).
- Import the serializers and common elements at the beginning of the file, and then define the views.


### Additional important notes
- When the developer ask you about the best approach or advices, after answer, ask if you can proceed with the implementation of the code, and wait for the confirmation before start writing the code.
- Build with typing hints and docstrings for all views, serializers, and complex functions.
- The API error messages should be in Spanish, as the user-facing frontend is in Spanish.
- Avoid boilerplate and repetition by leveraging DRF's generic views, mixins, and the `BaseViewSet` where possible. If the standard suggest that, answer before choose the best approach for the specific case.
- Never execute `makemigrations` or `migrate` commands yourself. I will to execute manually after review post session the changes.
- Limit code width to 80 columns. Wrap lines only if they exceed this limit, maintaining a single-line format whenever possible for readability.
