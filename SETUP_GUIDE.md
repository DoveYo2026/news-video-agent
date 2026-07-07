# 🛠️ Complete Setup Guide

This guide walks you through setting up the News Video Agent from scratch.

## Step 1: Get Your API Keys

### 1.1 NewsAPI Key

1. Visit **https://newsapi.org/register**
2. Create a free account with your email
3. Verify your email
4. You'll see your API key on the dashboard
5. Copy the API key

### 1.2 Google Cloud Text-to-Speech

1. Go to **https://console.cloud.google.com**
2. Create a new project (or select existing)
3. Enable "Cloud Text-to-Speech API":
   - Search for "Text-to-Speech"
   - Click "Enable"
4. Create Service Account:
   - Go to "Service Accounts" in left menu
   - Click "Create Service Account"
   - Name: `news-video-agent`
   - Click "Create and Continue"
5. Grant Permissions:
   - Role: "Cloud Text-to-Speech API User"
   - Click "Continue" then "Done"
6. Create Key:
   - Click on service account name
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key"
   - Select "JSON"
   - Download the JSON file
   - Save to a safe location (e.g., `~/credentials/gcloud-tts.json`)

### 1.3 TikTok API (Optional)

> **Note**: TikTok API requires a business account and special approval

1. Go to **https://developer.tiktok.com**
2. Sign in with TikTok account
3. Apply for developer access
4. Create an application
5. Get OAuth credentials after approval
6. Copy your access token

### 1.4 WeChat Official Account (Optional)

> **Note**: WeChat requires a registered official account (服务号 or 订阅号)

1. Register at **https://mp.weixin.qq.com**
2. Get to "Settings" > "Account Information"
3. Find "API Credentials" or similar
4. Copy:
   - AppID
   - AppSecret (or Access Token if available)

## Step 2: Set Up Your Computer

### 2.1 Install Python

- **Windows/Mac**: Download from https://www.python.org/downloads
- **Linux**: `sudo apt-get install python3 python3-venv`
- Verify: `python --version` (should be 3.8 or higher)

### 2.2 Install FFmpeg

FFmpeg is needed for video creation.

**Windows**:
- Download from https://ffmpeg.org/download.html
- Extract to a folder
- Add to system PATH

**Mac**:
```bash
brew install ffmpeg
```

**Linux**:
```bash
sudo apt-get install ffmpeg
```

Verify: `ffmpeg -version`

### 2.3 Install ImageMagick (Optional but recommended)

For better image processing.

**Windows**: Download from https://imagemagick.org/download

**Mac**:
```bash
brew install imagemagick
```

**Linux**:
```bash
sudo apt-get install imagemagick
```

## Step 3: Clone and Setup Repository

### 3.1 Clone Repository

```bash
git clone https://github.com/DoveYo2026/news-video-agent.git
cd news-video-agent
```

### 3.2 Create Virtual Environment

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal line.

### 3.3 Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This may take a few minutes the first time.

## Step 4: Configure Environment

### 4.1 Copy Example Configuration

```bash
cp .env.example .env
```

### 4.2 Edit `.env` File

Open `.env` in a text editor (Notepad, VSCode, etc.):

```env
# REQUIRED: Your APIs
NEWS_API_KEY=paste_your_newsapi_key_here
GOOGLE_APPLICATION_CREDENTIALS=/path/to/google-credentials.json

# OPTIONAL: For social media uploads
TIKTOK_ACCESS_TOKEN=your_tiktok_token
WECHAT_ACCESS_TOKEN=your_wechat_token

# Configuration (keep as default unless you know what you're doing)
VIDEOS_PER_DAY=3
SCHEDULE_TIME=09:00
VIDEO_WIDTH=1080
VIDEO_HEIGHT=1920
TTS_LANGUAGE_CODE=en-GB
TTS_VOICE_NAME=en-GB-Standard-B
```

**Important**: 
- Replace `paste_your_newsapi_key_here` with your actual NewsAPI key
- Replace `/path/to/google-credentials.json` with the actual path to your downloaded JSON file (e.g., `C:\Users\YourName\credentials\gcloud-tts.json` on Windows)

### 4.3 Verify Configuration

```bash
python -c "from config import *; print('✓ Configuration loaded successfully')"
```

## Step 5: Test the Agent

### 5.1 Test News Fetching

```bash
python -c "
from news_fetcher import NewsFetcher
fetcher = NewsFetcher()
articles = fetcher.fetch_top_headlines(category='technology', limit=1)
print(f'✓ Fetched {len(articles)} article(s)')
for article in articles:
    print(f'  - {article[\"title\"][:60]}...')
"
```

### 5.2 Test Text-to-Speech

```bash
python -c "
from text_to_speech import TextToSpeech
from config import TEMP_DIR
import os

tts = TextToSpeech()
test_file = os.path.join(TEMP_DIR, 'test.mp3')
result = tts.synthesize_speech('This is a test of the text to speech system.', test_file)
print(f'✓ TTS test: {\"Success\" if result else \"Failed\"}')"
```

### 5.3 Test Full Pipeline

```bash
python main.py test
```

This will:
1. Fetch 1 trending article
2. Process it
3. Generate TTS audio
4. Create a video
5. Show results

Expected output:
```
INFO - Processing article: [Article Title]
INFO - Generating text-to-speech audio...
INFO - Generating video...
INFO - Uploading to social media platforms...
✓ Article processed successfully: ./output/videos/video_YYYYMMDD_HHMMSS.mp4
```

## Step 6: Run the Agent

### 6.1 Generate Videos Now (Once)

```bash
python main.py once
```

This will generate 3-5 videos immediately.

### 6.2 Run as Daily Scheduler

```bash
python main.py
```

This will:
- Generate videos every day at 09:00 (configurable in `.env`)
- Keep running in the background
- Log all activities to `logs/agent_YYYYMMDD.log`

Press `Ctrl+C` to stop.

## Step 7: Monitor and Debug

### 7.1 Check Logs

```bash
# View live logs (real-time)
tail -f logs/agent_20240107.log

# View errors only
grep ERROR logs/agent_20240107.log

# View TikTok uploads only
grep "tiktok" logs/agent_20240107.log
```

### 7.2 Check Output Videos

Videos are saved to `output/videos/`:

```bash
ls -la output/videos/
```

Each video file is named: `video_YYYYMMDD_HHMMSS.mp4`

### 7.3 Common Issues and Solutions

| Problem | Solution |
|---------|----------|
| **"API key invalid"** | Check `.env` has correct key |
| **"No module named google"** | Run `pip install -r requirements.txt` again |
| **"ffmpeg not found"** | Install FFmpeg and add to PATH |
| **"Permission denied"** | Make sure you have write access to the directory |
| **"TLS certificate error"** | Update certificates: `pip install --upgrade certifi` |

## Step 8: Set Up Continuous Running (Optional)

### 8.1 Windows - Task Scheduler

1. Open "Task Scheduler"
2. Create Basic Task
3. Name: "News Video Agent"
4. Trigger: "Daily" at 09:00
5. Action: "Start a program"
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `C:\path\to\main.py once`
   - Start in: `C:\path\to\news-video-agent`

### 8.2 Mac/Linux - Crontab

```bash
# Open crontab editor
crontab -e

# Add this line (generates videos at 9 AM daily):
0 9 * * * cd /path/to/news-video-agent && /path/to/venv/bin/python main.py once
```

## Step 9: Upload to Social Media (Setup)

### 9.1 Manual Upload

For now, you can upload videos manually:

1. Go to `output/videos/`
2. Download the latest `video_*.mp4`
3. Upload to TikTok/WeChat manually

### 9.2 Automated Upload

Once you have proper API credentials:

1. Add tokens to `.env`
2. They will upload automatically

## ✅ Setup Complete!

Your News Video Agent is now ready. Run:

```bash
python main.py once
```

to generate your first videos!

---

## 📞 Troubleshooting Help

If you encounter issues:

1. **Check the error message** - Copy the exact error
2. **Check logs** - Look in `logs/` directory for details
3. **Verify credentials** - Ensure all API keys are correct in `.env`
4. **Test components** - Run individual tests from Step 5
5. **Check GitHub Issues** - See if others had the same problem

## 🎓 Learning Resources

- **Python**: https://www.learnpython.org
- **Google Cloud TTS**: https://cloud.google.com/text-to-speech/docs
- **NewsAPI**: https://newsapi.org/docs
- **TikTok API**: https://developer.tiktok.com/doc/
- **WeChat API**: https://developers.weixin.qq.com/doc

Happy coding! 🚀
