from typing import Dict, Any
import os
from app.services.video_processor import VideoProcessor
from app.services.audio_processor import AudioProcessor
from app.services.model_service import ModelService
from app.services.audio_model_service import AudioModelService

class DeepfakeDetector:
    def __init__(self):
        self.video_processor = VideoProcessor()
        self.audio_processor = AudioProcessor()
        self.visual_model = ModelService()
        self.audio_model = AudioModelService()

    def analyze_video(self, video_path: str) -> Dict[str, Any]:
        """
        Orchestrates the analysis process:
        1. Visual Analysis (Frames -> EfficientNet)
        2. Audio Analysis (Wav -> MFCC -> CNN)
        3. Fusion
        """
        print(f"Starting multi-modal analysis for: {video_path}")
        
        # --- 1. Visual Analysis ---
        visual_prob = 0.0
        visual_confidence = 0.0
        frames_extracted = 0
        
        try:
            frames = self.video_processor.extract_frames(video_path, max_frames=20)
            frames_extracted = len(frames)
            if frames:
                visual_prob = self.visual_model.predict_frames(frames)
                visual_confidence = visual_prob if visual_prob > 0.5 else (1 - visual_prob)
                print(f"Visual Probability: {visual_prob:.4f}")
        except Exception as e:
            print(f"Visual analysis error: {e}")

        # --- 2. Audio Analysis ---
        audio_prob = 0.0
        audio_confidence = 0.0
        has_audio = False
        
        try:
            audio_path = self.audio_processor.extract_audio(video_path)
            if audio_path:
                has_audio = True
                mfcc = self.audio_processor.get_mfcc(audio_path)
                if mfcc is not None:
                    audio_prob = self.audio_model.predict_audio(mfcc)
                    audio_confidence = audio_prob if audio_prob > 0.5 else (1 - audio_prob)
                    print(f"Audio Probability: {audio_prob:.4f}")
        except Exception as e:
            print(f"Audio analysis error: {e}")

        # --- 3. Fusion Logic ---
        # Weighted average: Visuals usually carry more weight unless audio is very confident
        # If no audio, rely 100% on visual
        
        if has_audio:
            # Simple fusion: 60% Visual, 40% Audio
            combined_prob = (visual_prob * 0.6) + (audio_prob * 0.4)
        else:
            combined_prob = visual_prob

        is_fake = combined_prob > 0.5
        final_confidence = combined_prob if is_fake else (1 - combined_prob)

        result = {
            "file": os.path.basename(video_path),
            "is_fake": is_fake,
            "fake_probability": round(combined_prob, 4),
            "confidence": round(final_confidence, 4),
            "details": {
                "visual_prob": round(visual_prob, 4),
                "audio_prob": round(audio_prob, 4) if has_audio else None,
                "frames_analyzed": frames_extracted,
                "has_audio": has_audio
            }
        }
        
        return result

