#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import copy
import yaml
import re
from datetime import datetime

TMPL_INDEX='<li><a href="#%s">%s</a></li>'
TMPL_ITEM='<dl id="%s"><dt>%s</dt><dd>%s</dd></dl>'

def encode_dict(_dict, enc):
    for k, v in _dict.items():
        k = k.encode(enc)
        v = v.encode(enc)
    return _dict

def replace(src, _dict):
    dest = copy.copy(src)
    for k, v in _dict.items():
        dest = dest.replace(k, v)
    return dest

# proc front matter
n = 0
lines = open(sys.argv[1], 'r').readlines()
if lines[0].strip() == '---':
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            n = i
            break

fm = { "lang": '', "title": '', "description": '', "date": datetime.now().isoformat()}
try:
    fm.update(yaml.load(''.join(lines[1:n])))
except:
    pass
body = ''.join(lines[n+1:])
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

data = encode_dict({
    '${fm_lang}': fm['lang'],
    '${fm_title}': fm['title'],
    '${fm_description}': fm['description'],
    '${fm_date}': fm['date'],
    '${indexes}': "\n".join(sorted(indexes)),
    '${items}': "\n".join(sorted(items))
}, 'utf-8')
tmpl = open('tmpl.html').read()

print replace(tmpl, data)