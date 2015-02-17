[![Build Status](http://img.shields.io/travis/davidtingsu/html2hamlpy/master.svg)](https://travis-ci.org/davidtingsu/html2hamlpy?branch=master)
[![Coverage Status](http://img.shields.io/coveralls/davidtingsu/html2hamlpy/master.svg)](https://coveralls.io/r/davidtingsu/html2hamlpy?branch=master)
[![Latest Version](https://pypip.in/version/html2hamlpy/badge.svg)](https://pypi.python.org/pypi/html2hamlpy/)
[![Downloads](https://pypip.in/d/html2hamlpy/badge.svg)](https://pypi.python.org/pypi/html2hamlpy/)
[![License](https://pypip.in/license/html2hamlpy/badge.svg)](https://pypi.python.org/pypi/html2hamlpy/)


html2hamlpy
===========
Converts (django) HTML to [HamlPy](https://github.com/jessemiller/HamlPy)


Installation
============

    pip install html2hamlpy


Usage
=====

```python
from html2hamlpy.html import Converer

Converter('some django template code', 'html.parser').to_haml()
```
