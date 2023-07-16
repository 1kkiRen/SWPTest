from googleapiclient.discovery import build
import pandas as pd
import socket

# Set up the API client

api_key = 'AIzaSyAA98QQg0DPoXT_Pp_C7vJYqYBiUmi5Iv4'  # Replace with your API key
youtube = build('youtube', 'v3', developerKey=api_key)

socket.setdefaulttimeout(3)


# Make an API request to retrieve video details
def get_comments(link, comments_number):
    try:
        video_id = link[link.rfind("/") + 1:]
        last_index = video_id.find("&")
        if last_index != -1:
            video_id = video_id[:last_index]
        video_id = video_id.replace("watch?v=", "")

        print(video_id)

        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=comments_number  # Adjust the number of results per page as needed
        ).execute()

        print(response)

        # Extract the comments from the first page
        comments = response['items']
        df = pd.DataFrame(map(lambda x: x['snippet']['topLevelComment']['snippet']['textDisplay'],
                              comments), columns=['Comments'])
        return df
    except Exception as e:
        print("Youtube api failed")
        print(e)
        return pd.DataFrame([], columns=['Comments'])

# print(get_comments("https://www.youtube.com/watch?v=GYkq9Rgoj8E"))

# Примеры ссылок
# https://www.youtube.com/watch?v=GYkq9Rgoj8E
# https://www.youtube.com/watch?v=51QO4pavK3A
# https://www.youtube.com/watch?v=F8UMrZGFsT4
