import sys
import os

# Add the backend directory to the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.detector import DeepfakeDetector

def main():
    print("Sherlock: Local Deepfake Detection Engine")
    print("=========================================")
    
    # Initialize Detector
    try:
        detector = DeepfakeDetector()
    except Exception as e:
        print(f"Failed to initialize detector: {e}")
        return

    while True:
        print("\nOptions:")
        print("1. Analyze a video")
        print("2. Exit")
        
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            video_path = input("Enter path to video file: ").strip()
            # Remove quotes if user copied path as "path"
            video_path = video_path.replace('"', '')
            
            if os.path.exists(video_path):
                print("\nAnalyzing... This may take a moment.")
                result = detector.analyze_video(video_path)
                
                print("\n--- Analysis Result ---")
                if "error" in result:
                    print(f"Error: {result['error']}")
                else:
                    status = "FAKE" if result['is_fake'] else "REAL"
                    color = "\033[91m" if result['is_fake'] else "\033[92m" # Red for Fake, Green for Real
                    reset = "\033[0m"
                    
                    print(f"Prediction: {color}{status}{reset}")
                    print(f"Combined Probability: {result['fake_probability']:.2%}")
                    print("Details:")
                    print(f"  - Visual Probability: {result['details']['visual_prob']:.2%}")
                    if result['details']['audio_prob'] is not None:
                        print(f"  - Audio Probability:  {result['details']['audio_prob']:.2%}")
                    else:
                        print("  - Audio Probability:  N/A (No audio detected)")
                    print(f"  - Frames Analyzed:    {result['details']['frames_analyzed']}")
                print("-----------------------")
            else:
                print("File not found.")
                
        elif choice == "2":
            print("Exiting.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
