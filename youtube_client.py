import os
import pickle
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from typing import List, Dict, Any
import base64
from google.oauth2.credentials import Credentials

class YouTubeClient:
    def __init__(self, client_id: str = None, client_secret: str = None):
        self.api = None
        self.credentials = None
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']
        self.flow = None

    def get_client_config(self, redirect_uri: str) -> dict:
        return {
            "web": {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [redirect_uri]
            }
        }

    def to_pickle(self) -> str:
        """Serialize the credentials to a base64 string."""
        if self.credentials:
            creds_dict = {
                'token': self.credentials.token,
                'refresh_token': self.credentials.refresh_token,
                'token_uri': self.credentials.token_uri,
                'client_id': self.credentials.client_id,
                'client_secret': self.credentials.client_secret,
                'scopes': self.credentials.scopes
            }
            return base64.b64encode(pickle.dumps(creds_dict)).decode('utf-8')
        return ''

    @classmethod
    def from_pickle(cls, pickle_str: str) -> 'YouTubeClient':
        """Deserialize the credentials from a base64 string."""
        if not pickle_str:
            raise ValueError("No pickled credentials data provided")
        
        client = cls()
        creds_dict = pickle.loads(base64.b64decode(pickle_str.encode('utf-8')))
        
        client.credentials = Credentials(
            token=creds_dict['token'],
            refresh_token=creds_dict['refresh_token'],
            token_uri=creds_dict['token_uri'],
            client_id=creds_dict['client_id'],
            client_secret=creds_dict['client_secret'],
            scopes=creds_dict['scopes']
        )
        
        client.api = build('youtube', 'v3', credentials=client.credentials)
        return client

    def get_authorization_url(self, redirect_uri: str) -> tuple[str, str]:
        """Get the authorization URL for OAuth2 flow."""
        self.flow = Flow.from_client_config(
            self.get_client_config(redirect_uri),
            scopes=self.scopes,
            redirect_uri=redirect_uri
        )
        authorization_url, state = self.flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        return authorization_url, state

    def complete_oauth_flow(self, state: str, code: str, redirect_uri: str):
        """Complete the OAuth flow with the received code."""
        if not self.flow:
            self.flow = Flow.from_client_config(
                self.get_client_config(redirect_uri),
                scopes=self.scopes,
                redirect_uri=redirect_uri
            )
        
        # Set the state and code
        self.flow.fetch_token(code=code)
        self.credentials = self.flow.credentials
        self.api = build('youtube', 'v3', credentials=self.credentials)

    def get_channel_info(self) -> Dict[str, str]:
        if not self.api:
            raise ValueError("YouTube API client not initialized")
            
        response = self.api.channels().list(
            part='snippet,contentDetails',
            mine=True
        ).execute()
        
        if response['items']:
            channel = response['items'][0]
            return {
                'id': channel['id'],
                'title': channel['snippet']['title'],
                'url': f"https://www.youtube.com/channel/{channel['id']}"
            }
        return {}

    def get_video(self, video_id: str) -> Dict[str, Any]:
        """Get a single video's details."""
        if not self.api:
            raise ValueError("YouTube API client not initialized")
            
        response = self.api.videos().list(
            part='snippet',
            id=video_id
        ).execute()
        
        if response['items']:
            snippet = response['items'][0]['snippet']
            return {
                'id': video_id,
                'title': snippet.get('title', ''),
                'description': snippet.get('description', ''),
                'tags': snippet.get('tags', []),
                'publishedAt': snippet.get('publishedAt', ''),
                'thumbnail_url': snippet.get('thumbnails', {}).get('medium', {}).get('url', '')
            }
        return None

    def get_videos(self, date_after=None, date_before=None, query=None) -> List[Dict[str, Any]]:
        if not self.api:
            raise ValueError("YouTube API client not initialized")
            
        videos = []
        page_token = None

        while True:
            request = self.api.search().list(
                part='snippet',
                forMine=True,
                maxResults=50,
                type='video',
                pageToken=page_token
            )
            
            response = request.execute()
            
            for item in response['items']:
                video_id = item['id']['videoId']
                snippet = item['snippet']
                
                # Get full video details including tags
                video_response = self.api.videos().list(
                    part='snippet',
                    id=video_id
                ).execute()
                
                if video_response['items']:
                    full_snippet = video_response['items'][0]['snippet']
                    videos.append({
                        'id': video_id,
                        'title': full_snippet.get('title', ''),
                        'description': full_snippet.get('description', ''),
                        'tags': full_snippet.get('tags', []),
                        'publishedAt': full_snippet.get('publishedAt', ''),
                        'thumbnail_url': full_snippet.get('thumbnails', {}).get('medium', {}).get('url', '')
                    })

            page_token = response.get('nextPageToken')
            if not page_token:
                break

        return videos

    def update_video(self, video_id: str, title: str = None, description: str = None, 
                    tags: List[str] = None) -> bool:
        if not self.api:
            raise ValueError("YouTube API client not initialized")
            
        try:
            # Get current video details
            video_response = self.api.videos().list(
                part='snippet',
                id=video_id
            ).execute()

            if not video_response['items']:
                return False

            snippet = video_response['items'][0]['snippet']

            # Update only provided fields
            if title is not None:
                snippet['title'] = title
            if description is not None:
                snippet['description'] = description
            if tags is not None:
                snippet['tags'] = tags

            # Update video
            self.api.videos().update(
                part='snippet',
                body={
                    'id': video_id,
                    'snippet': snippet
                }
            ).execute()

            return True
        except Exception as e:
            print(f"Error updating video {video_id}: {str(e)}")
            return False

    def logout(self):
        self.credentials = None
        self.api = None
        self.flow = None
