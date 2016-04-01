"""
debitparser.py

Parses Santander UK debit card reports and produces a JSON file with the transactions.

Copyright (C) 2016 by Arménio Pinto
Please the the file /LICENSE for the license details.
"""

import argparse
import re
from decimal import Decimal
import json


def main():
	args = parser = parse_arguments()


def parse_arguments():
	""" Parses the command-line arguments. """

	parser = argparse.ArgumentParser(
		description = "Converts Santander TXT debit reports to JSON.")
	parser.add_argument("input_file", help = "The input TXT debit report path.")
	parser.add_argument("output_file", help = "The output JSON debit report path.")

	return parser.parse_args()


if __name__ == "__main__":
	main()