import subprocess
from subprocess import CREATE_NEW_CONSOLE
import time

i=0
with open("search.txt", "r") as a_file:
  for line in a_file:
    if i==0:
      i+=1
      continue
    stripped_line = line.strip()
    data = stripped_line.split(",")
    joined_string = " ".join(data)
    exe="py search.py "+joined_string
    subprocess.Popen(exe, creationflags=CREATE_NEW_CONSOLE)
    print(i,"Process Created")
    i+=1
time.sleep(5)