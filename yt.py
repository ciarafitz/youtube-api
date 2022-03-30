import os
import re
from datetime import timedelta
from googleapiclient.discovery import build

api_key = 'AIzaSyCEUwCqgHTvSzDYixlMtti7Mw8tfdP14Fw'

youtube = build('youtube', 'v3', developerKey=api_key)

hours_pattern = re.compile(r'(\d+)H') #regular expresion \d is digit H in hours
minutes_pattern = re.compile(r'(\d+)M') #M in minutes
seconds_pattern = re.compile(r'(\d+)S') #S in seconds

total_seconds = 0
nextPageToken = None
while True:
        pl_request = youtube.playlistItems().list(
                part='contentDetails',
                #playlistId="PL-osiE80TeTvviVL0pJGX5mZCo7CAvIuf",
                playlistId="PLsifFPg4DahLU-5x5ThJ0p6f69gWQUoO0", #JustinBieber JUSTICE Platlist 43 videos
                maxResults=50,
                pageToken = nextPageToken
        )

        pl_response = pl_request.execute()

        vid_ids = []
        for item in pl_response['items']:
                vid_ids.append(item['contentDetails']['videoId'])

        vid_request = youtube.videos().list(
                part="contentDetails",
                id=','.join(vid_ids)
        )

        vid_response = vid_request.execute() 


        for item in vid_response['items']:
                duration = item['contentDetails']['duration']

                hours = hours_pattern.search(duration)
                minutes = minutes_pattern.search(duration)
                seconds = seconds_pattern.search(duration)

                hours = int(hours.group(1)) if hours else 0
                minutes = int(minutes.group(1)) if minutes else 0
                seconds = int(seconds.group(1)) if seconds else 0

                video_seconds = timedelta(
                        hours = hours,
                        minutes = minutes,
                        seconds = seconds
                ).total_seconds()

                total_seconds += video_seconds
                

        nextPageToken = pl_response.get('nextPageToken')

        if not nextPageToken:
                break

total_seconds = int(total_seconds)

minutes, seconds = divmod(total_seconds, 60)
hours, minutes = divmod(minutes, 60)

print(f'{hours}:{minutes}:{seconds}')
        