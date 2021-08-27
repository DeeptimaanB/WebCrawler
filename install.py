  
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("beautifulsoup4")
install("pygooglenews")
install("feedparser==6.0")