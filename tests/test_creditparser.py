"""
test_creditparser.py

Tests the Santander UK credit card reports parser.

Copyright (C) 2016 by Arménio Pinto
Please the the file /LICENSE for the license details.
"""

import json
import creditparser


def test_is_credit_report():
	"""Tests creditparser.is_credit_report()."""
	assert creditparser.is_credit_report("tests/data/credit_1.txt")
	assert not creditparser.is_credit_report("tests/data/debit_1.txt")


def test_parse_description():
	"""Tests creditparser.parse_description()."""
	with open("tests/data/credit_descriptions.json", "r") as test_data_file:
		for test_description in json.load(test_data_file):
			description = creditparser.parse_description(test_description["description"])
			assert description == test_description["expected"]


def test_parse_transaction():
	"""Tests creditparser.parse_transaction()."""
	with open("tests/data/credit_transactions.json", "r") as test_data_file:
		for test_transaction in json.load(test_data_file):
			transaction = creditparser.parse_transaction(test_transaction["transaction"])
			assert transaction == test_transaction["expected"]


def test_parse_file():
	"""Tests creditparser.parse_file()."""
	with open("tests/data/credit_1.json", "r") as test_output_file:
		assert json.load(test_output_file) == creditparser.parse_file("tests/data/credit_1.txt")
