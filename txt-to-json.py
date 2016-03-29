import argparse
import re
import json


def parse_txt(input_file):
	transactions = []

	lines = [line.rstrip("\n") for line in open(input_file)]
	# Transactions only show-up from the 4th line onwards.
	for line in lines[4:-1]:
		line = re.sub(r"\t{2,}", r"\t", line.strip())
		transactions.append(parse_transaction(line))

	return transactions


# [date] [card] [description] [amount]
TRANSACTION_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})\t(\*\*\ \d{4})\t([^\t]+)\t([\d.]+)$")

def parse_transaction(line):
	transaction = {}

	match = TRANSACTION_PATTERN.match(line)
	if match:
		transaction["date"] = match.group(1)
		transaction["card"] = match.group(2)
		transaction.update(parse_description(match.group(3)))
		transaction["amount"] = match.group(4)

	return transaction


# [type] [location] [description]
DESCRIPTION_PATTERN = re.compile(r"^([^\t]+)\t([^\t]+)\t([^\t]+)$")

def parse_description(description):
	attributes = {}

	match = DESCRIPTION_PATTERN.match(re.sub(r"\s{2,}", r"\t", description.strip()))
	if match:
		attributes["type"] = match.group(1)
		attributes["location"] = match.group(2)
		attributes["description"] = match.group(3)

	return attributes


def parse_arguments():
	parser = argparse.ArgumentParser(
		description = "Converts Santander TXT credit reports to JSON.")
	parser.add_argument("input_file", help = "The input TXT credit report path.")
	parser.add_argument("output_file", help = "The output JSON credit report path.")
	return parser.parse_args()


def main():
	args = parser = parse_arguments()
	output = parse_txt(args.input_file)
	with open(args.output_file, "w") as o:
		json.dump(output, o, indent = 4, separators = (",", ": "))


if __name__ == "__main__":
	main()