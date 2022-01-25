import sys


def text(_file, content):
    _tagged("file", _file, file=sys.stderr, flush=True)
    if not content.strip():
        note("no visible text recognized")
    else:
        _tagged("text", flush=True)
        for line in content.splitlines():
            line = line.strip()
            if line:
                _tagged("text", "  " + line, flush=True)
        _tagged("text", flush=True)


def note(msg):
    _tagged("note", msg, file=sys.stderr, flush=True)


def warn(msg):
    _tagged("warn", msg, file=sys.stderr, flush=True)


def _tagged(tag, msg=None, **kwargs):
    if msg:
        print(tag + ":", msg, **kwargs)
    else:
        print(tag + ":", **kwargs)
