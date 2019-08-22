import signal, sys
from snifferbot import *

def signalHandler(sig, frame):
    print("Exiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, signalHandler)

bot = snifferbot()
with open('token', 'r') as token:
    bot.run(token.read())
