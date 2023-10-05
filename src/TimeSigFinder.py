# 3 4  <- t
# 4 4
def __get_n_connected_notes(notes,t):
    
    count = 0
    for note in notes:
        start = note.start
        end = note.start + note.duration

    
        x = end - (start-(start % t))
        print(start,end,x)
        if x > t:
            count += 1

    return count

        


def guess_time_signature(notes):
    print("3/4:",__get_n_connected_notes(notes,3))
    print("4/4:",__get_n_connected_notes(notes,4))
    return
