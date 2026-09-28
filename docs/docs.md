# Architecture & Implementation Plan

## Architecture

The application is planned as a **FastAPI REST service** backed by **PostgreSQL** and **Redis**, with Docker Compose managing the API, database, and Redis services.

### Core Data Model

* **Users** — `admin`, `provider`, and `customer` roles.
* **Bookings** — connects a customer with a provider, including service, time, and booking status.
* **Reviews** — linked to completed bookings, with rating and comments.

### RBAC

RBAC will be enforced at the API level:

* **Admin** — can access all bookings.
* **Provider** — can access only their own bookings.
* **Customer** — can access only their own bookings.

Resource ownership will be checked in addition to the user's role.

### Redis

Redis will be used as a queue for the review summarisation endpoint. The initial implementation will enqueue a summarisation job stub rather than making a real LLM call.

## Implementation Plan

1. Set up FastAPI, PostgreSQL, and database models.
2. Add booking CRUD endpoints.
3. Implement authentication and role/resource-level authorization.
4. Add reviews with completed-booking validation.
5. Add Redis-backed summarisation job.
6. Dockerize API, PostgreSQL, and Redis using Docker Compose.
7. Add tests for CRUD and RBAC behaviour.
8. Add GitHub Actions for linting and tests.
9. Complete setup documentation and end-to-end verification.

## Current Status

The assessment is currently incomplete. Due to an examination schedule overlapping with the assessment deadline, I was unable to complete and properly test the full implementation within the allocated time.

With the limited time available, I have submitted the **architecture, database design, API design, RBAC approach, Redis usage, and implementation plan** rather than submitting untested code that may not run reliably.

I will continue the implementation and aim to complete the remaining components by **end of day today**.

I sincerely request that my evaluation consider the architecture and work submitted now and, if possible, that the completed implementation be considered at the end of the evaluation process.
