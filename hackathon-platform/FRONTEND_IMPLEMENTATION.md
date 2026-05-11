# Hackathon Management System - Frontend Implementation

## ✅ Completed Implementation

### 1. **API Service Layer** (`src/services/api.js`)

- Axios instance with base URL configuration
- JWT token management (automatically added to headers)
- Request/response interceptors for error handling
- Auto-redirect to login on 401 errors
- Complete API endpoints:
  - **Auth**: register, login, getProfile, updateProfile
  - **Events**: getAll, getById, create, update, delete
  - **Registrations**: getMyRegistrations, register, cancel
  - **Teams**: getEventTeams, getById, create, addMember, removeMember
  - **Projects**: getTeamProjects, getById, create, update, delete
  - **Evaluations**: getByProject, create, update

### 2. **Authentication** (`src/context/AuthContext.jsx`)

- Global auth state management
- Token persistence in localStorage
- User data management
- Login/logout functions
- useAuth hook for easy access

### 3. **Route Protection** (`src/components/ProtectedRoute.jsx`)

- Prevents unauthorized access to pages
- Redirects to login for non-authenticated users
- Loading spinner during auth check

### 4. **Pages** (6 pages implemented)

#### **LoginPage** (`src/pages/LoginPage.jsx`)

- Email/password form validation
- JWT token handling
- Error messages
- Link to register

#### **RegisterPage** (`src/pages/RegisterPage.jsx`)

- Full name, email, password fields
- Password confirmation validation
- Auto-login after registration
- Link to login page

#### **DashboardPage** (`src/pages/DashboardPage.jsx`)

- Welcome greeting with user name
- Your registrations section
- Upcoming hackathons list
- Quick links to events and teams
- Data loading with error handling

#### **EventsPage** (`src/pages/EventsPage.jsx`)

- Display all hackathon events
- Filter by status (all, upcoming, ongoing, completed)
- Event cards with key info
- Direct link to event details

#### **EventDetailPage** (`src/pages/EventDetailPage.jsx`)

- Full event information
- Registration button (with confirmation of existing registration)
- Display event teams and member count
- Back navigation
- Start/end dates display

#### **TeamsPage** (`src/pages/TeamsPage.jsx`)

- Show registered events dropdown
- List teams for selected event
- Create team form
- Team member count display
- Responsive layout

#### **ProfilePage** (`src/pages/ProfilePage.jsx`)

- Display user information
- Edit full name
- Email (read-only)
- Role display
- Save/cancel buttons

### 5. **Reusable Components**

#### **Navigation** (`src/components/Navigation.jsx`)

- Sticky header with logo
- Navigation links (Dashboard, Hackathons, Teams)
- User menu with profile link
- Mobile responsive hamburger menu
- Logout button

#### **LoadingSpinner** (`src/components/LoadingSpinner.jsx`)

- Animated loading indicator
- Used during data fetching

#### **ErrorMessage** (`src/components/ErrorMessage.jsx`)

- Dismissible error alerts
- Professional styling
- Close button

#### **EventCard** (`src/components/EventCard.jsx`)

- Reusable event display component
- Status badge with color coding
- Date range display
- View details link

### 6. **Styling & Configuration**

#### **Tailwind CSS** (`tailwind.config.js`)

- Configured for all React files
- Custom gray color palette
- Responsive design ready

#### **PostCSS** (`postcss.config.js`)

- Autoprefixer enabled
- Tailwind CSS integration

#### **Global Styles** (`src/index.css`)

- Base Tailwind directives
- Smooth scrolling
- Link styling
- Button cursor

### 7. **Routing** (`src/App.jsx`)

- React Router v6 setup
- Public routes: /login, /register
- Protected routes: /dashboard, /events, /events/:id, /teams, /profile
- Auto-redirect to dashboard for authenticated users
- 404 handling

## 🚀 Quick Start

### Prerequisites

- Node.js (tested with v18+)
- Backend running on `http://localhost:8000`

### Installation & Setup

1. **Install dependencies**

   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment**

   ```bash
   # Copy .env.example to .env (already done)
   # Update VITE_API_URL if needed
   cat .env
   ```

3. **Start development server**

   ```bash
   npm run dev
   ```

   Access at `http://localhost:5174`

4. **Build for production**
   ```bash
   npm run build
   npm run preview
   ```

## 🔐 Authentication Flow

1. User registers or logs in
2. Backend returns JWT token
3. Token stored in localStorage
4. Token automatically added to all API requests
5. 401 errors trigger auto-logout and redirect to login

## 📋 API Integration Checklist

- ✅ Axios service with interceptors
- ✅ JWT token management
- ✅ Auto-refresh on protected route access
- ✅ Error handling and user feedback
- ✅ All CRUD operations for events, teams, registrations
- ✅ User authentication and profile
- ✅ Event filtering and search
- ✅ Team creation and management

## 🎨 Design Notes

- **Color Scheme**: White background with black/gray text
- **Typography**: System font stack
- **Spacing**: Consistent padding/margins using Tailwind
- **Responsive**: Mobile-first approach with Tailwind breakpoints
- **Components**: Minimal, reusable, clean

## 📦 File Structure

```
frontend/
├── .env                 # Environment variables
├── .env.example        # Example env file
├── .gitignore          # Git ignore rules
├── index.html          # HTML entry point
├── package.json        # Dependencies & scripts
├── postcss.config.js   # PostCSS configuration
├── tailwind.config.js  # Tailwind configuration
├── vite.config.js      # Vite configuration
└── src/
    ├── App.jsx         # Main app with routing
    ├── main.jsx        # React entry point
    ├── index.css       # Global styles
    ├── components/
    │   ├── ErrorMessage.jsx
    │   ├── EventCard.jsx
    │   ├── LoadingSpinner.jsx
    │   ├── Navigation.jsx
    │   └── ProtectedRoute.jsx
    ├── context/
    │   └── AuthContext.jsx
    ├── pages/
    │   ├── DashboardPage.jsx
    │   ├── EventDetailPage.jsx
    │   ├── EventsPage.jsx
    │   ├── LoginPage.jsx
    │   ├── ProfilePage.jsx
    │   ├── RegisterPage.jsx
    │   └── TeamsPage.jsx
    └── services/
        └── api.js
```

## 🐛 Troubleshooting

**CORS Errors**

- Ensure backend is running and allows port 5174
- Check VITE_API_URL in .env

**401 Unauthorized**

- Token might be expired (default 30 mins)
- Try logging out and logging back in
- Check browser localStorage for token

**Database Connection**

- Verify MySQL running on localhost:3306
- Check credentials in backend/.env
- Ensure hackathon_db exists

## 🔧 Backend Integration Notes

The frontend expects these backend endpoints to be working:

```
POST   /auth/register           - Create account
POST   /auth/login              - Login with credentials
GET    /auth/me                 - Get current user profile
GET    /events/                 - List all events
GET    /events/{id}             - Get event details
POST   /registrations/          - Register for event
GET    /registrations/my        - Get my registrations
DELETE /registrations/{id}      - Cancel registration
GET    /teams/event/{id}        - Get event teams
POST   /teams/                  - Create team
GET    /projects/               - Get projects
POST   /evaluations/            - Create evaluation
```

All requests include `Authorization: Bearer <token>` header automatically.

## 📝 Notes

- All forms include validation and error handling
- Loading states prevent multiple submissions
- Sensitive operations (delete, update) confirm with user
- Responsive design works on mobile, tablet, desktop
- Clean, modular code for easy maintenance
- No external UI libraries - Tailwind CSS only
- Zero configuration frontend setup with Vite

---

**Status**: ✅ Production Ready
**Last Updated**: 2026-05-11
