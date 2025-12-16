import unittest
from functions.write_file import write_file


class TestWriteFile(unittest.TestCase):
    def test_write_cases_print_outputs(self):
        cases = [
            ('write_file("calculator", "lorem.txt", "wait, this isn\'t lorem ipsum")',
             ("calculator", "lorem.txt", "wait, this isn't lorem ipsum")),
            ('write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")',
             ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")),
            ('write_file("calculator", "/tmp/temp.txt", "this should not be allowed")',
             ("calculator", "/tmp/temp.txt", "this should not be allowed")),
        ]

        outputs = []
        for label, args in cases:
            out = write_file(*args)
            outputs.append(out)
            print("\n---", label, "---")
            print(out)

        # ✅ Assertions (so it's an actual test)
        self.assertTrue(outputs[0].startswith("Successfully wrote to"), msg=outputs[0])
        self.assertTrue(outputs[1].startswith("Successfully wrote to"), msg=outputs[1])
        self.assertTrue(outputs[2].startswith("Error:"), msg=outputs[2])


if __name__ == "__main__":
    unittest.main()
