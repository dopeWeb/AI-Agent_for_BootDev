import unittest
from functions.run_python_file import run_python_file

class TestRunPythonFile(unittest.TestCase):
    def test_run_python_file_cases(self):
        # Define the test cases as (Label for printing, Arguments)
        cases = [
            ("1. Standard run (Usage instructions)", 
             ("calculator", "main.py")),
            
            ("2. Run with arguments (3 + 5)", 
             ("calculator", "main.py", ["3 + 5"])),
            
            ("3. Run calculator tests", 
             ("calculator", "tests.py")),
            
            ("4. Error: Directory traversal", 
             ("calculator", "../main.py")),
            
            ("5. Error: Non-existent file", 
             ("calculator", "nonexistent.py")),
            
            ("6. Error: Not a Python file", 
             ("calculator", "lorem.txt")),
        ]

        print("\n" + "="*30)
        print("RUNNING SUBPROCESS TESTS")
        print("="*30)

        for label, args in cases:
            # Execute the function
            result = run_python_file(*args)
            
            # Print the result as required by the assignment
            print(f"\n--- {label} ---")
            print(result)

            # Assertions to ensure the logic matches the assignment requirements
            if label.startswith("1") or label.startswith("2"):
                self.assertIn("STDOUT:", result)
            
            elif "traversal" in label:
                self.assertIn("outside the permitted working directory", result)
                self.assertTrue(result.startswith("Error:"))

            elif "Non-existent" in label:
                self.assertIn("not found", result)
                self.assertTrue(result.startswith("Error:"))

            elif "Not a Python" in label:
                self.assertIn("is not a Python file", result)
                self.assertTrue(result.startswith("Error:"))

if __name__ == "__main__":
    unittest.main()