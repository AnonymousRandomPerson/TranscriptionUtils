import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

scopes = ['https://www.googleapis.com/auth/youtube.readonly', 'https://www.googleapis.com/auth/youtube']

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file('client_secrets.json', scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build('youtube', 'v3', credentials=credentials)

# request = youtube.channels().list(
#     part='contentDetails',
#     mine=True
# )
# response = request.execute()
# print(response)

request = youtube.playlistItems().list(
    part='snippet,contentDetails',
    playlistId='UUtSLDYWuRxJWWHkH7cD4zdA'
)

response = request.execute()

while response:
  for video in response['items']:
    videoId = video['contentDetails']['videoId']
    name = video['snippet']['title']
    description = video['snippet']['description']
    if 'Parts:' in description:
      description = description.replace('Parts:', 'PDF/MIDI/MusicXML:')
      otherFormatsIndex = description.find('\n\nOther formats')
      if otherFormatsIndex > -1:
        description = description[:otherFormatsIndex]
      print('Updating', videoId, name, 'with new description', description)

      updateResponse = youtube.videos().update(
        part='snippet',
        body={
          'id': videoId,
          'snippet': {
            'title': name,
            'categoryId': '10',
            'description': description
          }
        }
      ).execute()

  next_request = youtube.playlistItems().list_next(request, response)
  if next_request is None:
    response = None
  else:
    response = next_request.execute()
