import json
import time
import sys

import spacer

# Send the header so that i3bar knows we want to use JSON:
print('{"version":1}')

# Begin the endless array.
print('[')

# We send an empty first array of blocks to make the loop simpler:
print('[],')

def bar(width):
    jout = []

    jout.append("spacer")
    jout.append({"full_text": "Centered"})
    jout.append("spacer")

    return spacer.expander(jout, width)

while True:
    print(json.dumps(bar(194)) + ",")
    sys.stdout.flush()
    time.sleep(1)

