from SmartGlovesProject import predictor as pred

if __name__ == '__main__':
    predictor = pred.Predictor("./resources/Resnet_SGD_valscore_60.pt")
    # audio_2_spec = spec_utils.Audio2Spectrogram()
    # wav_file_path = "./test_resources/audio/test.wav"
    spec_file_path = "./test_resources/spectrogram/test.jpg"
    # audio_2_spec.wav_to_spectrogram(src=wav_file_path, dest=spec_file_path)
    print(f"--------complete-----------")
    mood_class, prob = predictor.predict(img_path=spec_file_path)
    print(mood_class)
    print(prob)
    for i in range(1, 5):
        spec_file_path = f"./test_resources/spectrogram/test{i}.jpg"
        mood_class, prob = predictor.predict(img_path=spec_file_path)
        print(f"-------{i}--------")
        print(mood_class)
        print(prob)
