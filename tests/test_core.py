import unittest

from numfmt_cli.core import format_number, parse_number


class TestFormatNumber(unittest.TestCase):
    def test_millions(self) -> None:
        self.assertEqual(format_number(1234567), "1.2M")

    def test_thousands(self) -> None:
        self.assertEqual(format_number(1500), "1.5K")

    def test_billions(self) -> None:
        self.assertEqual(format_number(2_300_000_000), "2.3B")

    def test_trillions(self) -> None:
        self.assertEqual(format_number(4_000_000_000_000), "4.0T")

    def test_below_thousand_has_no_suffix(self) -> None:
        self.assertEqual(format_number(500), "500")

    def test_zero(self) -> None:
        self.assertEqual(format_number(0), "0")

    def test_negative_value(self) -> None:
        self.assertEqual(format_number(-1234567), "-1.2M")

    def test_custom_precision(self) -> None:
        self.assertEqual(format_number(1234567, precision=3), "1.235M")

    def test_zero_precision_rounds_to_integer_suffix(self) -> None:
        self.assertEqual(format_number(1500000, precision=0), "2M")


class TestParseNumber(unittest.TestCase):
    def test_parses_million_suffix(self) -> None:
        self.assertEqual(parse_number("1.2M"), 1200000)

    def test_parses_thousand_suffix(self) -> None:
        self.assertEqual(parse_number("500K"), 500000)

    def test_parses_billion_suffix(self) -> None:
        self.assertEqual(parse_number("2.3B"), 2300000000)

    def test_parses_trillion_suffix(self) -> None:
        self.assertEqual(parse_number("4T"), 4000000000000)

    def test_lowercase_suffix(self) -> None:
        self.assertEqual(parse_number("1.5m"), 1500000)

    def test_no_suffix_returns_integer(self) -> None:
        self.assertEqual(parse_number("500"), 500)

    def test_negative_with_suffix(self) -> None:
        self.assertEqual(parse_number("-1.2M"), -1200000)

    def test_invalid_string_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_number("not a number")

    def test_unknown_suffix_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_number("5Q")


if __name__ == "__main__":
    unittest.main()
