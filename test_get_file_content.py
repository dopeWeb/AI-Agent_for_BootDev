import unittest
from config import MAX_FILE_CHARS
from functions.get_file_content import get_file_content


class TestGetFileContent(unittest.TestCase):
    def test_lorem_truncates(self):
        result = get_file_content("calculator", "lorem.txt")

        # Should not be an error
        self.assertFalse(result.startswith("Error:"), msg=result)

        expected_suffix = f'[...File "lorem.txt" truncated at {MAX_FILE_CHARS} characters]'
        self.assertTrue(
            result.endswith(expected_suffix),
            msg="Truncation suffix missing / incorrect",
        )

        # total length should be MAX_FILE_CHARS + len(suffix)
        self.assertEqual(len(result), MAX_FILE_CHARS + len(expected_suffix))

    def test_other_cases_print_outputs(self):
        cases = [
            ('get_file_content("calculator", "main.py")', ("calculator", "main.py")),
            (
                'get_file_content("calculator", "pkg/calculator.py")',
                ("calculator", "pkg/calculator.py"),
            ),
            ('get_file_content("calculator", "/bin/cat")', ("calculator", "/bin/cat")),
            (
                'get_file_content("calculator", "pkg/does_not_exist.py")',
                ("calculator", "pkg/does_not_exist.py"),
            ),
        ]

        for label, args in cases:
            out = get_file_content(*args)
            print("\n---", label, "---")
            print(out)

        # Enforce the two error cases are errors:
        self.assertTrue(
            get_file_content("calculator", "/bin/cat").startswith("Error:"),
            msg="Expected /bin/cat to be rejected as outside working dir",
        )
        self.assertTrue(
            get_file_content("calculator", "pkg/does_not_exist.py").startswith("Error:"),
            msg="Expected missing file to return Error:",
        )


if __name__ == "__main__":
    unittest.main()

