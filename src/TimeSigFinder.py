import cui.CUI as CUI
# 3 4  <- t
# 4 4
def __get_n_connected_notes(notes,t):
    
    count = 0
    for note in notes:
        start = note.start
        end = note.start + note.duration

    
        x = end - (start-(start % t))
        if x > t:
            count += 1

    return count

        


def guess_time_signature(notes):
    twoFour = __get_n_connected_notes(notes,2)
    threeFour = __get_n_connected_notes(notes,3)
    fourFour =__get_n_connected_notes(notes,4)

    CUI.diagnostic("2/4 score", twoFour)
    CUI.diagnostic("3/4 score",threeFour)
    CUI.diagnostic("4/4 score",fourFour)

    if threeFour == fourFour:
        CUI.warning("Scores are equal, guessing 4/4")

    return
