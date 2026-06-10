# TubeSync

A powerful, open-source web application for batch updating YouTube video titles, descriptions, and tags. TubeSync is built to run entirely serverless on Vercel, using a "Bring Your Own Credentials" (BYOC) architecture so you never have to worry about API quotas.

## Features
- **Bring Your Own Credentials**: Uses your own Google Cloud Client ID and Secret for unlimited quota.
- **Batch Update Metadata**: Find & Replace, Append, or Prepend text to your video titles, descriptions, and tags.
- **Multi-channel support**: Manage any channel you have OAuth access to.
- **Serverless Ready**: Specifically optimized for 1-click deployment on Vercel.
- **Modern UI**: Clean, responsive interface built with Tailwind CSS.

## 🚀 One-Click Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fyourusername%2Ftubesync)

*Note: You must set the `SECRET_KEY` environment variable in your Vercel project settings for sessions to work.*

## Local Setup

1. Install Python 3.8 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application locally:
```bash
python app.py
```

4. Go to `http://localhost:5003` in your browser.

## How to get Google API Credentials
TubeSync requires your own Google Cloud OAuth credentials to interact with the YouTube API.

1. Go to the [Google Cloud Console](https://console.cloud.google.com).
2. Create a new project.
3. Enable the **YouTube Data API v3** in the API Library.
4. Go to **Credentials** -> Create Credentials -> **OAuth client ID**.
5. Set Application type to **Web application**.
6. Add your authorized redirect URIs:
   - For local development: `http://localhost:5003/oauth2callback`
   - For Vercel: `https://your-app-name.vercel.app/oauth2callback`
7. Copy the generated **Client ID** and **Client Secret** and paste them into the TubeSync setup page.

## Security Note
- Your Client ID and Client Secret are stored securely in your browser's encrypted session cookie. They are never saved to a database.
- For production, ensure you generate a strong, random `SECRET_KEY` environment variable so Flask can securely sign the cookies.
