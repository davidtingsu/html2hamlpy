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

    def test_variables(self):
        html = """\
<div class='article'>
  <div class='preview'>
    {{ story.teaser }}
  </div>
</div>
"""
        haml = """\
.article
  .preview
    = story.teaser
"""
        self.assertEqual(haml.rstrip(), render(html))

    def test_attribute_variables(self):
      haml="""\
%a{title:"Hello ={name}, how are you?"} Hello
"""
      html = """\
<a title='Hello {{ name }}, how are you?'>Hello</a>
"""
      self.assertEqual(haml.rstrip(), render(html))
if __name__ == '__main__':
    unittest.main()
