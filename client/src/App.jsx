import React, { useState } from 'react';
import axios from 'axios';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

function App() {
	const theme = createTheme({
		palette: {
		  type: "dark",
		},
	});


	const [channelId, setChannelId] = useState("");
	const [apiKey, setApiKey] = useState("");
	const [videoData, setVideoData] = useState([]);

	const fetchVideoData = async () => {
		if (!channelId || !apiKey) return;
		try {
			const response = await axios.get(`http://localhost:8001/videos?channelId=${channelId}&apiKey=${apiKey}`);
			console.log(response.data);
			setVideoData(response.data || []);
			} catch (error) {
			console.error(error);
		}
	};

	return (
		<ThemeProvider theme={theme}>
			<div style={{ padding: "1rem" }}>
				<Box
					sx={{
						marginTop: 8,
						display: "flex",
						flexDirection: "column",
						alignItems: "center",
					}}
				>
					<Typography
						variant="h3"
						sx={{
							width: "100%",
							textAlign: 'center', 
							fontSize: 40,
						}}
					>
						Youtube Data Collector
					</Typography>
					<TextField 
						sx={{
							width: 400,
							marginTop: "3rem",
						}}
						label="API Key"
						variant="outlined"
						value={apiKey}
						onChange={(e) => setApiKey(e.target.value)}
					/>
					<TextField
						sx={{
							width: 400,
							marginTop: "1rem",
						}}
						label="Channel ID"
						variant="outlined"
						value={channelId}
						onChange={(e) => setChannelId(e.target.value)}
					/>
					<Button
						sx={{
							backgroundColor: "#3D77B1",
							color: "#fff",
							marginTop: "1rem",
							width: 400,
							'&:hover': {
								backgroundColor: "#30638E", // オンマウス時の色
							},
						}}
						variant="contained" 
						onClick={fetchVideoData} 
					>
							Submit
					</Button>
				</Box>
				{Array.isArray(videoData) ? videoData.map((video, index) => (
					<Card key={index} style={{ marginTop: "1rem" }}>
					<CardContent>
						<Typography variant="h5">{video.title}</Typography>
						<Typography variant="body2">{video.description}</Typography>
						<Typography variant="body2">{video.publishedAt}</Typography>
						{video.thumbnails?.default && <img src={video.thumbnails.default.url} alt="video thumbnail" />}
						<Typography variant="body2">Category: {video.category}</Typography>
						<Typography variant="body2">Tags: {video.tags?.join(', ')}</Typography>
						<Typography variant="body2">Views: {video.viewCount}</Typography>
						<Typography variant="body2">Likes: {video.likeCount}</Typography>
						{/* <Typography variant="body2">Dislikes: {video.dislikeCount}</Typography> */}
						<Typography variant="body2">Comments: {video.commentCount}</Typography>
						<Typography variant="body2">Favorites: {video.favoriteCount}</Typography>
						<Typography variant="body2">Channel Title: {video.channelTitle}</Typography>
						<Typography variant="body2">Channel Description: {video.channelDescription}</Typography>
						<Typography variant="body2">Subscriber Count: {video.subscriberCount}</Typography>
						<Typography variant="body2">Total Views: {video.totalViews}</Typography>
						<Typography variant="body2">Total Videos: {video.totalVideos}</Typography>
						{/* <Typography variant="body2">Playlist Title: {video.playlistTitle}</Typography>
						<Typography variant="body2">Playlist Description: {video.playlistDescription}</Typography>
						<Typography variant="body2">Playlist Video Count: {video.playlistVideoCount || 'Not available'}</Typography>
						{video.comments && video.comments.map((comment, commentIndex) => (
							<div key={commentIndex}>
							<Typography variant="body2">Comment: {comment.text}</Typography>
							<Typography variant="body2">Comment Author: {comment.author}</Typography>
							<Typography variant="body2">Comment Date: {comment.date}</Typography>
							</div>
						))}
						{console.log(video)} */}
					</CardContent>
					</Card>
				)) : null}
			</div>
		</ThemeProvider>
	);
}

export default App;