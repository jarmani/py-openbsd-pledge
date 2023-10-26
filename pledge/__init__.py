import ctypes
import enum
import os
from pathlib import Path
from typing import Optional, Union

_pledge = None
try:
    _pledge = ctypes.CDLL(None, use_errno=True).pledge
    _pledge.restype = ctypes.c_int
    _pledge.argtypes = ctypes.c_char_p, ctypes.c_char_p
except Exception:
    pass


class Promise(enum.Flag):
    stdio = enum.auto()
    rpath = enum.auto()
    wpath = enum.auto()
    cpath = enum.auto()
    dpath = enum.auto()
    tmppath = enum.auto()
    inet = enum.auto()
    mcast = enum.auto()
    fattr = enum.auto()
    chown = enum.auto()
    flock = enum.auto()
    unix = enum.auto()
    dns = enum.auto()
    getpw = enum.auto()
    sendfd = enum.auto()
    recvfd = enum.auto()
    tape = enum.auto()
    tty = enum.auto()
    proc = enum.auto()
    exec = enum.auto()
    prot_exec = enum.auto()
    settime = enum.auto()
    ps = enum.auto()
    vminfo = enum.auto()
    id = enum.auto()
    pf = enum.auto()
    route = enum.auto()
    wroute = enum.auto()
    audio = enum.auto()
    video = enum.auto()
    bpf = enum.auto()
    unveil = enum.auto()
    error = enum.auto()
    disklabel = enum.auto()
    drm = enum.auto()
    vmm = enum.auto()

    def __str__(self) -> str:
        return " ".join(x.name for x in Promise if x.value & self.value)


def pledge(
    promises: Optional[Union[Promise, str]] = None,
    execpromises: Optional[Union[Promise, str]] = None,
):
    if not _pledge:
        raise OSError("Plegde is unsupported on your system")

    if isinstance(promises, str):
        promises = promises.encode()
    if isinstance(execpromises, str):
        execpromises = execpromises.encode()

    r = _pledge(promises, execpromises)
    if r == -1:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))


_unveil = None
try:
    _unveil = ctypes.CDLL(None, use_errno=True).unveil
    _unveil.restype = ctypes.c_int
    _unveil.argtypes = ctypes.c_char_p, ctypes.c_char_p
except Exception:
    pass


def unveil(path: Union[Path, bytes, str], permissions: Optional[str] = None):
    if not _unveil:
        raise OSError("unveil is unsupported on your system")

    if isinstance(path, str):
        path = path.encode()
    elif isinstance(path, Path):
        path = bytes(path)

    r = _unveil(path, permissions)
    if r == -1:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))
