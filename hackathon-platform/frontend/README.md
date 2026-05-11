# Frontend Setup Guide

## Installation

```bash
npm install
```

## Development

```bash
npm run dev
```

The frontend will be available at `http://localhost:5174`

## Features Implemented

- **Authentication**: Login/Register with JWT tokens
- **Dashboard**: Overview of registered events and upcoming hackathons
- **Events**: Browse and filter hackathon events
- **Event Details**: View event information and teams
- **Team Management**: Create teams for registered events
- **Profile**: View and edit user profile
- **Protected Routes**: Secure pages that require authentication

## Environment Variables

Create a `.env` file in the frontend directory with:

```
VITE_API_URL=http://localhost:8000
```

## Project Structure

- `src/pages/`: Page components (Login, Dashboard, Events, etc.)
- `src/components/`: Reusable UI components
- `src/services/`: API service layer with Axios
- `src/context/`: Auth context for state management
- `src/hooks/`: Custom React hooks (if needed)

## Technology Stack

- React 19
- Vite
- Tailwind CSS
- Axios
- React Router v6

## Backend API Integration

The frontend connects to the FastAPI backend on `http://localhost:8000` with the following endpoints:

- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user profile
- `GET /events/` - Get all hackathon events
- `GET /events/{id}` - Get event details
- `GET /registrations/my` - Get user's registrations
- `POST /registrations/` - Register for an event
- `DELETE /registrations/{id}` - Cancel registration
- `GET /teams/event/{eventId}` - Get teams for an event
- `POST /teams/` - Create a new team
- `GET /projects/` - Get all projects
- `POST /evaluations/` - Submit project evaluation
