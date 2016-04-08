"""
convert.py

Parses Santander UK account reports and produces a JSON file with the transactions.

Copyright (C) 2016 by Arménio Pinto
Please the the file /LICENSE for the license details.
"""

import argparse
import os
import json
import creditparser
import debitparser


def convert():
	"""Converts the supplied files."""

	args = parse_arguments()

	merged = []
	for report in args.reports:
		transactions = []
		if creditparser.is_credit_report(report):
			transactions = creditparser.parse_file(report)
		elif debitparser.is_debit_report(report):
			transactions = debitparser.parse_file(report)
		else:
			raise Exception(report + " isn't a known report.")

		if args.merge:
			merged.extend(transactions)
			print(report + " converted.")
		else:
			name, ext = os.path.splitext(report)
			output = name + ".json"
			save_transactions(transactions, output)
			print(report + " converted to " + output)

	if args.merge:
		save_transactions(merged, args.merge)
		print("All transactions saved to " + args.merge)


def save_transactions(transactions, output):
	"""Writes a bunch of transactions to a JSON file."""
	with open(output, "w") as f:
		json.dump(transactions, f, indent = 4, separators = (",", ": "))


def parse_arguments():
	""" Parses the command-line arguments. """

	parser = argparse.ArgumentParser(
		description = "Converts Santander UK account reports to JSON.")
	parser.add_argument("reports", nargs='+', help = "the input reports paths (supports wildcards).")
	parser.add_argument("-merge", help = "optionally merges all transactions into a single JSON file.")

	return parser.parse_args()


if __name__ == "__main__":
	convert()
