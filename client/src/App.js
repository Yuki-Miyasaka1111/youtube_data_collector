import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
    const [videoInfo, setVideoInfo] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            const response = await axios.get('http://localhost:8000/video/some_video_id');
            setVideoInfo(response.data);
        };
        fetchData();
    }, []);

    return (
        <div className="App">
        {videoInfo && (
            <div>
            <h1>{videoInfo.items[0].snippet.title}</h1>
            <p>{videoInfo.items[0].snippet.description}</p>
            </div>
        )}
        </div>
    );
}

export default App;
