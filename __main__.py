import json
import time
import sys

import globaltime
import systemstat
import spacer

# Send the header so that i3bar knows we want to use JSON:
print('{"version":1}')

# Begin the endless array.
print('[')

# We send an empty first array of blocks to make the loop simpler:
print('[],')

# Some function to simplify/preprocess stuff
# numbers and color code from a conky script somewhere
def color(num):
    if num > 75:
        return "\#cf6a4c"
    elif num >50:
        return "\#ffd75f"
    else:
        return "\#87af5f"

def bar(width):
    jout = []
    # read globaltime config
    for t in globaltime.time():
        jout.append({"full_text": t})
    # expanding spacer
    jout.append("spacer")
    # active network link speed monitor
    for interface, sup, sdown in systemstat.netlink(exclude={'lo'}):
        iud = "{sup}/{sdown} (%s)".format(sup=sup, sdown=sdown)
        jout.append({"full_text": iud%interface, "short_text": iud%interface[0], "align": "center"})

    # cpu usage percentage
    cpu = systemstat.cpu()
    jout.append({"full_text": "Cpu: %d%%" % cpu, "color": color(cpu), "min_width": "Cpu: 100%", "align": "center"})
    # ram + buffer usage percentage
    ram = systemstat.ram()
    jout.append({"full_text": "Ram: %d%%" % ram, "color": color(ram), "min_width": "Ram: 100%", "align": "center"})
    # date time
    jout.append({"full_text": systemstat.datetime()})

    return spacer.expander(jout, width)

# just a simple function to join the full_text from bar
def bartext(width):
    return "".join([item["full_text"] for item in bar(width) if isinstance(item, dict) and "full_text" in item])

# Now send blocks with information forever:
# todo, find out width somehow, manual way:
#print(json.dumps([{"full_text": 'y'+'|'*193}])+",") #means 194 as width
#input()

while True:
    print(json.dumps(bar(194)) + ",")
    #print(bartext(194))
    sys.stdout.flush()
    time.sleep(1)

