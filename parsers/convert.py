"""
convert.py

Parses Santander UK account reports and produces a JSON file with the transactions.

Copyright (C) 2016 by Arménio Pinto
Please the the file /LICENSE for the license details.
"""

import argparse
import os
import json
from . import creditparser
from . import debitparser


def convert(reports_files):
	"""
	Converts the supplied reports.

	:param reports_file the list of file paths to parse.
	:returns: a dictionary with the reports file name and the respective lists of transactions.
	"""

	transactions = {}
	for report_file in reports_files:
		if creditparser.is_credit_report(report_file):
			transactions[report_file] = creditparser.parse_file(report_file)
		elif debitparser.is_debit_report(report_file):
			transactions[report_file] = debitparser.parse_file(report_file)
		else:
			raise Exception(report_file + " isn't a known report.")

	return transactions


def save_transactions(transactions, output_file):
	"""Writes a bunch of transactions to a JSON file."""
	with open(output_file, "w") as f:
		json.dump(transactions, f, indent = 4, separators = (",", ": "))


def parse_arguments():
	"""Parses the command-line arguments."""

	parser = argparse.ArgumentParser(
		description = "Converts Santander UK account reports to JSON.")
	parser.add_argument("reports", nargs='+', help = "the input reports paths (supports wildcards).")
	parser.add_argument("-merge", help = "optionally merges all transactions into a single JSON file.")

	return parser.parse_args()


if __name__ == "__main__":
	args = parse_arguments()

	merged = []
	for report_file, transactions in sorted(convert(args.reports).items()):
		if args.merge:
			merged.extend(transactions)
			print(report_file + " converted.")
		else:
			name, ext = os.path.splitext(report_file)
			output_file = name + ".json"
			save_transactions(transactions, output_file)
			print(report_file + " converted to " + output_file)

	if args.merge:
		save_transactions(merged, args.merge)
		print("All transactions saved to " + args.merge)
