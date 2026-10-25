# PSUSphere

A Django web application for managing student organizations at Palawan State
University (PSU). Provides admin interface for managing colleges, programs,
organizations, students, and organization memberships.

## Features

- College management
- Program management
- Student organization management
- Student enrollment tracking
- Organization membership tracking
- REST API for managing colleges, programs, and students using Django REST Framework

## REST API

PSUSphere provides REST API endpoints for managing **colleges**, **programs**,
and **students** using Django REST Framework. Each resource supports list,
create, retrieve, update, partial update, and delete operations through the
routes below.

### Base URL and deployment status

Use the following base URL for local development:

```text
http://127.0.0.1:8000
```

A public PythonAnywhere URL for the REST API has not been confirmed in this
repository, so it is intentionally omitted. Replace the local base URL only
after a public deployment has been verified. This README does not claim that
the REST API is already deployed.

### Authentication

All API views require token authentication and an authenticated user. Send the
token in the `Authorization` header:

```http
Authorization: Token YOUR_TOKEN
```

`YOUR_TOKEN` is a placeholder. Replace it with a valid token for an existing
Django user. A missing or invalid token is rejected.

An administrator can create a token locally using DRF's management command:

```powershell
python manage.py drf_create_token <username>
```

Run the command from `projectsite` with the project environment active. The
command prints the token in the local terminal. Treat it as a credential: do
not commit it, paste it into source code, or include it in screenshots or logs.
There is no token-generation API endpoint.

Example authenticated request:

```powershell
curl -H "Authorization: Token YOUR_TOKEN" http://127.0.0.1:8000/api/colleges/
```

### Endpoint reference

The `<id>` segment is the record's database primary key. Use the trailing slash
shown in each route.

| Resource | List / Create | Retrieve / Update / Delete |
|---|---|---|
| Colleges | `GET /api/colleges/` — list<br>`POST /api/colleges/` — create | `GET /api/colleges/<id>/` — retrieve<br>`PUT` / `PATCH` — update<br>`DELETE` — delete |
| Programs | `GET /api/programs/` — list<br>`POST /api/programs/` — create | `GET /api/programs/<id>/` — retrieve<br>`PUT` / `PATCH` — update<br>`DELETE` — delete |
| Students | `GET /api/students/` — list<br>`POST /api/students/` — create | `GET /api/students/<id>/` — retrieve<br>`PUT` / `PATCH` — update<br>`DELETE` — delete |

`PUT`, `PATCH`, and `DELETE` use the same detail route shown for each resource.

Collection endpoints return arrays. Detail endpoints return single objects.
Successful list, retrieve, and update requests return `200 OK`; successful
creation returns `201 Created`; successful deletion returns `204 No Content`.

### College fields

The College serializer exposes all model fields:

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | integer | Read-only | Primary key |
| `college_name` | string | Yes | Maximum 150 characters |
| `created_at` | datetime | Read-only | Set automatically on creation |
| `updated_at` | datetime | Read-only | Updated automatically |

Example list response for `GET /api/colleges/`:

```json
[
  {
    "id": 1,
    "created_at": "2026-10-25T12:00:00Z",
    "updated_at": "2026-10-25T12:00:00Z",
    "college_name": "College of Sciences"
  }
]
```

Example create request for `POST /api/colleges/`:

```json
{
  "college_name": "College of Engineering"
}
```

Example `201 Created` response:

```json
{
  "id": 2,
  "created_at": "2026-10-25T12:05:00Z",
  "updated_at": "2026-10-25T12:05:00Z",
  "college_name": "College of Engineering"
}
```

### Program fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | integer | Read-only | Primary key |
| `prog_name` | string | Yes | Maximum 150 characters |
| `college` | integer | Yes | Primary key of an existing College |
| `students` | array | Read-only | Nested Student objects in the program |

The nested `students` field is returned when reading a Program. It is read-only;
create or update a Student through `/api/students/` rather than writing nested
students through the Program endpoint.

Example detail response for `GET /api/programs/<id>/`:

```json
{
  "id": 1,
  "prog_name": "BS Computer Science",
  "college": 1,
  "students": [
    {
      "id": 1,
      "student_id": "2026-0001",
      "lastname": "Dela Cruz",
      "firstname": "Juan",
      "middlename": "Santos",
      "program": 1,
      "program_name": "BS Computer Science"
    }
  ]
}
```

Example create request for `POST /api/programs/`:

```json
{
  "prog_name": "BS Information Technology",
  "college": 1
}
```

A newly created Program without students returns an empty `students` array.

### Student fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | integer | Read-only | Primary key |
| `student_id` | string | Yes | Maximum 15 characters |
| `lastname` | string | Yes | Maximum 25 characters |
| `firstname` | string | Yes | Maximum 25 characters |
| `middlename` | string or null | No | Maximum 25 characters |
| `program` | integer | Yes | Primary key of an existing Program |
| `program_name` | string | Read-only | Derived from the related Program |

Example detail response for `GET /api/students/<id>/`:

```json
{
  "id": 1,
  "student_id": "2026-0001",
  "lastname": "Dela Cruz",
  "firstname": "Juan",
  "middlename": "Santos",
  "program": 1,
  "program_name": "BS Computer Science"
}
```

Example create request for `POST /api/students/`:

```json
{
  "student_id": "2026-0002",
  "lastname": "Santos",
  "firstname": "Maria",
  "middlename": "Lopez",
  "program": 1
}
```

The `201 Created` response also includes the read-only `id` and `program_name`
fields.

For updates, `PUT` requires all required write fields, while `PATCH` may send
only the fields being changed.

### Validation and errors

Manual testing confirmed the following behavior:

- `400 Bad Request` for invalid input.
- `401 Unauthorized` for missing or invalid tokens on the tested list endpoint.
- `404 Not Found` for nonexistent College, Program, and Student detail records.
- `student_id` is limited to 15 characters.
- The `college` field on a Program must reference an existing College.
- The `program` field on a Student must reference an existing Program.
- `prog_name` is required when creating or fully updating a Program.

These checks are not a complete security audit of every endpoint and HTTP
method.

### Manual testing summary

Manual tests against the local development server covered:

- List, retrieve, create, update, and delete operations for Colleges, Programs,
  and Students.
- Valid, missing, and invalid token scenarios.
- Missing required fields and invalid foreign-key references.
- Student ID length validation.
- Nonexistent-record responses.
- Deletion of the temporary student test record after testing.

These were manual checks, separate from automated regression tests. The
repository also contains a small automated DRF API test module in
`projectsite/api/tests.py`, but it is not a complete regression or security
suite. A broader security review remains outstanding.

## Authors

**Erl Joseph Mangubat**

[![Email](https://img.shields.io/badge/Email-D14836?style=flat&logo=gmail&logoColor=white)](mailto:erljosephmangubat.phcs@gmail.com)
[![Facebook](https://img.shields.io/badge/Facebook-1877F2?style=flat&logo=facebook&logoColor=white)](https://www.facebook.com/share/1Lx4w2oZUL/)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=flat&logo=instagram&logoColor=white)](https://www.instagram.com/erljosephm)