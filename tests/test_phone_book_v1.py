import contextlib
import io
import unittest
from unittest.mock import patch

from src.phone_book_v1 import main


def f(lines):
    return '\n'.join(lines)


def s(text):
    return text.split('\n')


class TestPhoneBookV1(unittest.TestCase):
    """main() drives an interactive phone book: 1 search, 2 add, 3 quit."""

    def run_program(self, inputs, stop_msg):
        """Run main() with the given canned inputs and capture everything it
        prints. A sentinel AssertionError is appended to the input
        side_effect, so if the program asks for more input than the test
        supplies (e.g. it never reaches its "quit" branch), that surfaces
        as a clear test failure instead of the mock raising StopIteration.
        """
        buf = io.StringIO()
        side_effect = list(inputs) + [AssertionError("Input is asked too many times.")]
        with patch('builtins.input', side_effect=side_effect):
            try:
                with contextlib.redirect_stdout(buf):
                    main()
            except Exception:
                self.fail(stop_msg)
        return buf.getvalue()

    def test_1_program_stops(self):
        words = s("3")
        output_all = self.run_program(
            words,
            f"Make sure that the program stops with the input\n{f(words)}")
        self.assertIn(
            "quitting...", output_all,
            msg="The program should print 'quitting...' when it receives "
                "command 3.")

    def test_2_not_added_is_not_found(self):
        test_input = "1\nmary\n3"
        words = s(test_input)
        output_all = self.run_program(
            words,
            f"Make sure that the program stops with the input\n{f(words)}")

        exp = "no number\nquitting..."
        exp_words = exp.split('\n')

        message = ("\nPlease note, that in this exercise, no code should be "
                    "included inside\nif __name__ == \"__main__\":\nblock\n")

        self.assertTrue(
            len(output_all) > 0,
            msg=f"Your program does not print out anything with the input\n"
                f"{f(words)}\n{message}")
        output = [line.strip() for line in output_all.split("\n") if len(line) > 0]
        self.assertEqual(
            len(exp_words), len(output),
            msg=f"Instead of {len(exp_words)} rows, your program prints out "
                f"{len(output)} rows:\n{output_all}\nwith the input:\n"
                f"{f(words)}\nexpected print out is\n{exp}")
        for i in range(len(exp_words)):
            e = exp_words[i]
            line = output[i]
            self.assertEqual(
                line, e,
                msg=f"Your program is not working correctly with the input\n"
                    f"{f(words)}\nprint out on row {i + 1} is incorrect, it "
                    f"should be\n{e}\nbut it is\n{line}\nThe whole print out "
                    f"is:\n{output_all}\nThe expected print out is\n{exp}")

    def test_3_added_is_found(self):
        test_input = "2\nmary\n040-234567\n1\nmary\n3"
        words = s(test_input)
        output_all = self.run_program(
            words,
            f"Make sure that the program stops with the input\n{f(words)}")

        exp = "ok!\n040-234567\nquitting..."
        exp_words = exp.split('\n')

        self.assertTrue(
            len(output_all) > 0,
            msg=f"Your program does not print out anything with the input\n"
                f"{f(words)}")
        output = [line.strip() for line in output_all.split("\n") if len(line) > 0]
        self.assertEqual(
            len(exp_words), len(output),
            msg=f"Instead of {len(exp_words)} rows, your program prints out "
                f"{len(output)} rows:\n{output_all}\nwith the input:\n"
                f"{f(words)}\nexpected print out is\n{exp}")
        for i in range(len(exp_words)):
            e = exp_words[i]
            line = output[i]
            self.assertEqual(
                line, e,
                msg=f"Your program is not working correctly with the input\n"
                    f"{f(words)}\nprint out on row {i + 1} is incorrect, it "
                    f"should be\n{e}\nbut it is\n{line}\nThe whole print out "
                    f"is:\n{output_all}\nThe expected print out is\n{exp}")

    def test_4_old_is_replaced(self):
        test_input = "2\nmary\n040-234567\n2\nmary\n09-334455\n1\nmary\n3"
        words = s(test_input)
        output_all = self.run_program(
            words,
            f"Make sure that the program stops with the input\n{f(words)}")

        exp = "ok!\nok!\n09-334455\nquitting..."
        exp_words = exp.split('\n')

        self.assertTrue(
            len(output_all) > 0,
            msg=f"Your program does not print out anything with the input\n"
                f"{f(words)}")
        output = [line.strip() for line in output_all.split("\n") if len(line) > 0]
        self.assertEqual(
            len(exp_words), len(output),
            msg=f"Instead of {len(exp_words)} rows, your program prints out "
                f"{len(output)} rows:\n{output_all}\nwith the input:\n"
                f"{f(words)}\nexpected print out is\n{exp}")
        for i in range(len(exp_words)):
            e = exp_words[i]
            line = output[i]
            self.assertEqual(
                line, e,
                msg=f"Your program is not working correctly with the input\n"
                    f"{f(words)}\nprint out on row {i + 1} is incorrect, it "
                    f"should be\n{e}\nbut it is\n{line}\nThe whole print out "
                    f"is:\n{output_all}\nThe expected print out is\n{exp}")

    def test_5_many_commands(self):
        test_input = ("2\nmike\n040-234567\n2\nmary\n09-334455\n1\nmary\n"
                       "1\nmike\n1\nbecky\n2\nmike\n045-554433\n1\nmike\n3")
        words = s(test_input)
        output_all = self.run_program(
            words,
            f"Make sure that the program stops with the input\n{f(words)}")

        exp = ("ok!\nok!\n09-334455\n040-234567\nno number\nok!\n"
               "045-554433\nquitting...")
        exp_words = exp.split('\n')

        self.assertTrue(
            len(output_all) > 0,
            msg=f"Your program does not print out anything with the input\n"
                f"{f(words)}")
        output = [line.strip() for line in output_all.split("\n") if len(line) > 0]
        self.assertEqual(
            len(exp_words), len(output),
            msg=f"Instead of {len(exp_words)} rows, your program prints out "
                f"{len(output)} rows:\n{output_all}\nwith the input:\n"
                f"{f(words)}\nexpected print out is\n{exp}")
        for i in range(len(exp_words)):
            e = exp_words[i]
            line = output[i]
            self.assertEqual(
                line, e,
                msg=f"Your program is not working correctly with the input\n"
                    f"{f(words)}\nprint out on row {i + 1} is incorrect, it "
                    f"should be\n{e}\nbut it is\n{line}\nThe whole print out "
                    f"is:\n{output_all}\nThe expected print out is\n{exp}")

    def test_6_many_commands(self):
        test_input = ("2\njack\n040-1212334\n2\nwendy\n09-334455\n2\n"
                       "william\n050-2255433\n1\nmary\n1\nwendy\n1\nwilliam\n"
                       "2\njack\n045-554433\n1\njack\n3")
        words = s(test_input)
        output_all = self.run_program(
            words,
            f"Make sure that the program stops with the input\n{f(words)}")

        exp = ("ok!\nok!\nok!\nno number\n09-334455\n050-2255433\nok!\n"
               "045-554433\nquitting...")
        exp_words = exp.split('\n')

        self.assertTrue(
            len(output_all) > 0,
            msg=f"Your program does not print out anything with the input\n"
                f"{f(words)}")
        output = [line.strip() for line in output_all.split("\n") if len(line) > 0]
        self.assertEqual(
            len(exp_words), len(output),
            msg=f"Instead of {len(exp_words)} rows, your program prints out "
                f"{len(output)} rows:\n{output_all}\nwith the input:\n"
                f"{f(words)}\nexpected print out is\n{exp}")
        for i in range(len(exp_words)):
            e = exp_words[i]
            line = output[i]
            self.assertEqual(
                line, e,
                msg=f"Your program is not working correctly with the input\n"
                    f"{f(words)}\nprint out on row {i + 1} is incorrect, it "
                    f"should be\n{e}\nbut it is\n{line}\nThe whole print out "
                    f"is:\n{output_all}\nThe expected print out is\n{exp}")


if __name__ == '__main__':
    unittest.main()
