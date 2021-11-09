from SmartGlovesProject_Server.beat_tracker import BeatTracker

if __name__ == '__main__':
    bt = BeatTracker()
    beats = BeatTracker.get_beats("./test_resources/audio/test.wav")
    print(beats)
