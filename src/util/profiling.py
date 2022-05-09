import time


performances = {}


def timeit(name: str = None, print_each_call: bool = False):
    def timeit_decorator(method):
        def timed(*args, **kw):
            nonlocal name
            ts = time.time_ns()
            result = method(*args, **kw)
            te = time.time_ns()

            if name is None:
                name = kw.get("log_name", method.__name__.upper())

            delta = (te - ts) / 1e6
            if print_each_call:
                print("%r  %2.2f ms" % (name, delta))

            performances[name] = performances.get(name, 0) + delta
            return result

        return timed

    return timeit_decorator
