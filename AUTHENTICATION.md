# DroxAI Authentication System

This document describes the user authentication system implemented for the DroxAI platform.

## ⚙️ Optional Authentication

**By default, authentication is DISABLED** for single-user deployments. The system works immediately without requiring login.

To enable authentication (for multi-user environments):
```bash
export REQUIRE_AUTH=true
export REACT_APP_REQUIRE_AUTH=true
```

## 👑 Admin Users

**Owners/admins get unlimited session time** - no time limits, no payment required!

Set admin users via environment variable:
```bash
export ADMIN_EMAILS="owner@example.com,admin@example.com"
```

**Admin privileges:**
- ✅ 1-year token expiration (effectively unlimited)
- ✅ No payment required
- ✅ Full platform access
- ✅ Can be used alongside regular paid users

## Features

### Backend (FastAPI)
- **Optional Authentication**: Can be enabled/disabled via `REQUIRE_AUTH` environment variable
- **Admin Support**: Designated admin users get extended tokens (1 year) and no payment requirements
- **JWT-based Authentication**: Secure token-based authentication with 30-minute expiration for regular users
- **Password Security**: Bcrypt hashing via passlib for secure password storage
- **RESTful API Endpoints**:
  - `POST /api/auth/register` - Register new user
  - `POST /api/auth/login` - Login and receive JWT token (admin users get 1-year tokens)
  - `GET /api/auth/me` - Get current authenticated user info (returns anonymous user if auth disabled)
- **Email Validation**: Proper email format validation using email-validator
- **Simple Storage**: JSON-based user storage for minimal infrastructure changes

### Frontend (React)
- **Optional UI**: Login/Register pages hidden when authentication is disabled
- **Login Page**: Clean, user-friendly login interface
- **Registration Page**: Secure registration with password confirmation
- **Authentication Context**: Global state management using React Context API
- **Protected Routes**: Automatic redirect to login for unauthenticated users (when auth enabled)
- **Dynamic Navigation**: Shows Login/Register or Bot Builder/Dashboard based on auth setting
- **Token Management**: Automatic storage and retrieval from localStorage
- **User Greeting**: Displays username in header when logged in

## Security Features

1. **Optional by Default**: Authentication disabled for single-user mode
2. **Admin Privileges**: Owner/admin users get unlimited session time (1-year tokens)
3. **Password Hashing**: All passwords are hashed using bcrypt before storage
4. **JWT Tokens**: Short-lived tokens (30 minutes) for regular users, extended for admins
5. **Protected Routes**: Dashboard and Bot Builder require authentication (when enabled)
6. **Environment Variables**: JWT secret key can be configured via environment
7. **Vulnerability-Free Dependencies**: All dependencies scanned and updated
8. **Data Protection**: User data files excluded from version control

## Setup Instructions

### Quick Start (No Authentication)

Just run the application - authentication is disabled by default:

```bash
cd backend && python main.py
cd frontend && npm start
```

Access all features immediately at `http://localhost:3000` without login.

### Backend Setup with Authentication

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Enable authentication (optional):
```bash
export REQUIRE_AUTH=true
export JWT_SECRET_KEY="your-secure-random-key-here"
export ENVIRONMENT="development"  # or "production"

# Set yourself as admin (unlimited session, no payment)
export ADMIN_EMAILS="your@email.com"
```

3. Start the backend server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Set environment variables (optional):
```bash
export REACT_APP_API_URL="http://localhost:8000"
```

3. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Register User
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "securepassword123"
}
```

Response:
```json
{
  "email": "user@example.com",
  "username": "username",
  "created_at": "2025-11-02T21:00:00+00:00"
}
```

### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get Current User
```bash
GET /api/auth/me
Authorization: Bearer <access_token>
```

Response:
```json
{
  "email": "user@example.com",
  "username": "username",
  "created_at": "2025-11-02T21:00:00+00:00"
}
```

## Usage Flow

1. **Registration**: New users visit `/register` and create an account
2. **Login**: Users visit `/login` and authenticate with email/password
3. **Token Storage**: JWT token is stored in localStorage after successful login
4. **Automatic Authentication**: On page load, the app checks for stored token and validates it
5. **Protected Access**: Users can now access protected routes like `/dashboard` and `/builder`
6. **Logout**: Users can logout, which clears the token and redirects to home

## Production Deployment

For production deployment:

1. **Set JWT Secret**: Always set a secure random `JWT_SECRET_KEY` environment variable
2. **Set Environment**: Set `ENVIRONMENT=production` to enforce secret key requirement
3. **Use HTTPS**: Ensure all API communication uses HTTPS
4. **Update CORS**: Configure CORS to only allow your production frontend URL
5. **Database**: Consider upgrading from JSON storage to a proper database (PostgreSQL, MongoDB, etc.)
6. **Token Expiration**: Adjust `ACCESS_TOKEN_EXPIRE_MINUTES` based on your security requirements

## Security Considerations

- Passwords are never stored in plain text
- JWT tokens have short expiration times
- All authentication endpoints use proper HTTP status codes
- Email validation prevents invalid email formats
- Password strength can be enforced (currently minimum 8 characters)
- Token validation happens on every protected route request
- User data is excluded from version control

## Future Enhancements

Consider implementing:
- Password reset functionality
- Email verification
- Multi-factor authentication (MFA)
- OAuth/Social login (Google, GitHub, etc.)
- Remember me functionality
- Session management dashboard
- Rate limiting on login attempts
- Account lockout after failed attempts
- Password strength meter
- User profile management
