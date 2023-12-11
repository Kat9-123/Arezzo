import cui.CUI as CUI


def __get_n_tied_notes(notes,t):
    
    count = 0
    for note in notes:
        start = note.start
        end = note.start + note.duration

    
        x = end - (start-(start % t))
        if x > t:
            count += 1

    return count

        

TIME_SIGS = ["4/4","3/4","2/4"]

def guess_time_signature(notes) -> str:
    twoFour = __get_n_tied_notes(notes,2)
    threeFour = __get_n_tied_notes(notes,3)
    fourFour =__get_n_tied_notes(notes,4)

    CUI.diagnostic("2/4 score", twoFour)
    CUI.diagnostic("3/4 score",threeFour)
    CUI.diagnostic("4/4 score",fourFour)

    

    # Find the lowest num of tied notes,
    # prioritising left to right if they are equal.
    x = [fourFour,threeFour,twoFour]
    timeSig = TIME_SIGS[x.index(min(x))]

    CUI.important(f"Time signature: {timeSig}")

    return timeSig
