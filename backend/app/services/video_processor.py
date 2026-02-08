import cv2
import os
import numpy as np
from pathlib import Path
from typing import List, Optional

class VideoProcessor:
    def __init__(self, output_dir: str = "data/processed"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_frames(self, video_path: str, max_frames: int = 10) -> List[str]:
        """
        Extracts frames from a video file.
        
        Args:
            video_path: Path to the input video.
            max_frames: Maximum number of frames to extract (equally spaced).
            
        Returns:
            List of paths to saved frame images.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames <= 0:
            # Fallback if frame count cannot be determined
            frames = []
            success = True
            while success:
                success, frame = cap.read()
                if success:
                    frames.append(frame)
            total_frames = len(frames)
            # Re-open capture since we read it all
            cap.release()
            cap = cv2.VideoCapture(video_path)

        # Calculate indices for equally spaced frames
        indices = np.linspace(0, total_frames - 1, max_frames, dtype=int)
        
        saved_frame_paths = []
        current_frame = 0
        saved_count = 0

        while cap.isOpened() and saved_count < len(indices):
            success, frame = cap.read()
            if not success:
                break
            
            if current_frame in indices:
                frame_filename = f"frame_{current_frame}.jpg"
                save_path = self.output_dir / frame_filename
                cv2.imwrite(str(save_path), frame)
                saved_frame_paths.append(str(save_path))
                saved_count += 1
            
            current_frame += 1

        cap.release()
        return saved_frame_paths

    def get_video_metadata(self, video_path: str) -> dict:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return {}
            
        metadata = {
            "fps": cap.get(cv2.CAP_PROP_FPS),
            "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        }
        cap.release()
        return metadata

