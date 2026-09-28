# Architecture & Implementation Plan

## Architecture

The application is designed as a **FastAPI REST service** backed by **PostgreSQL** and **Redis**, with Docker Compose planned for managing the API, database, and Redis services.

### Core Data Model

* **Users** — `admin`, `provider`, and `customer` roles.
* **Services** — provider-created services with duration and pricing.
* **Availability Slots** — time slots associated with services.
* **Bookings** — connects a customer with a service/availability slot and booking status.
* **Reviews** — linked to completed bookings, with rating and comments.

### RBAC

RBAC is enforced at the API level:

* **Admin** — can access all resources.
* **Provider** — can manage their own services and access resources belonging to them.
* **Customer** — can access their own bookings and customer-specific resources.

Resource ownership is checked in addition to the user's role.

### Redis

Redis will be used as a queue for the review summarisation endpoint. The implementation will enqueue a summarisation job rather than making a real LLM call.

## Implementation Plan

1. Set up FastAPI, PostgreSQL, database models, and migrations. ✅
2. Implement authentication with password hashing and JWT. ✅
3. Implement RBAC and resource ownership authorization. ✅
4. Implement Service APIs with provider ownership. ✅
5. Implement Availability Slot APIs.
6. Implement Booking APIs with conflict/concurrency protection.
7. Implement Reviews and completed-booking validation.
8. Add Redis-backed review summarisation job.
9. Add tests, Docker Compose, and GitHub Actions.
10. Complete documentation and end-to-end verification.

## Current Status

The core foundation is now implemented, including:

* FastAPI application setup
* PostgreSQL database and migrations
* User and core database models
* JWT authentication and password hashing
* RBAC and resource ownership
* Service CRUD APIs

### Remaining Work

* Availability slot APIs
* Booking flow and double-booking protection
* Reviews
* Redis queue/worker
* Tests
* Docker and CI
* Final documentation and end-to-end verification

The implementation will continue toward completing and verifying the full assessment.
