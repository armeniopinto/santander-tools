"""
test_debitparser.py

Tests the Santander UK debit card reports parser.

Copyright (C) 2016 by Arménio Pinto
Please the the file /LICENSE for the license details.
"""

import json
from parsers import debitparser


def test_parse_description():
	"""Tests debitparser.parse_description()."""
	with open("tests/parsers/data/debit_descriptions.json") as test_data_file:
		for test_description in json.load(test_data_file):
			description = debitparser.parse_description(test_description["description"])
			assert description == test_description["expected"]


def test_parse_transaction():
	"""Tests debitparser.parse_transaction()."""
	with open("tests/parsers/data/debit_transactions.json") as test_data_file:
		for test_transaction in json.load(test_data_file):
			transaction = debitparser.parse_transaction(test_transaction["transaction"], "1234")
			assert transaction == test_transaction["expected"]


def test_parse_file():
	"""Tests debitparser.parse_file()."""
	with open("tests/parsers/data/debit_1.json", "r") as test_output_file:
		assert json.load(test_output_file) == debitparser.parse_file("tests/parsers/data/debit_1.txt")