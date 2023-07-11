# MY_CONSTANT
# my_function
# myValue
# MyClass

# __privateFunction
# _overridableFunction


import Utils
import AudioProcessor
AUDIO_TO_ANALYSE = r"audio\PWS_TEST_2.wav"




def start():
    AudioProcessor.process_audio(AUDIO_TO_ANALYSE)


if __name__ == "__main__":
    start()

