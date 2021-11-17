import librosa
import numpy as np
from SmartGlovesProject_Server.Util.sigmoidlize import sigmoidlize


def to_frames(y, sr):
    """Framing the sample,at hop_length=512, frame_length=2048

    Argument:
        - y: samples
        - sr: sample rate
    Return:
        - frames_sig: mean of each frames, sigmoid normalized to [-1,1], and time_per_frame: time per frame in seconds
    """
    frames = librosa.util.frame(x=y, hop_length=512, axis=0, frame_length=2048)
    frames_mean = np.mean(frames, axis=1)
    frames_sig = sigmoidlize(frames_mean)
    time_per_frame = (1 / sr) * 512
    return frames_sig, time_per_frame
