import io
import unittest

from numfmt_cli.cli import main


class TestCli(unittest.TestCase):
    def test_bare_number_formats_to_human(self) -> None:
        out = io.StringIO()
        code = main(["1234567"], out=out)
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue().strip(), "1.2M")

    def test_suffixed_number_parses_to_integer(self) -> None:
        out = io.StringIO()
        code = main(["1.2M"], out=out)
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue().strip(), "1200000")

    def test_precision_flag(self) -> None:
        out = io.StringIO()
        code = main(["1234567", "--precision", "3"], out=out)
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue().strip(), "1.235M")

    def test_negative_bare_number(self) -> None:
        out = io.StringIO()
        code = main(["-1234567"], out=out)
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue().strip(), "-1.2M")

    def test_invalid_input_errors(self) -> None:
        err = io.StringIO()
        code = main(["not-a-number"], err=err)
        self.assertEqual(code, 2)
        self.assertIn("not a valid number", err.getvalue())


if __name__ == "__main__":
    unittest.main()
