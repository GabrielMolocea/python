# 🔐 JWT Auth App — Flask + React/TypeScript

A login application with **JWT tokens that expire in 60 seconds**.

## Project Structure

```
auth-app/
├── backend/
│   ├── app.py           # Flask server
│   └── requirements.txt
└── frontend/
    ├── src/
│   │   ├── App.tsx      # All React components
│   │   ├── App.css      # Styles
│   │   ├── api.ts       # API service layer
│   │   └── index.tsx    # Entry point
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   └── tsconfig.json
```

## Setup & Run

### 1. Backend (Flask)

```bash
cd backend
pip install -r requirements.txt
python app.py
# Runs on http://localhost:5000
```

### 2. Frontend (React + TypeScript)

```bash
cd frontend
npm install
npm start
# Runs on http://localhost:3000
```

## API Endpoints

| Method | Path             | Auth      | Description                         |
| ------ | ---------------- | --------- | ----------------------------------- |
| POST   | `/api/login`     | ❌        | Login, returns JWT                  |
| GET    | `/api/verify`    | ✅ Bearer | Check token validity + seconds left |
| GET    | `/api/protected` | ✅ Bearer | Example protected route             |

## Token Details

- **Algorithm**: HS256
- **Expiry**: 60 seconds (`TOKEN_EXPIRY_SECONDS` in `app.py`)
- **Format**: `Authorization: Bearer <token>`

## Test Credentials

| Username | Password    |
| -------- | ----------- |
| alice    | password123 |
| bob      | hunter2     |

## Customization

- Change expiry: edit `TOKEN_EXPIRY_SECONDS` in `backend/app.py`
- Change secret key: edit `SECRET_KEY` in `backend/app.py` (use env var in production!)
- Add users: add to the `USERS` dict with `hashlib.sha256(password.encode()).hexdigest()`
