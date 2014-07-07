import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import io
import bs4
import unittest
from lib.html2hamlpy import html
def render(string):
  return bs4.BeautifulSoup(string).to_haml()
