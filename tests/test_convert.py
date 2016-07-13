"""
test_convert.py

Tests the Santander UK account report converter.

Copyright (C) 2016 by Arménio Pinto
Please the the file /LICENSE for the license details.
"""

import creditparser
import debitparser
import convert


def test_convert():
	"""Tests convert.convert()."""
	credit_file = "tests/data/credit_1.txt"
	credit_transactions = creditparser.parse_file(credit_file)

	debit_file = "tests/data/debit_1.txt"
	debit_transactions = debitparser.parse_file(debit_file)

	all_transactions = convert.convert([credit_file, debit_file])

	assert credit_file in all_transactions
	assert debit_file in all_transactions
	assert all_transactions[credit_file] == credit_transactions
	assert all_transactions[debit_file] == debit_transactions
