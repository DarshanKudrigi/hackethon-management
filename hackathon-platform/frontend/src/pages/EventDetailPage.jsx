import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { eventsAPI, registrationsAPI, teamsAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';
import { Navigation } from '../components/Navigation';

export const EventDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [event, setEvent] = useState(null);
  const [teams, setTeams] = useState([]);
  const [isRegistered, setIsRegistered] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [registering, setRegistering] = useState(false);

  useEffect(() => {
    loadEventData();
  }, [id]);

  const loadEventData = async () => {
    try {
      setLoading(true);
      const [eventRes, teamsRes, regsRes] = await Promise.all([
        eventsAPI.getById(id),
        teamsAPI.getEventTeams(id),
        registrationsAPI.getMyRegistrations(),
      ]);

      setEvent(eventRes.data);
      setTeams(teamsRes.data || []);

      // Check if user is registered
      const userReg = regsRes.data?.find(reg => reg.event_id === parseInt(id));
      setIsRegistered(!!userReg);
    } catch (err) {
      setError('Failed to load event details');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async () => {
    try {
      setRegistering(true);
      await registrationsAPI.register(id);
      setIsRegistered(true);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to register');
    } finally {
      setRegistering(false);
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

  if (!event) {
    return (
      <>
        <Navigation />
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <p className="text-gray-600">Event not found</p>
        </div>
      </>
    );
  }

  const startDate = new Date(event.start_date).toLocaleDateString();
  const endDate = new Date(event.end_date).toLocaleDateString();

  return (
    <>
      <Navigation />
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <button
            onClick={() => navigate('/events')}
            className="mb-6 text-gray-600 hover:text-gray-900 flex items-center gap-2"
          >
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Events
          </button>

          <ErrorMessage message={error} onClose={() => setError('')} />

          <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
            <div className="flex justify-between items-start mb-4">
              <h1 className="text-4xl font-bold text-gray-900">{event.title}</h1>
              <span className={`px-4 py-2 rounded-lg text-sm font-medium ${
                event.status === 'upcoming' ? 'bg-blue-100 text-blue-800' :
                event.status === 'ongoing' ? 'bg-green-100 text-green-800' :
                'bg-gray-100 text-gray-800'
              }`}>
                {event.status}
              </span>
            </div>

            <p className="text-gray-600 text-lg mb-6">{event.description}</p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8 py-6 border-y border-gray-200">
              <div>
                <p className="text-sm text-gray-600 mb-1">Start Date</p>
                <p className="text-lg font-semibold text-gray-900">{startDate}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">End Date</p>
                <p className="text-lg font-semibold text-gray-900">{endDate}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Teams</p>
                <p className="text-lg font-semibold text-gray-900">{teams.length}</p>
              </div>
            </div>

            <div className="flex gap-4">
              {!isRegistered ? (
                <button
                  onClick={handleRegister}
                  disabled={registering}
                  className="px-6 py-3 bg-gray-900 text-white rounded-lg font-medium hover:bg-gray-800 transition-colors disabled:opacity-50"
                >
                  {registering ? 'Registering...' : 'Register for Event'}
                </button>
              ) : (
                <div className="px-6 py-3 bg-green-100 text-green-800 rounded-lg font-medium flex items-center gap-2">
                  <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  You're Registered
                </div>
              )}
            </div>
          </div>

          {/* Teams Section */}
          {teams.length > 0 && (
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Teams</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {teams.map((team) => (
                  <div key={team.team_id} className="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">{team.name}</h3>
                    <p className="text-gray-600 text-sm mb-4">{team.description || 'No description'}</p>
                    <div className="flex items-center text-sm text-gray-500">
                      <svg className="h-4 w-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM9 10a3 3 0 11-6 0 3 3 0 016 0zm0 0a3 3 0 110 6 3 3 0 010-6zm8-2a1 1 0 11-2 0 1 1 0 012 0zm-1 7a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                      {team.member_count || 0} members
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
};
