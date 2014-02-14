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

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os
import sys


def buildPDF(data, filename):
	""" create a PDF document"""
	doc = SimpleDocTemplate(
		filename, 
		pagesize=letter,
		rightMargin=36,leftMargin=36,
		topMargin=36,bottomMargin=18
	)

	Story = []  # this will be the text of the document that is flowed into the PDF

	styles = getSampleStyleSheet()
	styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

	# add the header to the Story
	header = 'Title: <b>%s</b><br/>\
	Artist: <b>%s</b><br/>\
	Key: <b>%s</b><br/>\
	Tempo: <b>%s</b><br/>' % (
		data.get('title'), 
		data.get('artist'), 
		data.get('key'), 
		data.get('tempo'))
	Story.append(Paragraph(header, styles['Normal']))
	Story.append(Spacer(1,12))

	for section in data.get('sections'):
		notestr = ''
		if section.get('notes'):
			for note in section.get('notes'):
				notestr += "- %s<br/>" % note

		lyrstr = ''
		if section.get('lyrics'):
			#lyrstr += '<para leftIndent="20">'
			for lyric in section.get('lyrics'):
				lyrstr += "%s<br/>" % lyric 
			#lyrstr += "</para>"

		para = """
		<b>%s</b><br/>
		<i>- %s measure%s<br/>
		%s</i>
		%s
		""" % (
			section.get('title'), 
			section.get('measures', "0"),
			's' if section.get('measures', None) else '',
			notestr,
			lyrstr
		)
		Story.append(Paragraph(para, styles['Normal']))
		#Story.append(Paragraph(lyrstr, styles['Normal']))
		Story.append(Spacer(1,12))

	# create the PDF and write it out
	doc.build(Story)






def main(args):
	"""Main loop, import the file, parse out the json, process it, and output the PDF"""
	import json
	for filename in args.input:
		(outfile, ext) = os.path.splitext(filename)
		outfile = outfile + ".pdf"

		print "processing %s, writing to %s" % (filename,outfile)
		raw = open(filename).read()
		jdata = json.loads(raw)

		doc = buildPDF(jdata, outfile)


if __name__ == "__main__":
	"""preamble, handle option parsing, housekeeping, and start the main loop"""

	import argparse
	parser = argparse.ArgumentParser(description="Process a Cheetsheet file into a PDF")
	parser.add_argument('input', nargs='+', help='Cheetsheet-formatted filename(s) to process.')

	args = parser.parse_args()
	main(args)

