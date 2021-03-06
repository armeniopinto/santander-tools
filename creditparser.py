"""
creditparser.py

Parses Santander UK credit card reports and produces a list with the transactions.

Copyright (C) 2016 by Arménio Pinto
Please the the file /LICENSE for the license details.
"""

import argparse
import re
from decimal import Decimal


# [start_date][end_date][card]
FIRST_LINE_PATTERN = re.compile(r"\d{4}\-\d{2}\-\d{2}\d{4}\-\d{2}\-\d{2}\d{4}")

def is_credit_report(input_file):
	"""Returns True if the file is a credit report."""
	with open(input_file, "r") as f:
		return True if FIRST_LINE_PATTERN.match(f.readline()) else False


def parse_file(input_file):
	"""
	Parses a TXT credit report and returns a list of transactions with the following attributes:

	date - the transaction's date.
	card - the credit card associated with the transaction.
	card_type - the type of card, always 'Credit' for credit reports.
	type - the textual description of the transaction type.
	sub_type - the textual description of the transaction sub-type.
	location - the place where the transaction occurred.
	description - the textual description of the transaction.
	amount - the transaction's amount (negative value for purchases, positive for money in).

	:input_file the path to the report to parse.
	:return: the list of transactions in the report.
	"""

	# Removes unnecessary clutter from a report's lines:
	lines = [re.sub(r"\t{2,}", r"\t", line.rstrip("\n")) for line in open(input_file, "r")]

	return [parse_transaction(line) for line in lines if is_transaction(line)]


# [date]	[card]	[description]	([amount_in]|[money_out])
TRANSACTION_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})\t\*\*\ (\d{4})\t([^\t]+)\t((\d+\.\d{2})?)\t?((\d+\.\d{2})?)$")

def is_transaction(line):
	"""Returns a match if the supplied line is a transaction."""
	return TRANSACTION_PATTERN.match(line)


def parse_transaction(line):
	"""Parses a transaction line."""
	line = line.strip()

	transaction = {}
	match = TRANSACTION_PATTERN.match(line)
	transaction["date"] = match.group(1)
	transaction["card_type"] = "Credit"
	transaction["card_number"] = match.group(2)
	transaction.update(parse_description(match.group(3)))
	amount = Decimal(match.group(4))
	# All "money-out" transaction lines end with a non-tab. This is a bit of a hack :(.
	if not line.endswith("\t"):
		amount = amount * Decimal("-1")
	transaction["amount"] = float(amount)

	return transaction


DESCRIPTION_PATTERNS = [
	{
		# A regular purchase:
		"type": "PURCHASE",
		# PURCHASE - [type]	[location]	[description]
		"pattern": re.compile(r"^PURCHASE\ -\ ([^\t]+)\t([^\t]+)\t(.*)$")
	},
	{
		# A refund:
		"type": "REFUND",
		# PURCHASE [type] REFUND	[location]	[description]
		"pattern": re.compile(r"^PURCHASE ([^\ ]+) REFUND\t([^\t]+)\t(.*)$")
	},
	{
		# A recurrent purchase:
		"type": "PURCHASE",
		# RECURRENT TRANSACTION	[location]	[description]
		"pattern": re.compile(r"^([^\ ]+) TRANSACTION\t([^\t]+)\t(.*)$")
	}
]

def parse_description(description):
	"""Parses a transaction description."""

	# Replaces the description multiple spaces separators with tabs:
	description = re.sub(r"\s{2,}", r"\t", description).strip()

	for pattern in DESCRIPTION_PATTERNS:
		match = pattern["pattern"].match(description)
		if match:
			return build_transaction_description(match, pattern["type"])

	# Some other transaction (initial balance, payment, etc.):
	return {"type": description}


def build_transaction_description(match, type):
	"""Builds a transaction's description from a regex match."""
	return {
		"type": type, 
		"sub_type": match.group(1),
		"location": match.group(2),
		"description": match.group(3)
	}
