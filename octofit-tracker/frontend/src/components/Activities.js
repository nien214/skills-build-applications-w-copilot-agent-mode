import React, { useState, useEffect } from 'react';

function Activities() {
  const [activities, setActivities] = useState([]);

  useEffect(() => {
    console.log('Activities component mounted');
    fetch('/api/activities/')
      .then(response => {
        console.log('API response status:', response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Fetched activities:', data);
        // Map API response to expected structure
        const mappedActivities = data.map(activity => ({
          id: activity.id,
          name: activity.activity_type, // Map activity_type to name
          duration: activity.duration,
          calories: 'N/A', // Placeholder for calories
          date: activity.date || 'Unknown', // Include date field
        }));
        console.log('Mapped activities:', mappedActivities); // Log mapped activities
        setActivities(mappedActivities);
      })
      .catch(error => console.error('Error fetching activities:', error));
  }, []);

  console.log('Activities state:', activities); // Log activities state before rendering

  return (
    <div className="container mt-4">
      <h1 className="mb-4">Activities</h1>
      {activities.length === 0 ? (
        <p>No activities available. Please check back later or ensure the API is working correctly.</p>
      ) : (
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Activity</th>
              <th>Duration</th>
              <th>Calories Burned</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {activities.map(activity => (
              <tr key={activity.id}>
                <td>{activity.name}</td>
                <td>{activity.duration}</td>
                <td>{activity.calories}</td>
                <td>{activity.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default Activities;