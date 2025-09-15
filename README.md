# PROSCRUM

A Golf Handicap Calculator by Students of the Provadis School of International Management and Technologies

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Project Structure](#project-structure)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Usage](#usage)
- [Testing](#testing)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

---

## About

PROSCRUM is a web application designed to help golfers calculate and track their handicaps. The project consists of a Python-based backend (API) and a modern TypeScript/Vue.js frontend, providing a seamless user experience for managing golf rounds, courses, and user authentication in English and German.
Additionally Admins can manage users, courses rounds and more. 

---

## Features

- User authentication and authorization
- Add, edit, and view golf courses
- Record and manage golf rounds
- Calculate golf handicaps
- Data visualization of rounds and statistics
- Responsive and modern UI
- Internationalization (i18n) support

---

## Project Structure

```
PROSCRUM/
│
├── PROSCRUM-BACKEND/      # FastAPI backend (Python)
│   ├── app/
│   │   ├── routers/       # API route definitions
│   │   ├── models.py      # Database models
│   │   ├── calculations.py, new_calculations.py, old_calculation.py
│   │   ├── ...            # Other backend modules
│   ├── requirements.txt   # Python dependencies
│   └── README.md
│
├── PROSCRUM-FRONTEND/     # Vue.js frontend (TypeScript)
│   ├── src/
│   │   ├── components/    # Vue components
│   │   ├── pages/         # Page components
│   │   ├── composables/   # Composable utilities
│   │   ├── i18n/          # Localization files
│   │   ├── assets/        # Images, icons, sounds
│   │   └── ...            # Other frontend modules
│   ├── public/
│   ├── package.json       # Frontend dependencies
│   └── README.md
│
├── README.md              # Project overview (this file)
└── package.json           # (optional) Monorepo dependencies
```

---

## Backend Setup

1. **Navigate to the backend directory:**
    ```powershell
    cd PROSCRUM-BACKEND
    ```

2. **Create a virtual environment (optional but recommended):**
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```powershell
    pip install -r requirements.txt
    ```

4. **Run the FastAPI server:**
    ```powershell
    uvicorn app.main:app --reload
    ```

    The API will be available at `http://127.0.0.1:8000`.

---

## Frontend Setup
See PROSCRUM/blob/main/PROSCRUM-FRONTEND/README.md

---

## Usage

- Open PROSCRUMs "Golf Handicap Calculator" in your browser at https://164.30.73.144/.
- Register or log in.
- Add golf courses and record your rounds.
- View your handicap and statistics.

---

## Testing

### Backend

- Tests are located in `PROSCRUM-BACKEND/app/test/`.
- Run tests with your preferred Python test runner (e.g., pytest).

### Frontend

- Frontend tests are located in `PROSCRUM-FRONTEND/src/components/__tests__/` and `src/pages/__tests__/`.
- Run tests with:
  ```powershell
  npm run test
  ```

---

## Technologies Used

- **Backend:** Python, FastAPI, SQLAlchemy
- **Frontend:** Vue.js 3, TypeScript, Vite, Pinia, Vue Router
- **Other:** ESLint, Vitest, i18n, CSS

---

### Team
Frontend Development:
    - [Jakob Fischer](https://github.com/JakobFischer2574)

Backend Development:
    - [Jan Brandenstein](https://github.com/JanBrandenstein)
    - [Martin](https://github.com/Moartin-Dev)
    - [Robin](https://github.com/notsambutrobin)
    - [Samuel Gerules](https://github.com/Sannynator)

Server Hosting:
    - [Jan Brandenstein](https://github.com/JanBrandenstein)

Team Lead:
    - [Santino](https://github.com/Sanny64)

## Lizenz
This project is for educational purposes by students of the Provadis School of International Management and Technologies.
License managed by [Jakob Fischer](https://github.com/JakobFischer2574)