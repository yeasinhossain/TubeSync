from flask import Flask, redirect, request, url_for, session, render_template, jsonify
from youtube_client import YouTubeClient
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']

@app.route('/')
def index():
    if 'credentials' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if request.method == 'POST':
        client_id = request.form.get('client_id')
        client_secret = request.form.get('client_secret')
        if client_id and client_secret:
            session['client_credentials'] = {
                'client_id': client_id,
                'client_secret': client_secret
            }
            return redirect(url_for('login'))
        else:
            return render_template('setup.html', error="Please provide both Client ID and Client Secret.")
    return render_template('setup.html')

@app.route('/login')
def login():
    if 'client_credentials' not in session:
        return redirect(url_for('setup'))
        
    try:
        creds = session['client_credentials']
        client = YouTubeClient(client_id=creds['client_id'], client_secret=creds['client_secret'])
        redirect_uri = url_for('oauth2callback', _external=True)
        # Aggressively ensure HTTPS in production behind Vercel's proxy
        if 'localhost' not in redirect_uri and '127.0.0.1' not in redirect_uri:
            redirect_uri = redirect_uri.replace('http://', 'https://')
            
        auth_url, state = client.get_authorization_url(redirect_uri=redirect_uri)
        session['state'] = state
        return redirect(auth_url)
    except Exception as e:
        return f"Error during login: {str(e)}", 500

@app.route('/oauth2callback')
def oauth2callback():
    try:
        state = session.get('state')
        if not state or state != request.args.get('state'):
            return 'Invalid state parameter', 400

        code = request.args.get('code')
        if not code:
            return 'No authorization code received', 400

        creds = session.get('client_credentials')
        if not creds:
            return redirect(url_for('setup'))

        client = YouTubeClient(client_id=creds['client_id'], client_secret=creds['client_secret'])
        redirect_uri = url_for('oauth2callback', _external=True)
        if 'localhost' not in redirect_uri and '127.0.0.1' not in redirect_uri:
            redirect_uri = redirect_uri.replace('http://', 'https://')
            
        client.complete_oauth_flow(
            state=state,
            code=code,
            redirect_uri=redirect_uri
        )
        
        session['credentials'] = client.to_pickle()
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Error during callback: {str(e)}", 500

@app.route('/dashboard')
def dashboard():
    if 'credentials' not in session:
        return redirect(url_for('login'))
    
    try:
        creds = session.get('client_credentials', {})
        client = YouTubeClient.from_pickle(session['credentials'])
        client.client_id = creds.get('client_id')
        client.client_secret = creds.get('client_secret')
        
        channel_info = client.get_channel_info()
        videos = client.get_videos()
        return render_template('dashboard.html', channel=channel_info, videos=videos)
    except Exception as e:
        session.pop('credentials', None)
        return redirect(url_for('login'))

@app.route('/api/videos', methods=['GET'])
def get_videos():
    if 'credentials' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        client = YouTubeClient.from_pickle(session['credentials'])
        videos = client.get_videos()
        return jsonify({'videos': videos})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/videos/batch-update', methods=['POST'])
def batch_update_videos():
    if 'credentials' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        client = YouTubeClient.from_pickle(session['credentials'])
        data = request.get_json()
        
        video_ids = data.get('video_ids', [])
        action_type = data.get('action_type', 'replace') # 'replace', 'append', 'prepend'
        old_text = data.get('old_text', '')
        new_text = data.get('new_text', '')
        include_titles = data.get('include_titles', True)
        include_descriptions = data.get('include_descriptions', True)
        include_tags = data.get('include_tags', True)
        
        if not video_ids:
            return jsonify({'error': 'No videos selected'}), 400
            
        if action_type == 'replace' and (not old_text or not new_text):
            return jsonify({'error': 'Missing replace text parameters'}), 400
            
        if action_type in ['append', 'prepend'] and not new_text:
            return jsonify({'error': 'Missing text to add'}), 400

        results = []
        for video_id in video_ids:
            video = client.get_video(video_id)
            if not video:
                results.append({
                    'video_id': video_id,
                    'status': 'error',
                    'message': 'Video not found'
                })
                continue

            title = video['title']
            description = video['description']
            tags = video.get('tags', []) or []
            
            # Apply changes based on action type
            if action_type == 'replace':
                if include_titles: title = title.replace(old_text, new_text)
                if include_descriptions: description = description.replace(old_text, new_text)
                if include_tags: tags = [tag.replace(old_text, new_text) for tag in tags]
            elif action_type == 'append':
                if include_titles: title = f"{title} {new_text}"
                if include_descriptions: description = f"{description}\n{new_text}"
                if include_tags: tags.append(new_text)
            elif action_type == 'prepend':
                if include_titles: title = f"{new_text} {title}"
                if include_descriptions: description = f"{new_text}\n{description}"
                if include_tags: tags = [new_text] + tags
            
            # YouTube API limits: title (100), description (5000), tags (500 chars total)
            title = title[:100]
            description = description[:5000]
            
            success = client.update_video(
                video_id,
                title=title,
                description=description,
                tags=tags
            )
            
            results.append({
                'video_id': video_id,
                'status': 'success' if success else 'error',
                'updates': {
                    'title': title,
                    'description': description,
                    'tags': tags
                } if success else None
            })

        return jsonify({
            'status': 'success',
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/switch-channel')
def switch_channel():
    try:
        session.pop('credentials', None)
        return redirect(url_for('login'))
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/logout')
def logout():
    try:
        session.clear()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error during logout: {str(e)}", 500

if __name__ == '__main__':
    # When running locally, allow HTTP for oauthlib
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(host='0.0.0.0', debug=True, port=5003)
