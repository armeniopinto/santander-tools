"""
test_creditparser.py

Tests the Santander UK credit card reports parser.

Copyright (C) 2016 by Arménio Pinto
Please the the file /LICENSE for the license details.
"""

import json
from parsers import creditparser


def test_parse_description():
	"""Tests creditparser.parse_description()."""
	with open("tests/parsers/data/credit_descriptions.json") as test_data_file:
		for test_description in json.load(test_data_file):
			description = creditparser.parse_description(test_description["description"])
			assert description == test_description["expected"]


def test_parse_transaction():
	"""Tests creditparser.parse_transaction()."""
	with open("tests/parsers/data/credit_transactions.json") as test_data_file:
		for test_transaction in json.load(test_data_file):
			transaction = creditparser.parse_transaction(test_transaction["transaction"])
			assert transaction == test_transaction["expected"]