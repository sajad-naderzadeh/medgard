# MedGuard AI

MedGuard AI is a research prototype for cardiovascular-risk decision support. It provides a FastAPI backend, patient-data storage, a trained cardiovascular model, and safety-oriented response primitives. It is **not** a diagnostic or treatment system.

## Run locally

```bash
cp .env.example .env
docker compose up --build
```

The API is available at `http://localhost:8000`; interactive documentation is at `/docs`.

## What is implemented

- JWT authentication and role-protected routes
- MongoDB-backed patient profiles and clinical records
- Cardiovascular-risk prediction with persisted prediction history
- Clinical alerts for severe hypertension and low oxygen saturation
- Local knowledge, retrieval, safety, and explainability building blocks

## Verification

```bash
PYTHONPATH=backend:. pytest tests -q
```

## Safety and scope

The bundled model was trained on a small research dataset and has not undergone external clinical validation. Do not use it for diagnosis, triage, prescribing, or emergency decisions. Production deployment requires clinical validation, privacy/legal review, secret management, audit logging, monitoring, and appropriate regulatory review.
