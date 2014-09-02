from  test_helper import unittest, render
import re
class DjangoTest(unittest.TestCase):
    def test_closed_tags(self):
        html = """\
{% autoescape on %}
    foo
{% endautoescape %}

"""
        haml = """\
- autoescape
  foo
"""



        self.assertEqual(haml.rstrip(), render(html))
if __name__ == '__main__':
    unittest.main()
