#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from urllib import request
import sys

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True
            
    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.line = self.theContent
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                link = "<a href='" + self.theContent + "'>" + self.line + "</a><br>"
                filePrueba = open("prueba.html", "a")
                filePrueba.write(link)
                self.inContent = False
                self.theContent = ""
                self.line = ""
                filePrueba.close
    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars
            
# --- Main prog

if len(sys.argv) < 1:
    print ("Usage: python xml-parser-barrapunto.py <document>")
    print ()
    print (" <document>: file name of the document to parse")
    sys.exit(1)
    
# Load parser and driver

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!
filePrueba = open("prueba.html", "w")
filePrueba.close
url = "http://barrapunto.com/index.rss"
xmlUrl = request.urlopen(url)
theParser.parse(xmlUrl)

print ("Parse complete")
