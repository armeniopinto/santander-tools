"""
debitparser.py

Parses Santander UK debit card reports and produces a JSON file with the transactions.

Copyright (C) 2016 by Arménio Pinto
Please the the file /LICENSE for the license details.
"""

import argparse
import re
from decimal import Decimal
import datetime
import json

def parse_file(input_file):
	"""
	Parses a TXT debit report and returns a list of transactions with the following attributes:

	date - the transaction's date.
	card - the debit card associated with the transaction.
	card_type - the type of card, always 'Debit' for debit reports.
	type - the textual description of the transaction type.
	sub_type - the textual description of the transaction sub-type.
	location - the place where the transaction occurred.
	description - the textual description of the transaction.
	amount - the transaction's amount (negative value for purchases, positive for money in).
	"""

	# Removes unnecessary clutter from a report's lines:
	lines = [line.strip() for line in  open(input_file)]

	card = parse_card(lines[2])

	return [parse_transaction(lines[n + 1:n + 5], card) for n in range(3, len(lines))[0::5]]


CARD_PATTERN = re.compile(r"Account:\sXXXX\ XXXX\ XXXX\ (\d{4})")

def parse_card(card):
	"""Parses and returns the card number."""
	return CARD_PATTERN.match(card).group(1)


DATE_PATTERN = re.compile(r"Date:\s(\d{2}/\d{2}/\d{4})")

DESCRIPTION_PATTERNS = [
	re.compile(r"Description:\s(CARD\ PAYMENT)\ TO\ (.*)"),
	re.compile(r"Description:\s(CASH\ WITHDRAWAL)\ AT\ (.*)"),
	re.compile(r"Description:\s(CASH\ WITHDRAWAL\ REVERSAL)\ AT\ (.*)"),
	re.compile(r"Description:\s(CASH\ WITHDRAWAL\ HANDLING\ CHARGE)\ (.*)"),
	re.compile(r"Description:\s(CASH\ PAID\ IN)\ AT\ (.*)"),
	re.compile(r"Description:\s(POST\ OFFICE\ CASH\ WITHDRAWAL)()"),
	re.compile(r"Description:\s(DIRECT\ DEBIT\ PAYMENT)\ TO\ (.*)"),
	re.compile(r"Description:\s(BILL\ PAYMENT)\ TO\ (.*)"),
	re.compile(r"Description:\s(BILL\ PAYMENT\ VIA\ FASTER\ PAYMENT)\ TO\ (.*)"),
	re.compile(r"Description:\s\s?(FASTER\ PAYMENTS\ RECEIPT) (.*)"),
	re.compile(r"Description:\s(TRANSFER\ TO)\ (.*)"),
	re.compile(r"Description:\s(TRANSFER\ FROM)\ (.*)"),
	re.compile(r"Description:\s(TRANSFER\ VIA\ FASTER\ PAYMENT)()"),
	re.compile(r"Description:\s(REGULAR\ TRANSFER\ PAYMENT)\ TO\ (.*)"),
	re.compile(r"Description:\s(REJECTED\ TRANSFER\ VIA\ FASTER\ PAYMENT)\ TO\ (.*)"),
	re.compile(r"Description:\s(STANDING\ ORDER\ VIA\ FASTER\ PAYMENT)\ TO\ (.*)"),
	re.compile(r"Description:\s(BANK\ GIRO)\ (.*)"),
	re.compile(r"Description:\s(CREDIT)\ FROM\ (.*)"),
	re.compile(r"Description:\s(CHEQUE\ PAID\ IN)\ (.*)"),
	re.compile(r"Description:\s(BANK\ CHEQUE)\ (.*)"),
	re.compile(r"Description:\s(INTEREST\ PAID)\ (.*)"),
	re.compile(r"Description:\s(OVERSEAS\ TRANSACTION\ FEE)()")
]

AMOUNT_PATTERN = re.compile(r"Amount:\s(\-?\d+\.\d{2})")

def parse_transaction(lines, card):
	"""Parses a transaction lines."""

	transaction = {}

	transaction["date"] = datetime.datetime.strptime(
		DATE_PATTERN.match(lines[0]).group(1), "%d/%m/%Y").strftime("%Y/%m/%d")

	for description_pattern in DESCRIPTION_PATTERNS:
		match = description_pattern.match(lines[1])
		if match:
			transaction["type"] = match.group(1)
			transaction["description"] = match.group(2)
			break
	if "type" not in transaction:
		transaction["type"] = "UNKNOWN"
		transaction["description"] = lines[1]

	transaction["amount"] = AMOUNT_PATTERN.match(lines[2]).group(1)

	return transaction


def main():
	args = parser = parse_arguments()
	output = parse_file(args.input_file)
	with open(args.output_file, "w") as o:
		json.dump(output, o, indent = 4, separators = (",", ": "))


def parse_arguments():
	""" Parses the command-line arguments. """

	parser = argparse.ArgumentParser(
		description = "Converts Santander TXT debit reports to JSON.")
	parser.add_argument("input_file", help = "The input TXT debit report path.")
	parser.add_argument("output_file", help = "The output JSON debit report path.")

	return parser.parse_args()


if __name__ == "__main__":
	main()