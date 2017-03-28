#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import copy
import yaml
import re
from datetime import datetime

TMPL_INDEX='<li><a href="#%s">%s</a></li>'
TMPL_ITEM='<dl id="%s"><dt>%s</dt><dd>%s</dd></dl>'

def replace(src, _dict):
    dest = copy.copy(src)
    for k, v in _dict.items():
        dest = dest.replace(k, v)
    return dest

# TODO proc front matter
lines = open(sys.argv[1], 'r').readlines()
n = 5
body = ''.join(lines[n:])
gloss = yaml.load(body)

items = []
indexes = []
keywords = sorted(gloss.keys(), key=lambda x: len(x), reverse=True)

for k, v in gloss.items():
    indexes.append(TMPL_INDEX % (k, k))
    v = v.strip().replace("\n","<br>\n")
    for i in range(len(keywords)):
        v = v.replace(keywords[i], '{{ #KEYWORD#%d }}' % i)
    for i in range(len(keywords)):
        v = v.replace('{{ #KEYWORD#%d }}' % i, '<a href="#%s">%s</a>' % (keywords[i], keywords[i]))
    v = re.sub(r"(https?:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:@&=+$,%#]+)", '<a href="\\1" target="_blank">\\1</a>', v)
    items.append(TMPL_ITEM % (k, k, v))

data = {
    '${fm_lang}': 'ja', # TODO 
    '${fm_title}': 'glossary', # TODO
    '${fm_description}': '', # TODO
    '${fm_date}': datetime.now().isoformat(),
    '${indexes}': "\n".join(sorted(indexes)).encode('utf-8'),
    '${items}': "\n".join(sorted(items)).encode('utf-8')
}
tmpl = open('tmpl.html').read()

print replace(tmpl, data)