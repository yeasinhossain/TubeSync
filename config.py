import os
import secrets

class Config:
    # Flask settings
    # We generate a random secret key for dev if not provided, but on Vercel
    # this needs to be set in environment variables!
    SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(16))
    
    # YouTube API settings
    YOUTUBE_API_SCOPES = [
        'https://www.googleapis.com/auth/youtube.force-ssl',
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/userinfo.email'
    ]
