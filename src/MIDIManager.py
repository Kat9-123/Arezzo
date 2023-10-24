import pretty_midi


def get_midi(path):
    midi_data = pretty_midi.PrettyMIDI(path)

    for instrument in midi_data.instruments:
        return instrument.notes
