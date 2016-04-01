"""
creditparser.py

Parses Santander UK credit card reports and produces a JSON file with the transactions.

Copyright (C) 2016 by Arménio Pinto
Please the the file /LICENSE for the license details.
"""

import argparse
import re
from decimal import Decimal
import json


def parse_file(input_file):
	"""
	Parses a TXT credit report and returns a list of transactions with the following attributes:

	date - the transaction's date.
	card - the credit card associated with the transaction.
	type - the textual description of the transaction type.
	location - the place where the transaction occurred.
	description - the textual description of the transaction.
	amount - the transaction's amount (negative value for purchases, positive for money in).
	"""

	# Removes unnecessary clutter from a report's lines:
	lines = [re.sub(r"\t{2,}", r"\t", line.rstrip("\n")) for line in  open(input_file)]

	return [parse_transaction(line) for line in lines if is_transaction(line)]


# [date]	[card]	[description]	([amount_in]|[money_out])
TRANSACTION_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})\t(\*\*\ \d{4})\t([^\t]+)\t((\d+\.\d{2})?)\t?((\d+\.\d{2})?)$")

def is_transaction(line):
	"""Returns a match if the supplied line is a transaction."""
	return TRANSACTION_PATTERN.match(line)


def parse_transaction(line):
	"""Parses a transaction line."""

	transaction = {}
	match = TRANSACTION_PATTERN.match(line)
	transaction["date"] = match.group(1)
	transaction["card"] = match.group(2)
	transaction.update(parse_description(match.group(3)))
	amount = Decimal(match.group(4))
	# All "money-out" transaction lines end with a non-tab. This is a bit of a hack :(.
	if not line.endswith("\t"):
		amount = amount * Decimal("-1")
	transaction["amount"] = amount

	return transaction


# PURCHASE - [type]	[location]	[description]
PURCHASE_PATTERN = re.compile(r"^PURCHASE\ -\ ([^\t]+)\t([^\t]+)\t(.*)$")

# PURCHASE [type] REFUND	[location]	[description]
REFUND_PATTERN = re.compile(r"^PURCHASE ([^\ ]+) REFUND\t([^\t]+)\t(.*)$")

# RECURRENT TRANSACTION	[location]	[description]
RECURRENT_PATTERN = re.compile(r"^([^\ ]+) TRANSACTION\t([^\t]+)\t(.*)$")

def parse_description(description):
	"""Parses a transaction description."""

	# Replaces the description multiple spaces separators with tabs:
	description = re.sub(r"\s{2,}", r"\t", description).strip()

	# Regular purchase:
	match = PURCHASE_PATTERN.match(description)
	if match:
		return build_transaction_description(match, "PURCHASE")

	# Refund:
	match = REFUND_PATTERN.match(description)
	if match:
		return build_transaction_description(match, "REFUND")

	# Recurrent:
	match = RECURRENT_PATTERN.match(description)
	if match:
		return build_transaction_description(match, "PURCHASE")

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


def main():
	args = parser = parse_arguments()
	output = parse_file(args.input_file)
	with open(args.output_file, "w") as o:
		json.dump(output, o, indent = 4, separators = (",", ": "), default = decimal_default)


def decimal_default(obj):
	"""Converts all decimals to floats during JSON serialisation."""
	if isinstance(obj, Decimal):
		return float(obj)
	raise TypeError


def parse_arguments():
	""" Parses the command-line arguments. """

	parser = argparse.ArgumentParser(
		description = "Converts Santander TXT credit reports to JSON.")
	parser.add_argument("input_file", help = "The input TXT credit report path.")
	parser.add_argument("output_file", help = "The output JSON credit report path.")

	return parser.parse_args()


if __name__ == "__main__":
	main()