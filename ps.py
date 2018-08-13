from __future__ import print_function
import argparse
import getpass
import os.path
import os

try:
	input = raw_input
except NameError:
	pass

parser = argparse.ArgumentParser(description='Stores and retrieves passwords through the use of a master key.')
parser.add_argument('--list', '-l', '--ls', action='store_true', help='Lists the tags of passwords stored')
parser.add_argument('--store', '-s', nargs=1, metavar='TAG', help='Store password at tag.')
parser.add_argument('--get', '-g', nargs=1, metavar='TAG', help='Get value from tag.')
parser.add_argument('--remove', '-r', nargs=1, metavar='TAG', help='Removes item from database. Requires override argument to be present as well.')
parser.add_argument('--override', '-f', action='store_true', help='Allows overwriting of preexisting data.')

args = parser.parse_args()

def ask_for_master_key():
	return getpass.getpass('Please enter master key for tag: ')

def ask_for_password():
	return getpass.getpass('Please enter password for tag: ')

def get_tags():
	"""Lists all tags for currently stored passwords (just contents of db folder)"""
	return os.listdir("db")

def validate_tag(tag):
	"""Returns if tag is alphanumeric, plus underscores."""
	return tag.replace("_", "").isalnum()

def get_tag_path(tag):
	return "db/" + tag

def verify_tag(tag):
	"""Ensures tag is valid, or else throws an exception."""
	if not validate_tag(tag):
		raise ValueError("Tag " + tag + " is not a valid tag! Must be alphanumeric plus underscores.")
	return tag

def autocomplete(tag, tags):
	"""Returns which of tags is the best match for user typed tag, else return None."""
	bestmatch = None
	starts = False
	for candidate in tags:
		if candidate == tag:
			return tag
		if starts == False:
			if candidate.startswith(tag):
				starts = True
				bestmatch = candidate
			elif tag in candidate:
				bestmatch = candidate
	return bestmatch

def perform_cipher(one, two, positive):
	"""Shifts elements of one by values of characters of two in positional order, with sign determined by positive."""
	res = ""
	if len(one) > len(two):
		raise ValueError("Length of object to be ciphered must be less than or equal to length of key.")
	final = ""
	for i in range(0, len(one)):
		ord_one = ord(one[i])
		ord_two = ord(two[i])
		final_ord = ord_one + (1 if positive else -1) * ord_two
		final_ord = final_ord % 128 #get to ascii range
		final += chr(final_ord)
	return final

if args.remove != None:
	tag = verify_tag(args.remove[0])
	if not args.override:
		print("Cannot remove without override flag.")
	else:
		path = get_tag_path(tag)
		if os.path.isfile(path):
			os.remove(get_tag_path(tag))
		else:
			print("No such tag '" + tag + "' exists.")

if args.store != None:
	tag = verify_tag(args.store[0])
	password = ask_for_password()
	master_key = ask_for_master_key()
	path = get_tag_path(tag)
	if not args.override and os.path.isfile(path):
		print("Cannot overwrite a tag without override flag.")
	else:
		with open(path, "w") as f:
			f.write(perform_cipher(password, master_key, True))

if args.get != None:
	tag = verify_tag(args.get[0])
	tags = get_tags()
	found_tag = autocomplete(tag, tags)
	if found_tag == None:
		print("No tag '" + tag + "' found.")
	else:
		if found_tag != tag:
			print("Autocompleted to '" + found_tag + "'")
		master_key = ask_for_master_key()
		with open(get_tag_path(found_tag), "r") as f:
			print(perform_cipher(f.read(), master_key, False))

if args.list:
	tags = get_tags()
	for tag in tags:
		print(tag)

