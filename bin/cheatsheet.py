#!/usr/bin/env python

"""
This file is part of Cheetsheet.

Cheetsheet is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Cheetsheet is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Cheetsheet.  If not, see <http://www.gnu.org/licenses/>.

"""


def main(args):
	"""Main loop, process each file in turn"""
	for filename in args.input:
		print "processing %s" % (filename)


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Process a Cheetsheet file into a PDF")
	parser.add_argument('input', nargs='+', help='Cheetsheet-formatted filename(s) to process.')

	args = parser.parse_args()
	main(args)

