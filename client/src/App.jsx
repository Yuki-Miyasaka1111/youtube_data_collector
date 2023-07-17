import React, { useState } from 'react';
import axios from 'axios';
import Button from '@mui/material/Button';

function App() {
  const [channelId, setChannelId] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [videoData, setVideoData] = useState([]);

  const fetchVideoData = async () => {
    if (!channelId || !apiKey) return;
    try {
      	console.log("Making API call with:", channelId, apiKey);
      	const response = await axios.get(`http://localhost:8000/videos?channelId=${channelId}&apiKey=${apiKey}`);
      	console.log("API response:", response);
      	setVideoData(response.data || []);  // Assumes the server returns an object with a `videos` array.
    } catch (error) {
      	console.error("API call failed:", error);
    }
  };

  return (
    <div>
        <input 
            type="text"
            placeholder="API Key"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
        />
        <input 
            type="text"
            placeholder="Channel ID"
            value={channelId}
            onChange={(e) => setChannelId(e.target.value)}
        />
        <Button variant="contained" color="primary" onClick={fetchVideoData}>Fetch</Button>
        {Array.isArray(videoData) ? videoData.map((video, index) => (
            <div key={index}>
            <h2>{video.title}</h2>
            <p>{video.description}</p>
            // Add more fields as needed
            </div>
        )) : null}
    </div>
  );
}

export default App;