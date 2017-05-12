import time
import psutil

def _parsesendrecv(interface, new, old):
    up = max(new[interface].bytes_sent - old[interface].bytes_sent, -1)
    down = max(new[interface].bytes_recv - old[interface].bytes_recv, -1)
    return up, down

class _netlink:
    def __init__(self):
        self.old = psutil.net_io_counters(pernic=True)
    def get_status(self, exclude=[]):
        new = psutil.net_io_counters(pernic=True)
        o = []
        with open("/proc/net/route") as f:
            route = f.read()
        for interface in new:
            if interface in exclude or interface not in route:
                continue
            up, down = _parsesendrecv(interface, new, self.old)
            if up == -1:
                sup = "?K"
            else:
                sup = "%.1fK" % (up/1024)
            if down == -1:
                sdown = "?K"
            else:
                sdown = "%.1fK" % (down/1024)
            o.append((interface, sup, sdown))
        self.old = new
        return o

netlink = _netlink().get_status

def cpu():
    return psutil.cpu_percent()

def ram():
    mem = psutil.virtual_memory()
    return ((mem.used+mem.buffers)/mem.total)*100

def datetime():
    return time.strftime("%a %d/%m/%Y %H:%M:%S")
