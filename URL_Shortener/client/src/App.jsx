import React, { useState } from 'react';

function UrlShortener() {
  const [longUrl, setLongUrl] = useState('');
  const [shortUrl, setShortUrl] = useState('');
  const [error, setError] = useState('');

  const handleShorten = async (e) => {
    e.preventDefault();
    setError('');
    setShortUrl('');
    try {
      const resp = await fetch('http://localhost:8000/shorten/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ url: longUrl }),
      });
      const data = await resp.json();
      if (resp.ok && data.short_url) {
        setShortUrl(data.short_url);
      } else {
        setError(data.detail || 'Error creating short URL');
      }
    } catch {
      setError('Network error');
    }
  };

  return (
    <div style={{ maxWidth: 500, margin: "auto", padding: 30 }}>
      <h2>URL Shortener</h2>
      <form onSubmit={handleShorten}>
        <input
          type="url"
          value={longUrl}
          onChange={e => setLongUrl(e.target.value)}
          placeholder="Paste your long URL here"
          style={{ width: "100%", padding: "8px" }}
          required
        />
        <button type="submit" style={{ marginTop: 12 }}>Shorten</button>
      </form>
      {shortUrl && (
        <p style={{ marginTop: 16 }}>
          Short URL:<br />
          <a href={shortUrl} target="_blank" rel="noopener noreferrer">{shortUrl}</a>
        </p>
      )}
      {error && (
        <p style={{ color: 'red', marginTop: 12 }}>{error}</p>
      )}
    </div>
  );
}

export default UrlShortener;