# Use list compomprehension for string concatenation http://www.skymind.com/~ocrow/python_string/
from bs4 import Tag, CData, Comment, Tag, NavigableString, Doctype, BeautifulSoup
import re
import cgi
try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser


CLOSED_TAG_REGEX = re.compile(r'(?P<leftspace>\s*){%\s*(?P<opentagcontent>(?P<tag>[^\s%}]+)[^%}]*)\s+%}\n{0,1}(?P<content>.*?){%[^%}]*?end(?P=tag).*?%}(?P<rightspace>\n*)', re.DOTALL)
VARIABLE_REGEX = re.compile(r'(?P<leftspace>\s*){{\s*(?P<content>[^\{\}]+?)\s*}}(?P<rightspace>\s*)', re.DOTALL)
SELF_CLOSED_TAG_REGEX = re.compile(r'(?P<leftspace>\s*){%\s*(?P<content>(?P<tag>[^\s]+)[^%}]*)\s+%}\n{0,1}(?![^%}]*{%.*?end(?P=tag).*?%}\n*)', re.DOTALL)

def closed_tag_to_dynamic(matchobj):
    leftspace = matchobj.group('leftspace')
    content = matchobj.group('content')
    rightspace = matchobj.group('rightspace')
    opentagcontent = matchobj.group('opentagcontent')
    return "%s<dynamic dynamic=\"%s\">%s</dynamic>%s" % (leftspace, opentagcontent, content, rightspace)

def self_closed_tag_to_dynamic(matchobj):
    leftspace = matchobj.group('leftspace')
    content = matchobj.group('content')

    return "%s<dynamic dynamic=\"%s\"/>" % (leftspace, content)

class Converter:
    def __init__(self, *args, **kwargs):

        text = args[0]
        while(len(CLOSED_TAG_REGEX.findall(text)) > 0):
            text = re.sub(CLOSED_TAG_REGEX, closed_tag_to_dynamic, text)
        text = re.sub(SELF_CLOSED_TAG_REGEX, self_closed_tag_to_dynamic, text)

        self.soup = BeautifulSoup(text, *args[1:], **kwargs)

    def to_haml(self):
        return self.soup.to_haml()

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
    if (self.name == "dynamic"):
        output += ("- %s") % self.attrs['dynamic']
    elif (not
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
            leftover = [ s for s in filter(lambda c: not is_haml_css_attr(c), self.attrs['class']) ]
            del self.attrs['class']
            if any(leftover) : self.attrs['class'] = ' '.join(leftover)
    if len(self.attrs) > 0: output += haml_attributes(**kwargs)
    if self.isSelfClosing : output += "/"

    if len(list(self.children)) == 1:
        child = next(self.children)
        if isinstance(child, NavigableString):
          if not ("\n" in child):
            text = child.to_haml(tabs + 1, **kwargs)
            if not( not text or "\n" in chomp(text) ) : return output + " " + text.lstrip()
            return output + "\n" + text

    return render_children( output + "\n", tabs, **kwargs)

def render_children(so_far, tabs, **kwargs):
    instance = kwargs['instance']
    return so_far + ''.join(child.to_haml(tabs=tabs + 1) for child in (instance.children or []))


def chomp(text):
    return re.sub(r'[\n|\r\n|\r]$', '', text, count=1)

def escape_html_except_for_dynamic(soup):
    if not soup.body: return
    for c in soup.body.children:
        children = []
        children.append(c)
        while(len(children) > 0 and c != None):
            c = children.pop(0)
            if isinstance(c, Tag):
                if not c.is_dynamic:
                    c.replace_with("\n"+cgi.escape(str(c)))
                [children.append(c) for c in c.children]
            else:
                c.replace_with("\n"+cgi.escape(str(c)))


def convert_dynamic_to_haml(soup, tabs=0):
    if not soup.body: return ''
    escape_html_except_for_dynamic(soup)
    for c in soup.find_all("dynamic"): c.replace_with(c.to_haml(tabs=tabs))
    return decode_entities(''.join(soup.body.contents))


def to_haml_cdata(self, tabs):
    #TODO
    # handle dynamic content
    # https://github.com/haml/html2haml/blob/01c0bd0a2ee059f6482ef7185860664b0724cf23/lib/html2haml/html.rb#L205
    content = parse_text(self.string, tabs + 1)

    if BeautifulSoup(content).find_all("dynamic"):
        content = convert_dynamic_to_haml(BeautifulSoup(content), tabs=tabs+1)

    return "%s:cdata\n%s" % (tabulate(tabs), content)

def content_without_cdata_tokens(text):
    CDATA_OPEN_TAG_REGEX = re.compile(r'^\s*<!\[CDATA\[\n', flags = re.MULTILINE)
    CDATA_CLOSE_TAG_REGEX = re.compile(r'^\s*\]\]>\n', flags = re.MULTILINE)
    content = CDATA_OPEN_TAG_REGEX.sub("", text)
    content =  CDATA_CLOSE_TAG_REGEX.sub("", content)
    return content

def to_haml_navigable_string(self, tabs, **kwargs):
    if self.strip() == "" : return  ""
    return parse_text(self, tabs)
def to_haml_comment(self, tabs):
    condition, content = '', self.string
    match = re.search(r'\A(\[[^\]]+\])>(.*)<!\[endif\]\Z', content, re.MULTILINE | re.DOTALL)
    if match :
        condition = match.group(1)
        content = match.group(2)
    if '\n' in self.string:
        return "%s/%s\n%s" % (tabulate(tabs), condition, parse_text(content.strip(), tabs+1))
    else:
        return "%s/%s %s\n" % (tabulate(tabs), condition, content.strip())
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

def is_static_attribute(name, **kwargs):
    instance = kwargs['instance']
    return name in instance.attrs and not is_dynamic_attribute(name, **kwargs)

def is_static_classname(**kwargs):
    return is_static_attribute('class', **kwargs)

def is_dynamic_attribute(name, **kwargs):
    instance = kwargs['instance']
    return instance.is_dynamic

def to_haml_filter(filter, tabs, **kwargs):
    instance = kwargs['instance']

    content = instance.text
    if re.match(r'\s*<!\[CDATA\[(.*)\]\]>', instance.text, re.DOTALL | re.MULTILINE):
        content = content_without_cdata_tokens(content)
    else:
        content = decode_entities(content)

    soup = BeautifulSoup(content)
    if soup.body and soup.body.p : soup.body.p.replace_with(content)
    content = convert_dynamic_to_haml(soup, tabs=tabs+1)

    content = re.sub(r'\A\s*\n(\s*)','\g<1>', content)
    original_indent = re.match(r'\A(\s*)', content).group()

    if all( map(lambda line: len(line.strip()) == 0 or re.match('^'+original_indent, line), content.split('\n')) ):
         ORIGINAL_INDENT_REGEX = re.compile('^'+original_indent, flags = re.MULTILINE)
         content = ORIGINAL_INDENT_REGEX.sub(tabulate(tabs + 1), content)
    else:
        # Indentation is inconsistent. Strip whitespace from start and indent all
        # to ensure valid Haml
        # https://github.com/haml/html2haml/blob/c41cb712816d2ea4300e7c1730328a59a63b2ba7/lib/html2haml/html.rb#L453
        EMPTY_INDENT_REGEX = re.compile(r'^', flags=re.MULTILINE)
        content = content.lstrip()
        content = EMPTY_INDENT_REGEX.sub(tabulate(tabs + 1), content)
    content = translate_text_to_variable_haml(content)
    content = content.rstrip()
    content += "\n"

    return "%s:%s\n%s" % (tabulate(tabs), filter, content)

def haml_attributes(**kwargs):
    instance = kwargs['instance']
    if instance.is_dynamic: return ''
    attrs = map(lambda kv_pair : haml_attribute_pair(kv_pair[0], kv_pair[1]), instance.attrs.items())
    return "{%s}" % ', '.join(attrs)

def haml_attribute_pair(name, value, **kwargs):
    return "%s:\"%s\"" % (name, parse_text(value, tabs=0).rstrip())

def tabulate(tabs):
    return '  ' * tabs

def variable_object_to_haml(matchobj, inline=False, **kwargs):
    rightspace = matchobj.group('rightspace')
    leftspace = matchobj.group('leftspace')
    if inline:
        return "%s={%s}%s" % (leftspace, matchobj.group('content'), rightspace)
    else:
        return "%s= %s%s" % (leftspace, matchobj.group('content'), rightspace)
def variable_object_to_haml_generator(inline=False, **kwargs):
    return lambda matchobj, inline=inline: variable_object_to_haml(matchobj, inline, **kwargs)

def translate_text_to_variable_haml(text, **kwargs):
    instance = kwargs.pop('instance', None)
    inline_variable = len(VARIABLE_REGEX.findall(text)) > 0
    variable_match = VARIABLE_REGEX.match(text)
    if variable_match:
        text = re.sub(VARIABLE_REGEX, variable_object_to_haml_generator(), text)
    elif inline_variable:
        text = re.sub(VARIABLE_REGEX, variable_object_to_haml_generator(inline=True), text)
    return text

def parse_text(text, tabs, **kwargs):
    text = text.strip()
    if not text : return ""
    lines = []
    match = CLOSED_TAG_REGEX.match(text)
    if match : tabs += 1
    for line in text.split('\n'):
        line = translate_text_to_variable_haml(line).strip()
        lines.append("%s%s\n" %(tabulate(tabs), line))
    text = ''.join(lines)

    match = CLOSED_TAG_REGEX.match(text)
    if match :
        tag = match.group('tag')
        content = match.group('content')
        text = "- %s\n%s\n" %(tag, content)
    return text

def decode_entities(text):
    # http://stackoverflow.com/a/2087433/1123985
    return HTMLParser().unescape(text)

@property
def is_dynamic(self):
    return self.name == "dynamic"

setattr(BeautifulSoup, 'to_haml', to_haml_soup)
setattr(Tag, 'to_haml', to_haml_tag)
setattr(Tag, 'is_dynamic', is_dynamic)
setattr(CData, 'to_haml', to_haml_cdata)
setattr(Comment, 'to_haml', to_haml_comment)
setattr(NavigableString, 'to_haml', to_haml_navigable_string)
setattr(Doctype, 'to_haml', to_haml_doctype)
