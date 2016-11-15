
def parse_int(str, on_exception=0, raise_exception=False):
    try:
        return int(str)
    except Exception, e:
        if raise_exception:
            raise e
        return on_exception
