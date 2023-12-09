# MY_CONSTANT
# my_function
# myValue
# MyClass

# __privateFunction
# _overridableFunction




try:
    # The first thing we do is load the config. Because we do this
    # before initialising anything else, the global var CONFIG can
    # just be imported directly by other scripts
    import core.Configurator as cfg
    cfg.get_configuration()


    
    import cui.CUI as CUI
    CUI.init()

    CUI.progress("Initialising",spin=True)



    from core.Configurator import CONFIG, Modes, mode
    import core.Utils as Utils

    import transcription.Transcriber as Transcriber
    import testing.Tester as Tester
    import network.Trainer as NetTrainer
    import network.TrainingDataProcessor as TrainingDataProcessor
    CUI.force_stop_progress()


except ModuleNotFoundError:
    CUI.force_stop_progress(succesful=False)

    from subprocess import Popen


    CUI.warning("One or more module(s) were not found. Please see requirements.txt")
    CUI.warning("or do you want to automatically install them? (yes/no)")


    if not CUI.yesno():
        exit()
    CUI.important("Attempting to install dependencies...")
    Popen("pip install -r requirements.txt", shell=True).wait()
    exit()




def main() -> None:
    
    Utils.confirm_temp() # Make sure temp folder exists

    if mode == Modes.PROCESS_TRAINING_DATA:
        CUI.important("Processing training data...")
        TrainingDataProcessor.process_single()
        return
    
    elif mode == Modes.PROCESS_MULTIPLE_TRAINING_DATA:
        CUI.important("Processing multiple training data files...")
        TrainingDataProcessor.process_multiple()
        return

    elif mode == Modes.TRAIN:
        CUI.important("Training network...")
        NetTrainer.train()
        return

    elif mode == Modes.TEST_MULTIPLE:
        CUI.important("Testing...")
        Tester.test()
        return

    
    # Standard mode.
    CUI.important("Generating sheet music...")
    Transcriber.transcribe(CONFIG["ARGS"]["audio"])





    



if __name__ == "__main__":
    main()
    CUI.notify()

