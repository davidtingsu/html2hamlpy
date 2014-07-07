from  test_helper import unittest, render

class HtmlToHamlPyTest(unittest.TestCase):

    def test_no_tag_name_for_div_if_class_or_id_is_present(self):
        self.assertEqual('#foo', render('<div id="foo"></div>'))
        self.assertEqual('.foo', render('<div class="foo"></div>'))

    def test_multiple_class_names(self):
        self.assertEqual('.foo.bar.baz', render('<div class=" foo bar baz "></div>'))

if __name__ == '__main__':
    unittest.main()
