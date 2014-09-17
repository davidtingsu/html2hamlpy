import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import io
import bs4
import unittest
from html2hamlpy import html
def render(string):
  return html.Converter(string, 'html.parser').to_haml().rstrip()
