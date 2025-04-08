import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    fetch('/api/workouts/')
      .then(response => response.json())
      .then(data => setWorkouts(data))
      .catch(error => console.error('Error fetching workouts:', error));
  }, []);

  const fetchSuggestions = async () => {
    try {
      const response = await axios.get('/api/workouts/suggestions/', {
        headers: {
          Authorization: `Token ${localStorage.getItem('authToken')}`,
        },
      });
      setSuggestions(response.data.workout_suggestions);
    } catch (error) {
      console.error('Error fetching workout suggestions:', error);
      alert('Please log in to view personalized suggestions.');
    }
  };

  return (
    <div className="container mt-4">
      <h1 className="mb-4">Workouts</h1>
      <button onClick={fetchSuggestions} className="btn btn-primary mb-4">Get Personalized Suggestions</button>
      {suggestions.length > 0 && (
        <div>
          <h2>Personalized Suggestions</h2>
          <ul>
            {suggestions.map((suggestion, index) => (
              <li key={index}>
                {suggestion.name} - {suggestion.duration} - {suggestion.calories} calories
              </li>
            ))}
          </ul>
        </div>
      )}
      <h2>All Workouts</h2>
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Workout</th>
            <th>Duration</th>
            <th>Calories Burned</th>
          </tr>
        </thead>
        <tbody>
          {workouts.map(workout => (
            <tr key={workout.id}>
              <td>{workout.name}</td>
              <td>{workout.duration}</td>
              <td>{workout.calories}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Workouts;