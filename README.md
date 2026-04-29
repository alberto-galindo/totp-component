# 🔐 TOTP Component — QR Generation & Code Validation

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat&logo=flask&logoColor=white)
![RFC 6238](https://img.shields.io/badge/RFC-6238%20TOTP-blue?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

A lightweight web application that generates a **QR code** to register a TOTP service in Google Authenticator (or any RFC 6238-compatible app) and **validates** the 6-digit codes in real time.

---

## 📋 Table of Contents

- [Overview](#overview)
- [How TOTP Works](#how-totp-works)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Security Considerations](#security-considerations)
- [References](#references)

---

## Overview

This component was built as part of a Master's degree in Cybersecurity assignment. It covers two core requirements:

1. **QR Code generation** — creates an `otpauth://` provisioning URI and renders it as a scannable QR image embeddable in any HTML page.
2. **TOTP validation** — verifies the 6-digit code entered by the user against the shared secret stored in the server session, with a ±30 s clock-drift tolerance.

The frontend includes a **live countdown timer** showing how many seconds remain before the current code expires.

---

## How TOTP Works

TOTP (**Time-based One-Time Password**, RFC 6238) is built on top of HOTP (RFC 4226).  
The algorithm computes:

```
TOTP(K, T) = HOTP(K, T)  where  T = floor(Unix_time / 30)
HOTP(K, C) = Truncate( HMAC-SHA1(K, C) )  mod 10^6
```

| Parameter | Value |
|-----------|-------|
| Algorithm | HMAC-SHA1 |
| Digits    | 6 |
| Period    | 30 seconds |
| Secret    | 160-bit random Base32 string |

The same secret is shared between the server and the authenticator app (via QR scan), so both can independently compute the same code at any given time window.

---

## Project Structure

```
totp_component/
├── app.py                  # Flask server — TOTP logic & API routes
├── requirements.txt        # Python dependencies
└── templates/
    └── index.html          # Web UI — QR display + validation form
```

---

## Tech Stack

| Layer        | Library / Tool                  | Purpose                              |
|--------------|---------------------------------|--------------------------------------|
| Backend      | [Flask 3.x](https://flask.palletsprojects.com) | HTTP server & session management |
| TOTP         | [pyotp 2.9](https://github.com/pyauth/pyotp)   | RFC 6238 / RFC 4226 implementation |
| QR Code      | [qrcode + Pillow](https://github.com/lincolnloop/python-qrcode) | PNG image generation |
| Frontend     | HTML5 / CSS3 / Vanilla JS       | No external dependencies             |

---

## Getting Started

### Prerequisites

- Python **3.10+**
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/<your-repo>.git
cd totp_component

# Install dependencies
pip install -r requirements.txt
```

### Run

```bash
python app.py
```

Open your browser at **http://127.0.0.1:5000**

### Usage

1. Open the web app — a QR code is automatically generated.
2. Open **Google Authenticator** on your phone.
3. Tap **+** → *Scan a QR code* and point the camera at the QR.
4. The service **TareaSeguridad** will appear in the app with a rolling 6-digit code.
5. Enter the code in the validation field and click **Verify** — you'll get instant feedback.
6. Use the **Regenerate secret** button to create a new QR (re-scan required).

---

## API Endpoints

| Method | Route         | Description                                              |
|--------|---------------|----------------------------------------------------------|
| `GET`  | `/`           | Renders the main page with QR code and validation form   |
| `POST` | `/validate`   | Validates a TOTP code — returns `{valid: bool, message}` |
| `POST` | `/regenerate` | Generates a new secret and reloads the page              |

### Example response from `/validate`

```json
// Correct code
{ "valid": true,  "message": "✅ Código CORRECTO. Autenticación exitosa." }

// Wrong / expired code
{ "valid": false, "message": "❌ Código INCORRECTO o expirado." }
```

---

## Security Considerations

> ⚠️ This project is a **proof-of-concept**. For production use, apply the following hardening measures:

- **Secret storage** — persist the TOTP secret in a database with encryption at rest (AES-256); never store it in plain text.
- **Session key** — replace the demo `secret_key` with a cryptographically strong value:
  ```python
  import secrets
  app.secret_key = secrets.token_hex(32)
  ```
- **Rate limiting** — add brute-force protection to `/validate` (e.g. [Flask-Limiter](https://flask-limiter.readthedocs.io/)).
- **HTTPS** — mandatory in production to protect the signed session cookie.
- **Clock drift** — `valid_window=1` allows ±30 s tolerance; increasing it weakens security.
- **Secret exposure** — in production, do not display the raw Base32 secret on the UI.

---

## References

- [RFC 6238](https://datatracker.ietf.org/doc/html/rfc6238) — TOTP: Time-Based One-Time Password Algorithm  
- [RFC 4226](https://datatracker.ietf.org/doc/html/rfc4226) — HOTP: An HMAC-Based One-Time Password Algorithm  
- [pyotp](https://github.com/pyauth/pyotp) — Python One-Time Password Library  
- [qrcode](https://github.com/lincolnloop/python-qrcode) — QR Code image generator  
- [Flask](https://flask.palletsprojects.com) — The Pallets Project  
- [Google Authenticator — Android](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2)  
- [Google Authenticator — iOS](https://itunes.apple.com/es/app/google-authenticator/id388497605)  

---

<p align="center">
  Made with 🐍 Python &nbsp;|&nbsp; Master en Ciberseguridad
</p>
