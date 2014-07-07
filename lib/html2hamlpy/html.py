# Use list compomprehension for string concatenation http://www.skymind.com/~ocrow/python_string/
from bs4 import Tag, CData, Comment, Tag, NavigableString, Doctype, BeautifulSoup
import re
def to_haml_soup(self):
    return ''.join(child.to_haml(tabs=0) for child in (self.children or []) )
def to_haml_tag(self, tabs):
    output = tabulate(tabs)
    if len(self.attrs) > 0:
        if 'id' in self.attrs and is_static_id(self.attrs['id']):
            output +=  ("#%s" % self.attrs['id'])
            del self.attrs['id']
        if 'class' in self.attrs:
            for c in filter(lambda c: is_haml_css_attr(c), self.attrs['class']):
                output += ".%s" % (c)
            leftover = filter(lambda c: not is_haml_css_attr(c), self.attrs['class'])
            del self.attrs['class']
            if any(leftover) : self.attrs['class'] = ' '.join(leftover)
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
def is_static_id(id, **kwargs):
    #TODO
    return is_haml_css_attr(id)
def is_haml_css_attr(attr):
    return bool(re.match(r'^[-:\w]+$', attr))
def is_dynamic_attribute(name, **kwargs):
    #TODO
    return false
def is_static_attribute(options):
    pass
def is_static_classname(name, **kwargs):
    #TODO
    pass

def tabulate(tabs):
    return '  ' * tabs

setattr(BeautifulSoup, 'to_haml', to_haml_soup)
setattr(Tag, 'to_haml', to_haml_tag)
setattr(CData, 'to_haml', to_haml_cdata)
setattr(Comment, 'to_haml', to_haml_comment)
setattr(NavigableString, 'to_haml', to_haml_navigable_string)
setattr(Doctype, 'to_haml', to_haml_doctype)
