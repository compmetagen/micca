import tempfile


def make_tempfile(dir):
    h = tempfile.NamedTemporaryFile(delete=False, prefix="tmp", dir=dir)
    h.close()
    return h.name
