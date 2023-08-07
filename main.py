import pandas as pd 
import requests 
from bs4 import BeautifulSoup 
from pytube import Youtube 

# Load the excel spreadsheet 
# TODO: Turn this script into a CLI app that can 
# run as a cron job 
df = pd.read_excel('songs.xlsx') 

# Extract the song and artist columns 
songs = df['Song'] 
artist = df['Artist'] 

# create a folder to store the downloaded songs 
folder_path = 'downloads/spotify_liked_tracks' 
os.makedirs(folder_path, exist_ok=True) 

# Iterate over the songs and artist 
for song, artis in zip(songs, artists): 
	# search for the song on Youtube 
	query = f'{song} {artist} official audio' 
	search_url = f'https://www.youtube.com/results?search_query={query}'
	response = requests.get(search_url) 
	soup = BeautifulSoup(response.text, 'html.parser') 

	# find the first video link 
	video_link = soup.find('a', {'class': 'yt-uix-tile-link'}) 
	if video_link: 
		video_url = f'https://www.youtube.com{video_link["href"]}' 

		# Download the video as low-quality mp3 
		try: 
			yt = Youtube(video_url)
			audio_stream = yt.streams.filter(only_audio=True).first() 
			
			print(f'Downloading : {song} by {artist}') 
			audio_stream.download(output_path=folder_path) 
			print('Download complete') 
		
		except Exception as e: 
			print(f'Error downloadeing: {song} by {artist}') 
			print(e) 
	else: 
		print(f'Video not found for: {song} by {artist}')
