# MY_CONSTANT
# my_function
# myValue
# MyClass

# __privateFunction
# _overridableFunction
if __name__ == "__main__":
    print("Initialising...")



# The first thing we do is load the config. Because we do this
# before initialising anything else, the global var CONFIG can
# just be imported directly by other scripts
try:
    import core.Configurator as cfg
    cfg.get_configuration()

    from core.Configurator import CONFIG, Modes, mode

    import cui.CUI as CUI

    import core.Utils as Utils

    import transcription.Transcriber as Transcriber
    import testing.Tester as Tester
    import network.Trainer as NetTrainer
    import network.TrainingDataProcessor as TrainingDataProcessor





except ModuleNotFoundError:
    from subprocess import Popen
    print("One or more module(s) were not found. Please see requirements.txt")
    print("or do you want to automatically install them? (yes/no)")
    x = input(">").lower()

    if x != 'y' and x != "yes":
        exit()
    print("Attempting to install dependencies...")
    Popen("pip install -r requirements.txt", shell=True).wait()
    exit()




def main() -> None:

    
    CUI.init()

    Utils.confirm_temp()

    if mode == Modes.PROCESS_TRAINING_DATA:
        print("Processing training data...")
        TrainingDataProcessor.process_single()
        return
    
    elif mode == Modes.PROCESS_MULTIPLE_TRAINING_DATA:
        print("Processing multiple training data files...")
        TrainingDataProcessor.process_multiple()
        return

    elif mode == Modes.TRAIN:
        print("Training network...")
        NetTrainer.train()
        return

    elif mode == Modes.TEST_MULTIPLE:
        print("Testing...")
        Tester.test()
        return


    # Standard mode.
    Transcriber.transcribe(CONFIG["ARGS"]["audio"])





    



if __name__ == "__main__":
    main()

