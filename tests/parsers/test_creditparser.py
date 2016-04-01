import json
from parsers import creditparser


def test_parse_description():
	"""Tests creditparser.parse_description()."""
	with open("tests/parsers/test_credit_descriptions.json") as test_data_file:
		for test_description in json.load(test_data_file):
			description = creditparser.parse_description(test_description["description"])
			assert description == test_description["expected"]