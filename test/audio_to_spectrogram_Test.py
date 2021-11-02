from SmartGlovesProject.audio_to_spectrogram import Audio2Spectrogram


if __name__ == '__main__':
    # mp3_file = '../data/mp3/cls.mp3'
    wav_file = './test_resources/audio/test.wav'
    spec_file = './test_resources/spectrogram/test.jpg'
    audio2spectrogram = Audio2Spectrogram()
    # audio2spectrogram.audio_to_wav(mp3_file, wav_file)
    audio2spectrogram.wav_to_spectrogram(wav_file, './test_resources/spectrogram/test.jpg')
