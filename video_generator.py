"""
Generate video from text, audio, and visual elements
"""
import logging
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from moviepy.editor import (
    ImageClip, AudioFileClip, concatenate_videoclips,
    CompositeAudioClip, ColorClip
)
from config import (
    VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS, OUTPUT_DIR, TEMP_DIR,
    FONT_TITLE_SIZE, FONT_BODY_SIZE, FONT_SOURCE_SIZE,
    BG_COLOR, TEXT_COLOR, ACCENT_COLOR, SOURCE_COLOR
)

logger = logging.getLogger(__name__)


class VideoGenerator:
    """Generate short-form videos with text, audio, and visual layout"""
    
    def __init__(self):
        self.width = VIDEO_WIDTH
        self.height = VIDEO_HEIGHT
        self.fps = VIDEO_FPS
        self.bg_color = BG_COLOR
        self.text_color = TEXT_COLOR
        self.accent_color = ACCENT_COLOR
    
    def create_video(
        self,
        title: str,
        body_text: str,
        source: str,
        audio_path: str,
        output_path: str,
        image_path: str = None
    ) -> bool:
        """
        Create a complete video with title, body text, audio, and optional image
        
        Args:
            title: article title
            body_text: article body/summary
            source: news source name
            audio_path: path to MP3 audio file
            output_path: path to save output MP4
            image_path: optional path to background image
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create visual frames
            frame_path = self._create_visual_frame(title, body_text, source, image_path)
            
            if not frame_path:
                logger.error("Failed to create visual frame")
                return False
            
            # Create video from image and audio
            success = self._compose_video(frame_path, audio_path, output_path)
            
            # Clean up temporary files
            if os.path.exists(frame_path):
                os.remove(frame_path)
            
            return success
        
        except Exception as e:
            logger.error(f"Video creation failed: {e}")
            return False
    
    def _create_visual_frame(
        self,
        title: str,
        body_text: str,
        source: str,
        image_path: str = None
    ) -> str:
        """
        Create a visually appealing frame image
        
        Args:
            title: article title
            body_text: article body
            source: news source
            image_path: optional background image
            
        Returns:
            Path to created image, or None if failed
        """
        try:
            # Create image
            if image_path and os.path.exists(image_path):
                img = Image.open(image_path).convert("RGB")
                img = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
                # Add semi-transparent overlay
                overlay = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 180))
                img = img.convert("RGBA")
                img = Image.alpha_composite(img, overlay)
                img = img.convert("RGB")
            else:
                # Create plain background
                img = Image.new("RGB", (self.width, self.height), self.bg_color)
            
            draw = ImageDraw.Draw(img)
            
            # Load fonts (with fallback)
            try:
                font_title = ImageFont.truetype("arial.ttf", FONT_TITLE_SIZE)
                font_body = ImageFont.truetype("arial.ttf", FONT_BODY_SIZE)
                font_source = ImageFont.truetype("arial.ttf", FONT_SOURCE_SIZE)
            except:
                font_title = ImageFont.load_default()
                font_body = ImageFont.load_default()
                font_source = ImageFont.load_default()
                logger.warning("Using default fonts")
            
            # Draw title with accent bar
            title_y = 100
            draw.rectangle(
                [(50, title_y - 10), (100, title_y + 50)],
                fill=self.accent_color
            )
            
            # Wrap title text
            title_lines = textwrap.wrap(title, width=30)
            for i, line in enumerate(title_lines[:3]):  # Max 3 lines
                draw.text(
                    (120, title_y + (i * 60)),
                    line,
                    font=font_title,
                    fill=self.text_color
                )
            
            # Draw body text
            body_y = title_y + 250
            body_lines = textwrap.wrap(body_text, width=35)
            for i, line in enumerate(body_lines[:5]):  # Max 5 lines
                draw.text(
                    (80, body_y + (i * 50)),
                    line,
                    font=font_body,
                    fill=self.text_color
                )
            
            # Draw source at bottom
            source_text = f"Source: {source}"
            draw.text(
                (80, self.height - 120),
                source_text,
                font=font_source,
                fill=SOURCE_COLOR
            )
            
            # Draw decorative bottom line
            draw.rectangle(
                [(80, self.height - 80), (self.width - 80, self.height - 75)],
                fill=self.accent_color
            )
            
            # Save image
            os.makedirs(TEMP_DIR, exist_ok=True)
            output_path = os.path.join(TEMP_DIR, "frame_temp.png")
            img.save(output_path)
            
            logger.info(f"Created visual frame: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Failed to create visual frame: {e}")
            return None
    
    def _compose_video(self, image_path: str, audio_path: str, output_path: str) -> bool:
        """
        Compose video from image and audio using MoviePy
        
        Args:
            image_path: path to frame image
            audio_path: path to audio MP3
            output_path: path to save output MP4
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load audio to get duration
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            
            logger.info(f"Creating video with {duration:.1f}s audio")
            
            # Create image clip with audio duration
            image_clip = ImageClip(image_path).set_duration(duration)
            
            # Create video with audio
            video = image_clip.set_audio(audio)
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Write video file
            video.write_videofile(
                output_path,
                fps=self.fps,
                codec="libx264",
                audio_codec="aac",
                verbose=False,
                logger=None
            )
            
            logger.info(f"Video created: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Video composition failed: {e}")
            return False


if __name__ == "__main__":
    # Test video generation
    logging.basicConfig(level=logging.INFO)
    
    generator = VideoGenerator()
    
    # Create test audio first (you'll need actual audio file)
    print("Video generator initialized and ready for use.")
