item_set = [
 ["item", "lol", "wat", "lol", "really longest item"],
 ["really longest item", "lol", "wat", "lol", "item"],
]

def dumb(items, free):
    return (" "*(free//(len(items)-1))).join(items)

def smart(items, free):
    total = sum(map(len, items)) + free
    tml = total - len(items[-1])
    num_of_spacer = len(items) -1
    avg_per_spacer = total/num_of_spacer
    overflow = 0
    o = []
    for item in items[:-1]:
        if (overflow+len(item)) > avg_per_spacer:
            overflow = avg_per_spacer-(overflow+len(item))
        o.append(("{:<%d}"%avg_per_spacer).format(item))
    #o.append(items[-1])

    # todo, warning hack to add last item
    # if len of item is longer than avg_per_spacer, it override the second last stuff
    return "".join(o)[:-len(items[-1])] + items[-1]

for items in item_set:
    print("-"*20)
    print(dumb(items, 60))
    print(smart(items, 60))
    print("-"*20)
