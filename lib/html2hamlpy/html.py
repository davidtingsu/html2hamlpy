# Use list compomprehension for string concatenation http://www.skymind.com/~ocrow/python_string/
from bs4 import Tag, CData, Comment, Tag, NavigableString, Doctype, BeautifulSoup
import re
def to_haml_soup(self):
    return ''.join(child.to_haml(tabs=0) for child in (self.children or []) )

def to_haml_tag(self, tabs, **kwargs):
    output = tabulate(tabs)
    kwargs['instance'] = self

    if (self.name == "style" and
        (self.attrs['type'] is None or self.attrs['type'] == "text/css") and
        len(set(self.attrs.keys()) - set(['type'])) == 0):
            return to_haml_filter('css', tabs, **kwargs)

    if (self.name == "script" and
        (self.attrs['type'] is None or self.attrs['type'] == "text/javascript") and
        len(set(self.attrs.keys()) - set(['type'])) == 0):
            return to_haml_filter('javascript', tabs, **kwargs)

    if (not
        ((self.name == 'div') and
        (
            ('id' in self.attrs and is_static_id(**kwargs)) or

            (
                ('class' in self.attrs and is_static_classname(**kwargs)) and
                ('class' in self.attrs and any(map(lambda c: is_haml_css_attr(c), self.attrs['class'])))
            )
        ))
    ):
        output +=  ('%%%s' % self.name)

    if len(self.attrs) > 0:
        if 'id' in self.attrs and is_static_id(**kwargs):
            output +=  ("#%s" % self.attrs['id'])
            del self.attrs['id']
        if 'class' in self.attrs:
            for c in filter(lambda c: is_haml_css_attr(c), self.attrs['class']):
                output += ".%s" % (c)
            leftover = filter(lambda c: not is_haml_css_attr(c), self.attrs['class'])
            del self.attrs['class']
            if any(leftover) : self.attrs['class'] = ' '.join(leftover)
    if len(self.attrs) > 0: output += haml_attributes(**kwargs)
    if self.isSelfClosing : output += "/"
    return output + ''.join(child.to_haml(tabs=0) for child in (self.children or []) )
def to_haml_cdata(self, tabs):
    #TODO
    pass
def to_haml_navigable_string(self, tabs):
    #TODO
    return self
def to_haml_comment(self, tabs):
    #TODO
    pass
def to_haml_doctype(self, tabs, **kwargs):
    attrs = ["", "", ""]
    search = re.search(r'DTD\s+([^\s]+)\s*([^\s|^\/]*)\s*([^\s]*)\s*\/\/', self.string)
    if search: attrs = search.groups()
    kind, version, strictness = [ attr.lower() for attr in attrs ]
    if kind == "html":
        version = ""
        if strictness == "": strictness = "strict"
    if version == "1.0" or version is None:
        version = ""
    if strictness == 'transitional'  or strictness is None:
        strictness = ""
    if version: version = " %s" % version.capitalize()
    if strictness: strictness = " %s" % strictness.capitalize()
    return "%s!!!%s%s" % (tabulate(tabs), version, strictness)

def is_static_id(**kwargs):
    instance = kwargs['instance']
    return  is_static_attribute('id', **kwargs) and is_haml_css_attr(instance.attrs['id'])

def is_haml_css_attr(attr):
    return bool(re.match(r'^[-:\w]+$', attr))

def is_dynamic_attribute(name, **kwargs):
    #TODO
    return False

def is_static_attribute(name, **kwargs):
    instance = kwargs['instance']
    return name in instance.attrs and not is_dynamic_attribute(name, **kwargs)

def is_static_classname(**kwargs):
    return is_static_attribute('class', **kwargs)

def is_dynamic_attribute(name, **kwargs):
    #TODO
    return False
def to_haml_filter(filter, tabs, **kwargs):
    instance = kwargs['instance']

    content = instance.text
    content = re.sub(r'\A\s*\n(\s*)','\g<1>', content)
    original_indent = re.match(r'\A(\s*)', content).group()

    if all( map(lambda line: len(line.strip()) == 0 or re.match('^'+original_indent, line), content.split('\n')) ):
         content = re.sub('^'+original_indent, tabulate(tabs + 1), content)
    else:
        # Indentation is inconsistent. Strip whitespace from start and indent all
        # to ensure valid Haml
        # https://github.com/haml/html2haml/blob/c41cb712816d2ea4300e7c1730328a59a63b2ba7/lib/html2haml/html.rb#L453
        content = content.lstrip()
        content = re.sub(r'^', tabulate(tabs + 1), content, flags=re.MULTILINE)

    content = content.rstrip()
    content += "\n"

    return "%s:%s\n%s" % (tabulate(tabs), filter, content)

def haml_attributes(**kwargs):
    instance = kwargs['instance']
    attrs = map(lambda (name, value): haml_attribute_pair(name, value), instance.attrs.items())
    return "{%s}" % ', '.join(attrs)

def haml_attribute_pair(name, value, **kwargs):
    return "%s:\"%s\"" % (name, value)

def tabulate(tabs):
    return '  ' * tabs

setattr(BeautifulSoup, 'to_haml', to_haml_soup)
setattr(Tag, 'to_haml', to_haml_tag)
setattr(CData, 'to_haml', to_haml_cdata)
setattr(Comment, 'to_haml', to_haml_comment)
setattr(NavigableString, 'to_haml', to_haml_navigable_string)
setattr(Doctype, 'to_haml', to_haml_doctype)
