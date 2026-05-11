import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const Navigation = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!user) return null;

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center gap-8">
            <Link to="/dashboard" className="text-2xl font-bold text-gray-900">
              HackathonHub
            </Link>
            <div className="hidden md:flex gap-6">
              <Link to="/dashboard" className="text-gray-700 hover:text-gray-900 px-3 py-2 text-sm font-medium">
                Dashboard
              </Link>
              <Link to="/events" className="text-gray-700 hover:text-gray-900 px-3 py-2 text-sm font-medium">
                Hackathons
              </Link>
              <Link to="/teams" className="text-gray-700 hover:text-gray-900 px-3 py-2 text-sm font-medium">
                Teams
              </Link>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="hidden md:flex items-center gap-4">
              <Link to="/profile" className="text-gray-700 hover:text-gray-900">
                <span className="text-sm font-medium">{user.full_name}</span>
              </Link>
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg text-sm font-medium"
              >
                Logout
              </button>
            </div>

            {/* Mobile menu button */}
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="md:hidden p-2 rounded-lg hover:bg-gray-100"
            >
              <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        {isOpen && (
          <div className="md:hidden pb-4 space-y-2">
            <Link to="/dashboard" className="block px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
              Dashboard
            </Link>
            <Link to="/events" className="block px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
              Hackathons
            </Link>
            <Link to="/teams" className="block px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
              Teams
            </Link>
            <Link to="/profile" className="block px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
              Profile
            </Link>
            <button
              onClick={handleLogout}
              className="w-full text-left px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </nav>
  );
};
