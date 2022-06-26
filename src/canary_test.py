import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self) -> None:
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
