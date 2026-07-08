# 🛠️ Complete Setup Guide - ElevenLabs Edition

This guide walks you through setting up the News Video Agent with ElevenLabs TTS.

**Best part: NO CREDIT CARD NEEDED!** 🎉

## Step 1: Get Your API Keys

### 1.1 NewsAPI Key

1. Visit **https://newsapi.org/register**
2. Create a free account with your email
3. Verify your email
4. You'll see your API key on the dashboard
5. Copy and save it (you'll need it in Step 4)

### 1.2 ElevenLabs API Key (NO CREDIT CARD!)

ElevenLabs is perfect because it needs **no credit card at all**!

#### Step 1: Sign Up (Free)

1. Go to **https://elevenlabs.io**
2. Click **"Sign Up"** (top right)
3. Enter your email and password
4. **NO CREDIT CARD REQUIRED!** ✅
5. Verify your email
6. Done!

#### Step 2: Get Your API Key

1. Log in to ElevenLabs dashboard
2. Click your **profile icon** (top right)
3. Go to **"Account"** or **"Profile Settings"**
4. Find **"API Key"** section
5. Click **"Show API Key"** or **"Copy"**
6. Save it safely (you'll need it in Step 4)

#### Step 3: Check Free Tier

Your free account includes:
- ✅ **10,000 characters per month** (completely free!)
- ✅ Perfect for 3-5 videos per day
- ✅ High-quality British English voices
- ✅ No limits, no credit card needed!

---

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

---

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

---

## Step 4: Configure Environment

### 4.1 Copy Example Configuration

```bash
cp .env.example .env
```

### 4.2 Edit `.env` File

Open `.env` in a text editor (Notepad, VSCode, etc.):

```env
# REQUIRED: Your APIs
NEWS_API_KEY=your_newsapi_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Optional settings (keep as default)
VIDEOS_PER_DAY=3
SCHEDULE_TIME=09:00
```

**Where to find these values:**
- `NEWS_API_KEY`: From NewsAPI website (Step 1.1)
- `ELEVENLABS_API_KEY`: From ElevenLabs dashboard (Step 1.2)

### 4.3 Verify Configuration

```bash
python -c "from config import *; print('✓ Configuration loaded successfully')"
```

---

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

### 5.2 Test ElevenLabs Connection

```bash
python -c "
from text_to_speech import TextToSpeech
print('Testing ElevenLabs TTS...')
tts = TextToSpeech()
print('✓ Connected to ElevenLabs successfully!')
"
```

### 5.3 Test Audio Generation

```bash
python -c "
from text_to_speech import TextToSpeech
from config import TEMP_DIR
import os

tts = TextToSpeech()
test_file = os.path.join(TEMP_DIR, 'test.mp3')
result = tts.synthesize_speech('This is a test of the text to speech system.', test_file)
if result:
    print(f'✓ TTS test successful!')
    print(f'✓ Audio file created: {test_file}')
else:
    print('✗ TTS test failed - check API key')
"
```

### 5.4 Test Full Pipeline

```bash
python main.py test
```

This will:
1. Fetch 1 trending article
2. Process it
3. Generate TTS audio using ElevenLabs
4. Create a video
5. Show results

Expected output:
```
INFO - Processing article: [Article Title]
INFO - Generating text-to-speech audio...
✓ Audio generated: ./temp/audio_*.mp3
INFO - Generating video...
✓ Article processed successfully: ./output/videos/video_*.mp4
```

---

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

---

## Step 7: Monitor and Debug

### 7.1 Check Logs

```bash
# View live logs (real-time)
tail -f logs/agent_20240107.log

# View errors only
grep ERROR logs/agent_20240107.log

# View ElevenLabs logs
grep "ElevenLabs\|Audio generated" logs/agent_20240107.log
```

### 7.2 Check Output Videos

Videos are saved to `output/videos/`:

```bash
ls -la output/videos/
```

Each video file is named: `video_YYYYMMDD_HHMMSS.mp4`

### 7.3 Check ElevenLabs Usage

1. Log in to https://elevenlabs.io
2. Go to **Account** or **Profile Settings**
3. Check **"Usage"** or **"Characters Used This Month"**
4. Your free tier shows: Characters used / 10,000

### 7.4 Common Issues and Solutions

| Problem | Solution |
|---------|----------|
| **"Invalid ElevenLabs API key"** | Check ELEVENLABS_API_KEY in .env is correct |
| **"Free tier limit reached"** | Upgraded to paid plan or wait for next month |
| **"No module named requests"** | Run `pip install -r requirements.txt` again |
| **"ffmpeg not found"** | Install FFmpeg and add to PATH |
| **"Permission denied"** | Make sure you have write access to the directory |

---

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

---

## Step 9: Upload to Social Media (Setup)

### 9.1 Manual Upload (Easiest)

For now, you can upload videos manually:

1. Go to `output/videos/`
2. Download the latest `video_*.mp4`
3. Upload to TikTok/WeChat manually

### 9.2 Automated Upload (Advanced)

Once you have proper API credentials:

1. Get TikTok API token from https://developer.tiktok.com
2. Get WeChat token from https://mp.weixin.qq.com
3. Add tokens to `.env`
4. They will upload automatically

---

## ✅ Setup Complete!

Your News Video Agent is now ready. Run:

```bash
python main.py once
```

to generate your first videos!

---

## 💡 ElevenLabs Features

### Free Tier Includes:
- ✅ **10,000 characters per month** (completely free!)
- ✅ **100+ voices** in 30+ languages
- ✅ **British English voices** (Victoria, Amy, etc.)
- ✅ **High quality** - professional sound
- ✅ **No credit card required**
- ✅ **No hidden fees**

### Usage Estimate for Your Agent:
- ~200 chars per video
- 3-5 videos per day = 1,000 chars/day
- ~30,000 chars/month
- **Free tier (10,000 chars/month) is perfect for testing!**
- When you're ready to scale, you can upgrade

---

## 📞 Troubleshooting Help

If you encounter issues:

1. **Check API Key** - Ensure ELEVENLABS_API_KEY in .env is correct
2. **Check Usage** - Log in to ElevenLabs to verify free tier usage
3. **Check logs** - Look in `logs/` directory for details
4. **Test components** - Run individual tests from Step 5
5. **Check internet** - Make sure you have internet connection for API calls

---

## 🎓 Learning Resources

- **Python**: https://www.learnpython.org
- **ElevenLabs**: https://elevenlabs.io/docs
- **NewsAPI**: https://newsapi.org/docs
- **TikTok API**: https://developer.tiktok.com/doc/
- **WeChat API**: https://developers.weixin.qq.com/doc

---

## 🚀 Next Steps

1. ✅ Sign up to ElevenLabs (https://elevenlabs.io) - NO CREDIT CARD!
2. ✅ Get your API key
3. ✅ Get your NewsAPI key
4. ✅ Follow this guide step-by-step
5. ✅ Test with `python main.py test`
6. ✅ Generate videos with `python main.py once`
7. ✅ Deploy to run daily

---

**Happy coding! Your journey to creating amazing short-form videos starts now!** 🎬📱✨

**Questions?** Check the troubleshooting section or visit ElevenLabs documentation!
