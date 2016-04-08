"""
convert.py

Parses Santander UK account reports and produces a JSON file with the transactions.

Copyright (C) 2016 by Arménio Pinto
Please the the file /LICENSE for the license details.
"""

import argparse
import json
import creditparser
import debitparser


def convert():
	args = parse_arguments()

	if creditparser.is_credit_report(args.input_file):
		output = creditparser.parse_file(args.input_file)
	elif debitparser.is_debit_report(args.input_file):
		output = debitparser.parse_file(args.input_file)

	with open(args.output_file, "w") as f:
		json.dump(output, f, indent = 4, separators = (",", ": "))


def parse_arguments():
	""" Parses the command-line arguments. """

	parser = argparse.ArgumentParser(
		description = "Converts Santander UK account reports to JSON.")
	parser.add_argument("input_file", help = "The input report path.")
	parser.add_argument("output_file", help = "The output report path.")

	return parser.parse_args()


if __name__ == "__main__":
	convert()
