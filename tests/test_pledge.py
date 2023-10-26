import signal
import subprocess
import sys
import unittest

from pledge import pledge, Promise


def generate_python_code(promises=None, execpromises=None):
    """
    Prevent the process core dump by setting size limit to 0.
    It increases the speed of tests and prevent poluting the current directory.
    See https://man.openbsd.org/getrlimit.2#RLIMIT_CORE
    """
    code = "import resource; resource.setrlimit(resource.RLIMIT_CORE, (0, 0));"
    code += f"from pledge import pledge; pledge({promises!r}, {execpromises!r});"

    return code


def run_inline_python(code):
    return subprocess.run([sys.executable, "-c", code], stdout=subprocess.DEVNULL)


class TestPledge(unittest.TestCase):
    def test_promises(self):
        self.assertEqual(
            str(Promise.stdio | Promise.rpath | Promise.tmppath), "stdio rpath tmppath"
        )

    def test_promises_dedup(self):
        self.assertEqual(
            str(
                Promise.tmppath
                | Promise.stdio
                | Promise.rpath
                | Promise.stdio
                | Promise.tmppath
            ),
            "stdio rpath tmppath",
        )

    def test_invalid(self):
        with self.assertRaises(OSError):
            pledge("INVALID ARGS")

    def test_nokill(self):
        code = generate_python_code(promises="stdio")
        result = run_inline_python(code + 'print("test")')
        self.assertNotEqual(result.returncode, -signal.SIGABRT)

    def test_kill(self):
        code = generate_python_code(promises="")
        result = run_inline_python(code + 'print("test")')
        self.assertEqual(result.returncode, -signal.SIGABRT)

    def test_tmppath_nokill(self):
        code = "import tempfile;"
        code += generate_python_code(promises="stdio rpath tmppath")
        code += (
            "tmp = tempfile.TemporaryFile();" + 'tmp.write(b"test");' + "tmp.close()"
        )
        result = run_inline_python(code)
        self.assertNotEqual(result.returncode, -signal.SIGABRT)

    def test_tmppath_kill(self):
        code = "import tempfile;"
        code += generate_python_code(promises="")
        code += (
            "tmp = tempfile.TemporaryFile();" + 'tmp.write(b"test");' + "tmp.close()"
        )
        result = run_inline_python(code)
        self.assertEqual(result.returncode, -signal.SIGABRT)


if __name__ == "__main__":
    unittest.main()
