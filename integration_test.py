import requests
import os
import cv2
import numpy as np
import sys
import time

# Configuration
EDGE_URL = "http://127.0.0.1:8787/api/v1/analyze"
API_KEY = "dev-secret-key"
TEST_VIDEO = "test_video.mp4"

def create_dummy_video(filename):
    """Creates a short 1-second dummy video for testing."""
    print(f"Generating dummy video: {filename}...")
    height, width = 480, 640
    fps = 30
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    
    for i in range(fps):
        # Create a frame with random noise/color to simulate content
        frame = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
        # Add some text
        cv2.putText(frame, f"Frame {i}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        out.write(frame)
    
    out.release()
    print("Video generated.")

def run_test():
    # 1. Ensure we have a video to test
    if not os.path.exists(TEST_VIDEO):
        try:
            create_dummy_video(TEST_VIDEO)
        except Exception as e:
            print(f"Error creating dummy video: {e}")
            print("Please ensure opencv-python is installed or provide a 'test_video.mp4' file.")
            return

    # 2. Prepare Request
    print(f"\nSending request to Edge Gateway: {EDGE_URL}")
    print(f"Using API Key: {API_KEY}")
    
    headers = {
        "X-API-KEY": API_KEY
    }
    
    files = {
        "file": (TEST_VIDEO, open(TEST_VIDEO, "rb"), "video/mp4")
    }

    try:
        start_time = time.time()
        response = requests.post(EDGE_URL, headers=headers, files=files)
        elapsed = time.time() - start_time
        
        print(f"\nResponse received in {elapsed:.2f}s")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("Success! Response JSON:")
            print(response.json())
        else:
            print("Request failed.")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("\nConnection Error!")
        print("Ensure both the Backend (port 8000) and Edge Worker (port 8787) are running.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_test()



