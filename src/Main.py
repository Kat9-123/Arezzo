# MY_CONSTANT
# my_function
# myValue
# MyClass

# __privateFunction
# _overridableFunction


import Utils
import AudioProcessor
AUDIO_TO_ANALYSE = r"PWS_TEST_0.wav"


AUDIO_BASE_PATH = "audio"

def start():
    AudioProcessor.process_audio("{}\\{}...".format(AUDIO_BASE_PATH,AUDIO_TO_ANALYSE))


if __name__ == "__main__":
    start()

