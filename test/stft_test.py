import pickle

from SmartGlovesProject_Server.short_time_fourier_trans import STFTer

if __name__ == '__main__':
    '''
    @version 1.0 
    '''
    wav_music_file = "./test_resources/audio/LightYourStory.wav"
    # spec_transformer.audio_to_wav(mp3_music_file, wav_music_file)
    stfter = STFTer()
    stfter.fourier_trans(wav_music_file, offset=30.0, duration=30.0)
