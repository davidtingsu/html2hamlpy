from  test_helper import unittest, render

class HtmlToHamlPyTest(unittest.TestCase):
    def test_doctype(self):
        self.assertEqual('!!!', render("<!DOCTYPE html>"))
        self.assertEqual('!!! 1.1', render('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'))
        self.assertEqual('!!! Strict', render('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'))
        self.assertEqual('!!! Frameset', render('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">'))
        self.assertEqual('!!! Mobile 1.2', render('<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.2//EN" "http://www.openmobilealliance.org/tech/DTD/xhtml-mobile12.dtd">'))
        self.assertEqual('!!! Basic 1.1', render('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML Basic 1.1//EN" "http://www.w3.org/TR/xhtml-basic/xhtml-basic11.dtd">'))
        self.assertEqual('!!!', render('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'))
        self.assertEqual('!!! Strict', render('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'))
        self.assertEqual('!!! Frameset', render('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">'))
        self.assertEqual('!!!', render('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">'))

    def test_id_and_class_should_be_removed_from_hash(self):
        self.assertEqual('%span#foo.bar', render('<span id="foo" class="bar">  </span>'))

    def test_no_tag_name_for_div_if_class_or_id_is_present(self):
        self.assertEqual('#foo', render('<div id="foo"></div>'))
        self.assertEqual('.foo', render('<div class="foo"></div>'))

    def test_multiple_class_names(self):
        self.assertEqual('.foo.bar.baz', render('<div class=" foo bar baz "></div>'))

    def test_class_with_dot_and_hash(self):
        self.assertEqual('%div{class:"foo.bar"}', render("<div class='foo.bar'></div>"))
        self.assertEqual('%div{class:"foo#bar"}', render("<div class='foo#bar'></div>"))
        self.assertEqual('.foo.bar{class:"foo#bar foo.bar"}', render("<div class='foo foo#bar bar foo.bar'></div>"))

    def test_id_with_dot_and_hash(self):
        self.assertEqual('%div{id:"foo.bar"}', render("<div id='foo.bar'></div>"))
        self.assertEqual('%div{id:"foo#bar"}', render("<div id='foo#bar'></div>"))

    def test_self_closing_tag(self):
        self.assertEqual("%img/", render("<img />"))

    def test_inline_text(self):
        self.assertEqual("%p foo", render("<p>foo</p>"))

    def test_inline_comment(self):
        self.assertEqual("/ foo", render("<!-- foo -->"))
        haml = """\
/ foo
%p bar
"""
        html = """\
<!-- foo -->
<p>bar</p>
"""
        self.assertEqual(haml.rstrip(), render(html))

    def test_non_inline_comment(self):
        haml = """\
/
  Foo
  Bar
"""
        html = """\
<!-- Foo
Bar -->
"""
        self.assertEqual(haml.rstrip(), render(html))

    def test_conditional_comment(self):
        haml = """\
/[if foo]
  bar
  baz
"""
        html = """\
<!--[if foo]>
  bar
  baz
<![endif]-->
"""
        self.assertEqual(haml.rstrip(), render(html))

    def test_style_to_css_filter(self):
        haml = """\
:css
  foo {
    bar: baz;
  }\
"""
        html = """\
<style type="text/css">
  foo {
    bar: baz;
  }
</style>
"""
        self.assertEqual(haml, render(html))

    def test_style_to_css_filter_with_following_content(self):
        haml="""\
%head
  :css
    foo {
      bar: baz;
    }
%body Hello
"""
        html = """\
<head>
  <style type="text/css">
    foo {
      bar: baz;
    }
  </style>
</head>
<body>Hello</body>
"""
        self.assertEqual(haml.rstrip(), render(html))

    def test_style_to_css_filter_with_no_content(self):
        haml = """\
:css
"""
        html = """\
<style type="text/css"> </style>
"""
        self.assertEqual(haml.rstrip(), render(html))

    def test_filter_with_inconsistent_indentation(self):
        haml = """\
:css
  foo {
      badly: indented;
  }
"""
        html="""\
<style type="text/css">
  foo {
    badly: indented;
}
</style>
"""
        self.assertEqual(haml.rstrip(), render(html))
    def test_inline_conditional_comment(self):
        haml = """\
/[if foo] bar baz
"""
        html="""\
<!--[if foo]> bar baz <![endif]-->
"""
        self.assertEqual(haml.rstrip(), render(html))

    def test_script_tag(self):
        haml =  """\
:javascript
  function foo() {
    return "12" & "13";
  }
"""
        html = """\
<script type="text/javascript">
  function foo() {
    return "12" & "13";
  }
</script>

"""
        self.assertEqual(haml.rstrip(), render(html))

if __name__ == '__main__':
    unittest.main()
