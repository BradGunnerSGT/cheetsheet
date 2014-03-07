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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from markdown import markdown
import os
import sys
import re
from pprint import pprint



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

	tdata = []
	for section in data.get('sections'):
		leftPanel = []
		rightPanel = []
		bullet = '<bullet>&bull;</bullet>'
		
		sectiontitle = '<strong>%s</strong>' % section.get('title', "NO TITLE GIVEN")
		leftPanel.append(Paragraph(sectiontitle, styles['Normal']))

		lyrics = ""
		if section.get('lyrics'):
			lyrics += '<br/>'.join(section.get('lyrics'))
		lyrics = markdown(lyrics) 
		lyrics = "<para leftIndent='5'>%s</para>" % lyrics
		rightPanel.append(Paragraph(lyrics, styles['Normal']))

		
		measures = int(section.get('measures', '0'))
		plural = '' if measures == 1 else 's'
		leftPanel.append(Paragraph('%s %s measure%s' % (bullet, measures, plural), styles['Normal']))
		
		if section.get('notes'):
			for note in section.get('notes'):
				note = markdown(note)
				note = note.replace('<p>', '')
				note = note.replace('</p>', '')
				#print note
				if note.find('|') > -1:
					left, p, remaining = note.partition('|')
					center, p, right = remaining.rpartition('|')
					note = "%s<font face=\"Courier\">|%s|</font>%s" % (left, center, right)
					#print note
				leftPanel.append(Paragraph("%s %s" % (bullet, note), styles['Normal']))

		tdata.append([
			leftPanel,
			rightPanel
		])

	Story.append(
		Table(
			tdata, 
			style = TableStyle([ 
							('VALIGN', (0,0) , (-1, -1) , 'TOP' ) ,
							('INNERGRID',   (0,0) , (-1, -1),  0.25 , colors.black ),
							('BOX',   (0,0) , (-1, -1),  0.5 , colors.black ),
							])
			)
	)
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

