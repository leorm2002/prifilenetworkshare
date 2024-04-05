from pathlib import Path
import os
PW_FILE = "pw.txt"
def getPw():
    fi = os.path.join(Path.home(), PW_FILE)
    with open(fi, 'r') as file:
        content = file.read()
        content = content.strip("\n")
        content = content.strip("\t")
        content = content.strip("\r")
        content = content.strip(" ")

        return content
