#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import logging
import tempfile
import shutil
from datetime import datetime

# Install yt-dlp if not available
def install_ytdlp():
    try:
        import yt_dlp
        print("✅ yt-dlp already installed")
    except ImportError:
        print("📦 Installing yt-dlp...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp", "--quiet"])
        import yt_dlp
        print("✅ yt-dlp installed successfully")

# Install yt-dlp first
install_ytdlp()
import yt_dlp

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class YouTubeDownloader:
    def __init__(self):
        self.download_dir = tempfile.mkdtemp()
        logger.info(f"🗂️ Download directory: {self.download_dir}")
        
    def test_youtube_access(self):
        """Test if we can access YouTube from Railway"""
        test_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll (short video)
            "https://www.youtube.com/watch?v=jNQXAC9IVRw"   # Another test video
        ]
        
        for i, url in enumerate(test_urls, 1):
            logger.info(f"🧪 Testing YouTube access #{i}: {url}")
            
            try:
                with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                logger.info(f"✅ Test #{i} SUCCESS:")
                logger.info(f"   • Title: {info.get('title', 'Unknown')}")
                logger.info(f"   • Duration: {info.get('duration', 'Unknown')} seconds")
                logger.info(f"   • Uploader: {info.get('uploader', 'Unknown')}")
                return True
                
            except Exception as e:
                logger.error(f"❌ Test #{i} FAILED: {str(e)}")
                continue
        
        logger.error("❌ All YouTube access tests failed!")
        return False
    
    def download_video(self, url, max_quality=True):
        """Download a single video"""
        try:
            logger.info(f"📥 Starting download: {url}")
            
            # Configure yt-dlp options
            ydl_opts = {
                'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
                'format': 'best' if max_quality else 'worst',
                'noplaylist': True,
                'extractaudio': False,
                'writesubtitles': False,
                'writeautomaticsub': False,
                'ignoreerrors': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info first
                info = ydl.extract_info(url, download=False)
                
                logger.info(f"📹 Video Info:")
                logger.info(f"   • Title: {info.get('title', 'Unknown')}")
                logger.info(f"   • Duration: {info.get('duration', 'Unknown')} seconds")
                logger.info(f"   • Uploader: {info.get('uploader', 'Unknown')}")
                logger.info(f"   • View Count: {info.get('view_count', 'Unknown')}")
                
                # Download the video
                logger.info("🚀 Starting download...")
                ydl.download([url])
                
                # Find downloaded file
                for filename in os.listdir(self.download_dir):
                    if not filename.startswith('.'):
                        file_path = os.path.join(self.download_dir, filename)
                        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                        
                        logger.info(f"✅ Download SUCCESS:")
                        logger.info(f"   • File: {filename}")
                        logger.info(f"   • Size: {file_size:.2f} MB")
                        logger.info(f"   • Path: {file_path}")
                        
                        return file_path
                
                logger.error("❌ Downloaded file not found!")
                return None
                
        except Exception as e:
            logger.error(f"❌ Download failed: {str(e)}")
            return None
    
    def cleanup(self):
        """Clean up temporary files"""
        try:
            if os.path.exists(self.download_dir):
                shutil.rmtree(self.download_dir)
                logger.info(f"🗑️ Cleaned up: {self.download_dir}")
        except Exception as e:
            logger.warning(f"⚠️ Cleanup failed: {e}")

def main():
    """Main function"""
    logger.info("🚀 YouTube Downloader for Railway - Starting...")
    logger.info(f"🕐 Current time: {datetime.now()}")
    logger.info(f"🐍 Python version: {sys.version}")
    
    downloader = YouTubeDownloader()
    
    try:
        # Test YouTube access
        logger.info("🧪 Testing YouTube access from Railway...")
        if not downloader.test_youtube_access():
            logger.error("❌ Cannot access YouTube from this Railway instance!")
            logger.error("💡 Possible issues:")
            logger.error("   • IP blocked by YouTube")
            logger.error("   • Geographical restrictions")
            logger.error("   • Network configuration issues")
            return
        
        logger.info("✅ YouTube access confirmed!")
        
        # Test video URLs
        test_videos = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll
            "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # Another test
        ]
        
        for i, video_url in enumerate(test_videos, 1):
            logger.info(f"\n📺 DOWNLOADING VIDEO #{i}")
            logger.info(f"🔗 URL: {video_url}")
            
            downloaded_file = downloader.download_video(video_url)
            
            if downloaded_file:
                logger.info(f"✅ Video #{i} downloaded successfully!")
                
                # Clean up individual file to save space
                try:
                    os.remove(downloaded_file)
                    logger.info(f"🗑️ Cleaned up: {os.path.basename(downloaded_file)}")
                except:
                    pass
            else:
                logger.error(f"❌ Video #{i} download failed!")
            
            # Wait between downloads
            if i < len(test_videos):
                logger.info("⏳ Waiting 10 seconds before next download...")
                time.sleep(10)
        
        logger.info("🎉 All downloads completed!")
        
    except KeyboardInterrupt:
        logger.info("⚠️ Download interrupted by user")
    except Exception as e:
        logger.error(f"💥 Unexpected error: {str(e)}")
    finally:
        downloader.cleanup()
        logger.info("👋 YouTube Downloader finished!")

if __name__ == "__main__":
    main()
