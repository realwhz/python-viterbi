import unittest
import tailbiting

class TailBitingTest(unittest.TestCase):
    def TestEncoder(self):
        codec = tailbiting.codec(7, 3, [[1, 0, 1, 1, 0, 1, 1], [1, 1, 1, 1, 0, 0, 1], [1, 1, 1, 0, 1, 0, 1]])
        input = [0, 1, 0, 0, 0, 1, 0, 0]
        output = codec.encode(input)
        expected = [0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0]
        self.failUnless(output == expected)

    def TestDecoder(self):
        output = [0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0]
        output = [1.0-2.0*x for x in output]
        decoded = codec.decode(output)
        expected = [0, 1, 0, 0, 0, 1, 0, 0]
        self.failUnless(decoded == expected)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
