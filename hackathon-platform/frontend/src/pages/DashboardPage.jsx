import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { eventsAPI, registrationsAPI } from '../services/api';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';
import { Navigation } from '../components/Navigation';

export const DashboardPage = () => {
  const { user } = useAuth();
  const [events, setEvents] = useState([]);
  const [registrations, setRegistrations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [eventsRes, regsRes] = await Promise.all([
        eventsAPI.getAll(),
        registrationsAPI.getMyRegistrations(),
      ]);
      setEvents(eventsRes.data || []);
      setRegistrations(regsRes.data || []);
    } catch (err) {
      setError('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <>
        <Navigation />
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <LoadingSpinner />
        </div>
      </>
    );
  }

  return (
    <>
      <Navigation />
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <ErrorMessage message={error} onClose={() => setError('')} />

          {/* Welcome Section */}
          <div className="mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">Welcome, {user?.full_name}!</h1>
            <p className="text-gray-600">Discover hackathons and connect with other developers.</p>
          </div>

          {/* Your Registrations */}
          {registrations.length > 0 && (
            <div className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Your Registrations</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {registrations.map((reg) => (
                  <div key={reg.registration_id} className="bg-white rounded-lg border border-gray-200 p-6">
                    <h3 className="font-semibold text-gray-900 mb-2">{reg.event_title}</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      Registered on {new Date(reg.registered_date).toLocaleDateString()}
                    </p>
                    <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${
                      reg.status === 'confirmed'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {reg.status}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Upcoming Events */}
          <div>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Upcoming Hackathons</h2>
              <Link to="/events" className="text-gray-900 font-medium hover:underline">
                View All →
              </Link>
            </div>
            
            {events.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {events.slice(0, 3).map((event) => (
                  <div key={event.event_id} className="bg-white rounded-lg border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow">
                    <div className="p-6">
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">{event.title}</h3>
                      <p className="text-gray-600 text-sm mb-4 line-clamp-2">{event.description}</p>
                      <div className="flex items-center text-sm text-gray-500 mb-4">
                        <svg className="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        {new Date(event.start_date).toLocaleDateString()}
                      </div>
                      <Link
                        to={`/events/${event.event_id}`}
                        className="inline-block w-full bg-gray-900 text-white py-2 rounded-lg text-center text-sm font-medium hover:bg-gray-800 transition-colors"
                      >
                        Learn More
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="bg-white rounded-lg border border-gray-200 p-12 text-center">
                <p className="text-gray-600">No events available at the moment.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
};
