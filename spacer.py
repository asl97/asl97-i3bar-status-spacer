# Some function to simplify/preprocess stuff
def intersperse(lst, item):
    """Insert item in between item in list, from http://stackoverflow.com/a/5921708/1986995"""
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

def expander(bar, width, separator="|"):
    """
    Expand 'spacer' item into white spaces to fill the bar
    
    Note: we use our own separators cause the width of i3bar separator is a PITA
    """
    # We starts with 0 length
    full = short = 0
    free = 0

    # Insert our own separator
    bar = intersperse(bar, {"full_text": separator})

    for i, item in enumerate(bar):
        if item == None: # Skip disabled separator
            continue
        if item == "spacer": # We disable our separator in between spacer
            # If both side are non-disable separators, we add one to the amount of free space
            # not quite sure how it works though.
            if i-1 > 0 and i+1 < len(bar):
                if bar[i-1] != None and bar[i+1] != None:
                    free += 1
            if i-1 > 0:
                bar[i-1] = None
            if i+1 < len(bar):
                bar[i+1] = None
            continue

        # Disable and remove i3bar separators
        item["separator"] = False
        item["separator_block_width"] = 0

        # min_width is always used if specified, see https://github.com/i3/i3/issues/2768
        reserve_space = item.get("min_width", 0)
        if isinstance(reserve_space, str):
            reserve_space = len(reserve_space)

        full_length = max(len(item["full_text"]), reserve_space)
        full += full_length
        if "short_text" not in item:
            short += full_length
        else:
            short += max(len(item["short_text"]), reserve_space)

    # Filtered out our disabled separator
    bar = [item for item in bar if item != None]

    # Assume program will be using short if full is longer than width
    if width > full:
        length = full
    elif width > short:
        length = short
    else: # Bar too long, filter out our spacer and return
        return [item for item in bar if item != "spacer"]

    # Work out spacers space
    # Currently it's implemented using same amount of space for all spacer
    # Might want to upgrade it to take account of item space so item stay in the same area
    # see baralignment.smart
    free_space = width - length + free
    num_of_spacer = bar.count("spacer")
    space_per_spacer = (free_space//num_of_spacer)
    left_over = free_space%num_of_spacer

    # We add left over spaces into each spacers
    spacer_index = 0
    for i, item in enumerate(bar):
        if item == "spacer":
            bar[i] = {"full_text":" "*(space_per_spacer+(1 if spacer_index<left_over else 0)), "separator":False, "separator_block_width":0}
            spacer_index += 1

    return bar

