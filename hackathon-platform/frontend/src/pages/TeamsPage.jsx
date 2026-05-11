import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { teamsAPI, eventsAPI, registrationsAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';
import { Navigation } from '../components/Navigation';

export const TeamsPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [registrations, setRegistrations] = useState([]);
  const [selectedEventId, setSelectedEventId] = useState(null);
  const [teams, setTeams] = useState([]);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [teamName, setTeamName] = useState('');
  const [teamDesc, setTeamDesc] = useState('');
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      const [regsRes, eventsRes] = await Promise.all([
        registrationsAPI.getMyRegistrations(),
        eventsAPI.getAll(),
      ]);

      setRegistrations(regsRes.data || []);
      setEvents(eventsRes.data || []);

      // Auto-select first registered event
      if (regsRes.data && regsRes.data.length > 0) {
        setSelectedEventId(regsRes.data[0].event_id);
        loadTeamsForEvent(regsRes.data[0].event_id);
      }
    } catch (err) {
      setError('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const loadTeamsForEvent = async (eventId) => {
    try {
      const response = await teamsAPI.getEventTeams(eventId);
      setTeams(response.data || []);
    } catch (err) {
      setError('Failed to load teams');
    }
  };

  const handleEventChange = (eventId) => {
    setSelectedEventId(eventId);
    loadTeamsForEvent(eventId);
  };

  const handleCreateTeam = async (e) => {
    e.preventDefault();
    if (!selectedEventId) {
      setError('Please select an event');
      return;
    }

    try {
      setCreating(true);
      await teamsAPI.create({
        name: teamName,
        event_id: selectedEventId,
        description: teamDesc,
      });
      setTeamName('');
      setTeamDesc('');
      setShowCreateForm(false);
      loadTeamsForEvent(selectedEventId);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create team');
    } finally {
      setCreating(false);
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

  if (registrations.length === 0) {
    return (
      <>
        <Navigation />
        <div className="min-h-screen bg-gray-50">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-6">Teams</h1>
            <div className="bg-white rounded-lg border border-gray-200 p-12 text-center">
              <p className="text-gray-600 mb-6">You must register for an event first to view or create teams.</p>
              <button
                onClick={() => navigate('/events')}
                className="inline-block bg-gray-900 text-white px-6 py-2 rounded-lg font-medium hover:bg-gray-800"
              >
                Browse Events
              </button>
            </div>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Navigation />
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-8">Teams</h1>

          <ErrorMessage message={error} onClose={() => setError('')} />

          {/* Event Filter */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
            <label className="block text-sm font-medium text-gray-700 mb-3">Select Event</label>
            <select
              value={selectedEventId || ''}
              onChange={(e) => handleEventChange(parseInt(e.target.value))}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-transparent outline-none"
            >
              <option value="">Choose an event...</option>
              {registrations.map((reg) => (
                <option key={reg.event_id} value={reg.event_id}>
                  {reg.event_title}
                </option>
              ))}
            </select>
          </div>

          {/* Create Team Form */}
          {!showCreateForm && selectedEventId && (
            <button
              onClick={() => setShowCreateForm(true)}
              className="mb-8 bg-gray-900 text-white px-6 py-2 rounded-lg font-medium hover:bg-gray-800"
            >
              + Create Team
            </button>
          )}

          {showCreateForm && (
            <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Create New Team</h2>
              <form onSubmit={handleCreateTeam} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Team Name</label>
                  <input
                    type="text"
                    value={teamName}
                    onChange={(e) => setTeamName(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-transparent outline-none"
                    placeholder="Your team name"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                  <textarea
                    value={teamDesc}
                    onChange={(e) => setTeamDesc(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-transparent outline-none"
                    placeholder="Team description..."
                    rows="3"
                  />
                </div>

                <div className="flex gap-3">
                  <button
                    type="submit"
                    disabled={creating}
                    className="flex-1 bg-gray-900 text-white py-2 rounded-lg font-medium hover:bg-gray-800 transition-colors disabled:opacity-50"
                  >
                    {creating ? 'Creating...' : 'Create Team'}
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowCreateForm(false)}
                    className="flex-1 bg-gray-200 text-gray-900 py-2 rounded-lg font-medium hover:bg-gray-300 transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Teams List */}
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Teams for {registrations.find(r => r.event_id === selectedEventId)?.event_title || 'Event'}
            </h2>
            {teams.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {teams.map((team) => (
                  <div key={team.team_id} className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-lg transition-shadow">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">{team.name}</h3>
                    <p className="text-gray-600 text-sm mb-4 line-clamp-2">{team.description || 'No description'}</p>
                    <div className="flex items-center text-sm text-gray-600 mb-4">
                      <svg className="h-4 w-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM9 10a3 3 0 11-6 0 3 3 0 016 0zm0 0a3 3 0 110 6 3 3 0 010-6zm8-2a1 1 0 11-2 0 1 1 0 012 0zm-1 7a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                      {team.member_count || 0} members
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="bg-white rounded-lg border border-gray-200 p-12 text-center">
                <p className="text-gray-600">No teams yet. Create the first one!</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
};
