import unittest
from multiprocessing import Process
from pledge import pledge


def victim(permissions, callback):
    pledge(permissions)

    if callback:
        callback()

    while True:
        pass


def survive(permissions, callback):
    killed = True
    p = Process(target=victim, args=(permissions, callback))
    p.start()
    p.join(0.5)

    if p.is_alive():
        killed = False
        p.terminate()

    return killed


class TestPledge(unittest.TestCase):

    def test_invalid(self):
        r = pledge("INVALID ARGS")
        self.assertLess(r, 0)

    def test_nokill(self):
        r = survive("", None)
        self.assertFalse(r)

    def test_kill(self):

        def f():
            print('KILL ME')

        r = survive("", f)
        self.assertTrue(r)


if __name__ == '__main__':
    unittest.main()
