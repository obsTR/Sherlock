import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import os
from typing import List, Dict

class ModelService:
    def __init__(self, model_name: str = "efficientnet_b0", device: str = None):
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Loading model {model_name} on {self.device}...")
        
        # Load a pre-trained EfficientNet model
        # In a real deepfake scenario, we would load a model fine-tuned on DFDC or FaceForensics++
        # For now, we use ImageNet weights to establish the pipeline.
        try:
            weights = models.EfficientNet_B0_Weights.DEFAULT
            self.model = models.efficientnet_b0(weights=weights)
            
            # Modify the classifier for binary classification (Real vs Fake)
            # EfficientNet B0's last layer is 'classifier' -> Sequential -> Linear
            # The input features for the last linear layer in B0 is 1280
            in_features = self.model.classifier[1].in_features
            self.model.classifier[1] = nn.Linear(in_features, 1)
            
            self.model.to(self.device)
            self.model.eval() # Set to inference mode
            
            # Standard ImageNet normalization
            self.transform = weights.transforms()
            
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def predict_frames(self, frame_paths: List[str]) -> float:
        """
        Predicts the probability of the video being FAKE based on extracted frames.
        Returns an average probability (0.0 = Real, 1.0 = Fake).
        """
        if not frame_paths:
            return 0.0

        probs = []
        
        with torch.no_grad():
            for frame_path in frame_paths:
                if not os.path.exists(frame_path):
                    continue
                
                # Load and preprocess image
                try:
                    img = Image.open(frame_path).convert('RGB')
                    img_t = self.transform(img).unsqueeze(0).to(self.device)
                    
                    # Forward pass
                    output = self.model(img_t)
                    
                    # Sigmoid to get probability between 0 and 1
                    prob = torch.sigmoid(output).item()
                    probs.append(prob)
                except Exception as e:
                    print(f"Error processing frame {frame_path}: {e}")

        if not probs:
            return 0.0

        # Simple averaging strategy for now
        # In production, we might use max() or a temporal model (LSTM)
        avg_prob = sum(probs) / len(probs)
        return avg_prob



