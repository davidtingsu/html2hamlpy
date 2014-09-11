from  test_helper import unittest, render
import re
class DjangoTest(unittest.TestCase):
    def test_django_variable_in_cdata(self):
        haml = """\
:cdata
  Foo ={bar} baz
"""
        html = """\
<![CDATA[Foo {{bar}} baz]]>
"""
        self.assertEqual(haml.rstrip(), render(html))

        haml = """\
:cdata
  = bar
"""
        html = """\
<![CDATA[ {{bar}} ]]>
"""
        self.assertEqual(haml.rstrip(), render(html))


    def test_django_inline_variable_in_script(self):
      haml = """\
:javascript
  function foo() {
    return  ={story.teaser};
  }
"""
      html = """\
<script type="text/javascript">
  function foo() {
    return  {{ story.teaser }};
  }
</script>
"""
      self.assertEqual(haml.rstrip(), render(html))

    def test_django_variable_in_script(self):
      haml = """\
:javascript
  = story.teaser
"""
      html = """\
<script type="text/javascript">
    {{ story.teaser }}
</script>
"""
      self.assertEqual(haml.rstrip(), render(html))
    def test_erb_in_style(self):
      haml = """\
:css
  foo {
      bar: ={baz};
  }
"""
      html = """\
<style type="text/css">
    foo {
        bar: {{ baz }};
    }
</style>
"""
      self.assertEqual(haml.rstrip(), render(html))

      haml = """\
:css
  = baz;
"""
      html = """\
<style type="text/css">
        {{ baz }};
</style>
"""
      self.assertEqual(haml.rstrip(), render(html))

    def test_closed_tags(self):
        html = """\
{% autoescape on %}
    foo
{% endautoescape %}

"""
        haml = """\
- autoescape on
  foo
"""
        self.assertEqual(haml.rstrip(), render(html))
    def test_closed_tags_separated_by_html(self):
        html = """\
{% autoescape on %}
    <b>bar</b>
{% endautoescape %}

"""
        haml = """\
- autoescape on
  %b bar
"""
        self.assertEqual(haml.rstrip(), render(html))

    def test_nested_closed_tags_separated_by_html(self):
        html = """\
{% autoescape on %}
  <b>baz</b>
  {% foo on %}
    <b>bar</b>
  {% endfoo %}
{% endautoescape %}
"""
        haml = """\
- autoescape on
  %b baz
  - foo on
    %b bar
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

    def test_self_closing_tag(self):
        haml = """\
- cycle 'row1' 'row2' as rowcolors
"""
        html = """\
{% cycle 'row1' 'row2' as rowcolors %}
"""
        self.assertEqual(haml.rstrip(), render(html))
    def test_consecutive_self_closing_tags(self):
        haml = """\
- cycle 'row1' 'row2' as rowcolors
- cycle 'row1' 'row2' as rowcolors
- bar
"""
        html = """\
{% cycle 'row1' 'row2' as rowcolors %}
{% cycle 'row1' 'row2' as rowcolors %}
{% bar %}
"""
        self.assertEqual(haml.rstrip(), render(html))


    def test_nested_closed_tag(self):
        haml = """\
%foo
  - cycle 'row1' 'row2' as rowcolors
"""
        html = """\
<foo>
  {% cycle 'row1' 'row2' as rowcolors %}
</foo>
"""
        self.assertEqual(haml.rstrip(), render(html))

if __name__ == '__main__':
    unittest.main()
