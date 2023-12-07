import os


for file in os.listdir("MAESTRO"):
    split = file.split("ORIG_MID--")
    os.rename(f"MAESTRO\\{file}",split[1])