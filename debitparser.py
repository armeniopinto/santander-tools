"""
debitparser.py

Parses Santander UK debit card reports and produces a list with the transactions.

Copyright (C) 2016 by Arménio Pinto
Please the the file /LICENSE for the license details.
"""

import argparse
import re
from decimal import Decimal
import datetime


# From: [start_date] to [end_date]
FIRST_LINE_PATTERN = re.compile(r"From:\s\d{2}/\d{2}/\d{4}\sto\s\d{2}/\d{2}/\d{4}")

def is_debit_report(input_file):
	"""Returns True if the file is a debit report."""
	with open(input_file, "r") as f:
		return True if FIRST_LINE_PATTERN.match(f.readline()) else False


def parse_file(input_file):
	"""
	Parses a TXT debit report and returns a list of transactions with the following attributes:

	date - the transaction's date.
	card - the debit card associated with the transaction.
	card_type - the type of card, always 'Debit' for debit reports.
	type - the textual description of the transaction type.
	description - the textual description of the transaction.
	amount - the transaction's amount (negative value for purchases, positive for money in).

	:input_file the path to the report to parse.
	:return: the list of transactions in the report.
	"""

	# Removes unnecessary clutter from a report's lines:
	lines = [line.strip().replace("&amp;", "&") for line in open(input_file, "r")]

	card = parse_card(lines[2])

	return [parse_transaction(lines[n + 1:n + 5], card) for n in range(3, len(lines))[0::5]]


CARD_PATTERN = re.compile(r"Account:\sXXXX\ XXXX\ XXXX\ (\d{4})")

def parse_card(card):
	"""Parses and returns the card number."""
	return CARD_PATTERN.match(card).group(1)


DATE_PATTERN = re.compile(r"Date:\s(\d{2}/\d{2}/\d{4})")
DESCRIPTION_PATTERN = re.compile(r"Description:\s(.*)")
AMOUNT_PATTERN = re.compile(r"Amount:\s(\-?\d+\.\d{2})")

def parse_transaction(lines, card):
	"""Parses a transaction's lines."""

	transaction = {}

	transaction["date"] = datetime.datetime.strptime(
		DATE_PATTERN.match(lines[0]).group(1), "%d/%m/%Y").strftime("%Y-%m-%d")
	transaction["card_type"] = "Debit"
	transaction["card_number"] = card
	transaction.update(parse_description(DESCRIPTION_PATTERN.match(lines[1]).group(1).strip()))
	transaction["amount"] = float(Decimal(AMOUNT_PATTERN.match(lines[2]).group(1)))

	return transaction


DESCRIPTION_PATTERNS = [
	re.compile(r"(?P<t>CARD\ PAYMENT)\ TO\ (?P<d>[^,]*).*"),
	re.compile(r"(?P<t>CASH\ WITHDRAWAL)\ AT\ (?P<d>[^,]*),\s?(?P<l>[^,]*).*"),
	re.compile(r"(?P<t>CASH\ WITHDRAWAL\ REVERSAL)\ AT\ (?P<d>[^,]*),\s?(?P<l>[^,]*).*"),
	re.compile(r"(?P<t>CASH\ WITHDRAWAL\ HANDLING\ CHARGE)\ (?P<d>.*)"),
	re.compile(r"(?P<t>CASH\ PAID\ IN)\ AT\ (?P<d>.*)"),
	re.compile(r"(?P<l>POST\ OFFICE)\ (?P<t>CASH\ WITHDRAWAL)"),
	re.compile(r"(?P<t>DIRECT\ DEBIT\ PAYMENT)\ TO\ (?P<d>.*)"),
	re.compile(r"(?P<t>BILL\ PAYMENT)\ TO\ (?P<d>.*)"),
	re.compile(r"(?P<t>BILL\ PAYMENT)\ VIA\ (?P<t2>FASTER\ PAYMENT)\ TO\ (?P<d>.*)"),
	re.compile(r"(?P<t2>FASTER\ PAYMENT)S\ (?P<t>RECEIPT) (?P<d>.*)"),
	re.compile(r"(?P<t>TRANSFER\ TO)\ (?P<d>.*)"),
	re.compile(r"(?P<t>TRANSFER\ FROM)\ (?P<d>.*)"),
	re.compile(r"(?P<t>TRANSFER)\ VIA\ (?P<t2>FASTER\ PAYMENT)(?P<d>)"),
	re.compile(r"(?P<t>REJECTED\ TRANSFER)\ VIA\ (?P<t2>FASTER\ PAYMENT)\ TO\ (?P<d>.*)"),
	re.compile(r"(?P<t>REGULAR\ TRANSFER\ PAYMENT)\ TO\ (?P<d>.*)"),
	re.compile(r"(?P<t>STANDING\ ORDER)\ PAYMENT\ TO\ (?P<d>.*)"),
	re.compile(r"(?P<t>STANDING\ ORDER)\ VIA\ (?P<t2>FASTER\ PAYMENT)\ TO\ (?P<d>.*)"),
	re.compile(r"(?P<t>BANK\ GIRO\ CREDIT)\ (?P<d>.*)"),
	re.compile(r"(?P<t>CREDIT)\ FROM\ (?P<d>.*)"),
	re.compile(r"(?P<t>CHEQUE\ PAID\ IN)\ AT\ (?P<d>.*)"),
	re.compile(r"(?P<t>BANK\ CHEQUE)\ (?P<d>.*)"),
	re.compile(r"(?P<t>INTEREST\ PAID)\ (?P<d>.*)"),
	re.compile(r"(?P<t>OVERSEAS\ TRANSACTION\ FEE)"),
	re.compile(r"(?P<t>REFUND)\ AT (?P<d>.*)")
]

def parse_description(line):
	"""Parses a description line."""

	description = {}

	for description_pattern in DESCRIPTION_PATTERNS:
		match = description_pattern.match(line)
		if match:
			keys = match.groupdict()
			description["type"] = match.group("t")
			if "t2" in keys:
				description["sub_type"] = match.group("t2")
			if "l" in keys:
				description["location"] = match.group("l").upper()
			if ("d" in keys) and match.group("d"):
				description["description"] = match.group("d")
			break

	if "type" not in description:
		description["type"] = "UNKNOWN"
		description["description"] = line

	return description
