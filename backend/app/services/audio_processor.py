import librosa
import numpy as np
import os
import subprocess
from pathlib import Path
from typing import Optional

class AudioProcessor:
    def __init__(self, output_dir: str = "data/processed_audio"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_audio(self, video_path: str) -> Optional[str]:
        """
        Extracts audio from video file using ffmpeg (via subprocess or librosa if supported).
        Returns path to the saved .wav file.
        """
        if not os.path.exists(video_path):
            return None

        video_filename = os.path.basename(video_path)
        audio_filename = f"{os.path.splitext(video_filename)[0]}.wav"
        save_path = self.output_dir / audio_filename

        # If audio already exists, return it
        if save_path.exists():
            return str(save_path)

        # Use ffmpeg to extract audio
        # Note: Requires ffmpeg to be installed on the system
        try:
            command = [
                "ffmpeg",
                "-i", video_path,
                "-ab", "160k",
                "-ac", "1", # Mono
                "-ar", "16000", # 16kHz
                "-vn", # No video
                "-y", # Overwrite
                str(save_path)
            ]
            # Run quietly
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            
            if save_path.exists():
                return str(save_path)
        except Exception as e:
            print(f"FFmpeg extraction failed: {e}. Attempting librosa fallback...")
            pass

        return None

    def get_mfcc(self, audio_path: str, n_mfcc: int = 40, duration: int = 5):
        """
        Loads audio and computes MFCC features.
        """
        try:
            # Load up to 'duration' seconds
            y, sr = librosa.load(audio_path, duration=duration, sr=16000)
            
            # If audio is too short, pad it
            target_len = duration * sr
            if len(y) < target_len:
                y = np.pad(y, (0, target_len - len(y)))
            else:
                y = y[:target_len]

            # Compute MFCC
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
            return mfcc
        except Exception as e:
            print(f"Error computing MFCC: {e}")
            return None



