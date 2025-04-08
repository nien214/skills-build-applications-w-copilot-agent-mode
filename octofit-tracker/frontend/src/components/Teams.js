useEffect(() => {
    fetch('https://literate-lamp-97w767q6wp46279q9-8000.app.github.dev/api/teams/')
      .then(response => response.json())
      .then(data => setTeams(data))
      .catch(error => console.error('Error fetching teams:', error));
  }, []);