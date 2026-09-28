# Service Booking & Review Platform

A small backend service designed to model the core workflow of a service booking and review platform, where providers offer services/time slots, customers create bookings, and completed bookings can receive reviews.

> **Stack:** FastAPI · PostgreSQL · Redis · Docker · GitHub Actions

---

## 1. Overview

The goal of this assessment is to build a REST API with:

* Role-based users: `admin`, `provider`, and `customer`
* Service booking management
* Provider/customer access isolation
* Reviews for completed bookings
* Redis integration for caching or background-job queuing
* Dockerized API, PostgreSQL, and Redis services
* Automated linting and testing through GitHub Actions

The implementation is intentionally kept small so that the core architecture, access-control decisions, and data relationships remain easy to understand and defend.

---

## 2. Planned Architecture

```text
                         ┌─────────────────────┐
                         │      Client         │
                         │  Postman / Browser  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │                     │
                         │  REST API           │
                         │  RBAC               │
                         │  Validation         │
                         └──────┬───────┬──────┘
                                │       │
                    ┌───────────┘       └────────────┐
                    ▼                                ▼
          ┌─────────────────┐                ┌───────────────┐
          │   PostgreSQL    │                │     Redis     │
          │                 │                │               │
          │ Users           │                │ Cache / Queue │
          │ Bookings        │                │               │
          │ Reviews         │                └───────────────┘
          └─────────────────┘
                    ▲
                    │
          ┌─────────┴─────────┐
          │   Docker Compose  │
          │                   │
          │ API + DB + Redis  │
          └───────────────────┘
```

---

## 3. Data Model

### Users

Stores all platform users and their roles.

```text
User
├── id
├── name
├── email
├── password_hash
└── role
     ├── admin
     ├── provider
     └── customer
```

### Bookings

Represents a customer's booking with a provider.

```text
Booking
├── id
├── provider_id → Users
├── customer_id → Users
├── service_name
├── start_time
├── end_time
├── status
└── created_at
```

Possible booking statuses:

* `pending`
* `confirmed`
* `completed`
* `cancelled`

### Reviews

A review belongs to a completed booking.

```text
Review
├── id
├── booking_id → Booking
├── customer_id → Users
├── rating
├── comment
└── created_at
```

A booking should only be reviewable after it has been completed, and a booking should have at most one review.

---

## 4. API Design

### Bookings

```text
POST   /bookings
GET    /bookings
GET    /bookings/{booking_id}
PUT    /bookings/{booking_id}
DELETE /bookings/{booking_id}
```

The booking endpoints will enforce role-based access.

Expected access rules:

| Role     | Access                                         |
| -------- | ---------------------------------------------- |
| Admin    | Can access all bookings                        |
| Provider | Can access bookings belonging to that provider |
| Customer | Can access bookings belonging to that customer |

A provider must never be able to read another provider's bookings, and a customer must never be able to read another customer's bookings.

---

## 5. Review Summarisation

An endpoint will trigger a review summarisation job:

```text
POST /reviews/summarise
```

The endpoint will not make a real LLM call.

Instead, Redis will be used as the backing mechanism for a lightweight job/stub:

```text
Client
  │
  ▼
FastAPI
  │
  ▼
Redis Queue
  │
  ▼
Summarisation Worker / Stub
```

This keeps the architecture ready for replacing the stub with an actual AI summarisation service later.

---

## 6. Redis

Redis will be used for a real application purpose rather than only being included as an infrastructure dependency.

The planned use is the review summarisation queue.

Example:

```text
POST /reviews/summarise
        │
        ▼
   FastAPI API
        │
        ▼
 Redis list/queue
        │
        ▼
 Summarisation stub
```

This allows the API request to remain lightweight while the summarisation work is handled asynchronously.

---

## 7. RBAC Approach

Authorization will be handled after authentication by determining the current user's role and ownership of the requested resource.

The basic authorization flow is:

```text
Request
   │
   ▼
Authentication
   │
   ▼
Identify User + Role
   │
   ▼
Check Resource Ownership
   │
   ├── Admin ────────► Allow
   │
   ├── Provider ─────► Own provider bookings only
   │
   └── Customer ─────► Own customer bookings only
```

Role checks alone are not sufficient for providers and customers because they also need resource-level ownership checks.

---

## 8. Docker Setup

The application is intended to run using Docker Compose with three primary services:

```text
docker-compose
│
├── api
│   └── FastAPI application
│
├── postgres
│   └── Application database
│
└── redis
    └── Cache / job queue
```

Planned startup command:

```bash
docker compose up --build
```

The API will expose its REST endpoints and FastAPI documentation through:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

## 9. Testing & CI

The project is planned to include automated tests for:

* Booking creation
* Booking CRUD operations
* Role-based access control
* Provider ownership restrictions
* Customer ownership restrictions
* Review eligibility
* Redis/job enqueue behaviour

GitHub Actions will run the project's linting and tests automatically.

Planned workflow:

```text
Git Push
   │
   ▼
GitHub Actions
   │
   ├── Install dependencies
   ├── Run lint
   └── Run tests
```

---

## 10. Project Structure

The intended project structure is:

```text
.
├── app/
│   ├── main.py
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   ├── services/
│   ├── auth/
│   └── database/
│
├── tests/
│
├── docs/
│   ├── architecture.md
│   └── implementation-plan.md
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 11. Implementation Status

| Requirement                | Status      |
| -------------------------- | ----------- |
| PostgreSQL schema          | Planned     |
| Users and roles            | Planned     |
| Booking CRUD               | Planned     |
| Review model               | Planned     |
| RBAC                       | Planned     |
| Redis integration          | Planned     |
| Review summarisation job   | Planned     |
| Docker Compose             | Planned     |
| Automated tests            | Planned     |
| GitHub Actions             | Planned     |
| Setup documentation        | In progress |
| Architecture documentation | In progress |

The repository currently documents the proposed architecture and implementation approach. Remaining components are intended to be implemented incrementally, with each major feature committed separately.

---

## 12. Production Considerations

Before treating this as production-ready, the following areas would require additional work:

* Database migrations using a migration tool such as Alembic
* Secure secret management instead of committing credentials
* Proper authentication and token lifecycle management
* Password hashing and credential security
* Input validation and consistent API error handling
* Database connection pooling and transaction handling
* Redis failure/retry handling
* Background worker management
* Rate limiting
* Structured logging and monitoring
* Automated database backups
* HTTPS and secure deployment configuration
* More comprehensive integration and authorization tests

---

## 13. Development Approach

The implementation is being approached incrementally:

1. Define the database schema and relationships.
2. Configure FastAPI and PostgreSQL.
3. Implement booking CRUD endpoints.
4. Add authentication and RBAC.
5. Add review functionality and completion validation.
6. Integrate Redis for the summarisation job.
7. Dockerize the complete application.
8. Add automated tests.
9. Add GitHub Actions CI.
10. Finalize setup and architecture documentation.

The focus is on keeping each component small, testable, and explainable rather than introducing unnecessary complexity.
