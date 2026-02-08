import torch
import torch.nn as nn
import numpy as np

class AudioModelService:
    def __init__(self, device: str = None):
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Initializing Audio Model on {self.device}...")
        
        # Simple CNN for Audio Classification (MFCC input)
        self.model = SimpleAudioCNN()
        self.model.to(self.device)
        self.model.eval()

    def predict_audio(self, mfcc_features: np.ndarray) -> float:
        """
        Returns probability of audio being FAKE (0.0 to 1.0)
        """
        if mfcc_features is None:
            return 0.5 # Uncertain

        with torch.no_grad():
            # Prepare tensor: (Batch, Channel, Height, Width) -> (1, 1, n_mfcc, time_steps)
            data = torch.from_numpy(mfcc_features).float().unsqueeze(0).unsqueeze(0).to(self.device)
            
            output = self.model(data)
            prob = torch.sigmoid(output).item()
            return prob

class SimpleAudioCNN(nn.Module):
    """
    A lightweight CNN to process MFCC spectrograms.
    """
    def __init__(self):
        super(SimpleAudioCNN, self).__init__()
        # Input shape: [1, 40, 157] approx for 5s audio at 16k sr
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        
        # Adaptive pool allows handling variable length audio to some extent
        self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc1 = nn.Linear(32, 128)
        self.fc2 = nn.Linear(128, 1)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = self.global_pool(x)
        x = x.view(x.size(0), -1) # Flatten
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x



