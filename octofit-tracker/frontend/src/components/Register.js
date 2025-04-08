import React, { useState } from 'react';
import axios from 'axios';

function Register() {
  const [name, setName] = useState(''); // Changed from username to name
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [age, setAge] = useState('');
  const [message, setMessage] = useState('');

  const handleRegister = async () => {
    if (!name || !email || !password || !age) { // Updated to check name instead of username
      setMessage('All fields are required.');
      return;
    }

    try {
      const response = await axios.post('/api/users/', {
        name, // Updated to send name instead of username
        email,
        password,
        age,
      });
      setMessage('Registration successful!');
    } catch (error) {
      if (error.response && error.response.data) {
        const errorMessages = Object.values(error.response.data).join(' ');
        setMessage(`Registration failed: ${errorMessages}`);
      } else {
        setMessage('Registration failed. Please try again.');
      }
    }
  };

  return (
    <div>
      <h1>Register</h1>
      <input
        type="text"
        placeholder="Name" // Updated placeholder
        value={name} // Updated to use name
        onChange={(e) => setName(e.target.value)} // Updated to setName
      />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <input
        type="number"
        placeholder="Age"
        value={age}
        onChange={(e) => setAge(e.target.value)}
      />
      <button onClick={handleRegister}>Sign Up</button>
      {message && <p>{message}</p>}
    </div>
  );
}

export default Register;
