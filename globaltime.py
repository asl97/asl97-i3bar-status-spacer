import os.path
import pytz
import datetime
import configparser

def time():
    """
    Function to read, parse and output globaltimerc config
    
    return empty list if globaltimerc does not exists
    """
    o = []
    globaltimerc_path = os.path.expanduser("~")+"/.config/globaltime/globaltimerc"
    if os.path.exists(globaltimerc_path):
        # We re-parse the file in case it changes
        config = configparser.ConfigParser()
        config.read(globaltimerc_path)

        now = datetime.datetime.now(pytz.UTC)

        for s in config.sections():
            # Ignore the default values since we don't use it
            if s == "Default Values":
                continue
            o.append("{name}: {dt}".format(name=s, dt=now.astimezone(pytz.timezone(config[s]["tz"])).strftime("%H:%M")))

    return o
