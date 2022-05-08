import time


def timeit(method):
    def timed(*args, **kw):
        ts = time.time_ns()
        result = method(*args, **kw)
        te = time.time_ns()
        if "log_time" in kw:
            name = kw.get("log_name", method.__name__.upper())
            kw["log_time"][name] = int((te - ts) / 1e6)
        else:
            print("%r  %2.2f ms" % (method.__name__, (te - ts) / 1e6))
        return result

    return timed
