# 🛠️ Complete Setup Guide - Amazon Polly Edition

This guide walks you through setting up the News Video Agent with Amazon Polly TTS.

## Step 1: Get Your API Keys

### 1.1 NewsAPI Key

1. Visit **https://newsapi.org/register**
2. Create a free account with your email
3. Verify your email
4. You'll see your API key on the dashboard
5. Copy and save it (you'll need it in Step 4)

### 1.2 Amazon Polly TTS (NEW - EASIER!)

Amazon Polly is much easier to set up than Google Cloud!

#### Step 1: Create AWS Account

1. Go to **https://aws.amazon.com**
2. Click **"Create AWS Account"** (top right)
3. Fill in:
   - Email address
   - Password
   - AWS account name
4. Click **"Create Account and Continue"**
5. Verify your email address
6. Add payment method (required, but won't charge for free tier)

#### Step 2: Get AWS Credentials

1. Log in to **AWS Console**: https://console.aws.amazon.com
2. Click your **account name** (top right)
3. Select **"Security Credentials"**
4. Go to **"Access Keys"** section
5. Click **"Create New Access Key"**
6. **Download the CSV file** - contains:
   - Access Key ID
   - Secret Access Key
7. **Save this file safely** (you'll need it in Step 4)

#### Step 3: Verify Polly is Available

1. In AWS Console, search for **"Polly"**
2. Go to **"Polly"** service
3. You should see the dashboard (no additional setup needed!)
4. Polly is **free tier**: 5 million characters per month

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

#### Option A: Using AWS Credentials (Easier)

Add your AWS credentials directly to `.env`:

```env
# Required: Your APIs
NEWS_API_KEY=your_newsapi_key_here

# AWS Credentials (from the CSV file you downloaded)
AWS_ACCESS_KEY_ID=AKIA3XXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxx
AWS_DEFAULT_REGION=us-east-1

# TTS Settings (keep defaults)
TTS_VOICE_ID=Amy
TTS_LANGUAGE_CODE=en-GB
TTS_ENGINE=neural

# Video settings (optional - keep as default)
VIDEOS_PER_DAY=3
SCHEDULE_TIME=09:00
```

**Where to find these values:**
- `NEWS_API_KEY`: From NewsAPI website
- `AWS_ACCESS_KEY_ID` & `AWS_SECRET_ACCESS_KEY`: From the CSV file you downloaded
- `AWS_DEFAULT_REGION`: Usually `us-east-1`

#### Option B: Using AWS CLI Configuration (Recommended for Production)

If you want to use the AWS CLI config file instead:

1. **Install AWS CLI**: https://aws.amazon.com/cli/
2. **Configure credentials**:
```bash
aws configure
```
Then just leave the AWS settings blank in `.env`:
```env
NEWS_API_KEY=your_newsapi_key_here

# Leave these blank if using AWS CLI credentials file
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=us-east-1
```

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

### 5.2 Test Text-to-Speech with Amazon Polly

```bash
python -c "
from text_to_speech import TextToSpeech
from config import TEMP_DIR
import os

print('Initializing Amazon Polly...')
tts = TextToSpeech()
print('✓ Polly initialized successfully!')

print('Available British English voices:')
voices = TextToSpeech.get_available_voices()
for voice_id, info in voices.items():
    print(f'  - {voice_id}: {info[\"Name\"]} ({info[\"Gender\"]})')
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
    print(f'✓ Audio file: {test_file}')
    duration = tts.get_audio_duration(test_file)
    print(f'✓ Duration: {duration:.1f} seconds')
else:
    print('✗ TTS test failed - check AWS credentials')
"
```

### 5.4 Test Full Pipeline

```bash
python main.py test
```

This will:
1. Fetch 1 trending article
2. Process it
3. Generate TTS audio using Amazon Polly
4. Create a video
5. Show results

Expected output:
```
INFO - Processing article: [Article Title]
INFO - Generating text-to-speech audio...
✓ Audio generated: ./temp/audio_*.mp3
INFO - Generating video...
INFO - Uploading to social media platforms...
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

# View Polly TTS logs
grep "Polly\|Audio generated" logs/agent_20240107.log
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
| **"Unable to locate credentials"** | Check AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in .env or AWS CLI config |
| **"InvalidParameterException"** | Text is invalid or too long - check article content |
| **"AccessDenied"** | AWS credentials are wrong or don't have Polly permissions |
| **"No module named boto3"** | Run `pip install -r requirements.txt` again |
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

## 💡 Amazon Polly Voice Options

Available British English voices:

| Voice ID | Name | Gender | Quality |
|----------|------|--------|---------|
| **Amy** | Amy | Female | Neural (Best) |
| **Brian** | Brian | Male | Neural (Best) |
| **Emma** | Emma | Female | Standard |
| **Arthur** | Arthur | Male | Neural (Very Good) |
| **Olivia** | Olivia | Female | Neural (Excellent) |

**Recommended**: `Amy` (default) - Professional British female voice

To use a different voice, change `TTS_VOICE_ID` in `.env`

---

## 📞 Troubleshooting Help

If you encounter issues:

1. **Check AWS Credentials** - Ensure they're in `.env` or AWS CLI config
2. **Check logs** - Look in `logs/` directory for details
3. **Verify AWS account** - Make sure Polly is available in your region
4. **Test components** - Run individual tests from Step 5
5. **Check GitHub Issues** - See if others had the same problem

---

## 🎓 Learning Resources

- **Python**: https://www.learnpython.org
- **Amazon Polly**: https://aws.amazon.com/polly/
- **NewsAPI**: https://newsapi.org/docs
- **AWS CLI**: https://aws.amazon.com/cli/
- **TikTok API**: https://developer.tiktok.com/doc/
- **WeChat API**: https://developers.weixin.qq.com/doc

---

## 🚀 Next Steps

1. ✅ Create AWS account
2. ✅ Get credentials
3. ✅ Follow this guide step-by-step
4. ✅ Test with `python main.py test`
5. ✅ Generate videos with `python main.py once`
6. ✅ Deploy to run daily

Happy coding! 🎬📱✨
