# Use list compomprehension for string concatenation http://www.skymind.com/~ocrow/python_string/
from bs4 import Tag, CData, Comment, Tag, NavigableString, Doctype, BeautifulSoup
import re
def to_haml_soup(self):
    return ''.join(child.to_haml(tabs=0) for child in (self.children or []) )

def to_haml_tag(self, tabs, **kwargs):
    output = tabulate(tabs)
    kwargs['instance'] = self

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
    return output + ''.join(child.to_haml(tabs=0) for child in (self.children or []) )
def to_haml_cdata(self, tabs):
    #TODO
    pass
def to_haml_navigable_string(self, tabs):
    #TODO
    pass
def to_haml_comment(self, tabs):
    #TODO
    pass
def to_haml_doctype(self, tabs):
    #TODO
    pass

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
