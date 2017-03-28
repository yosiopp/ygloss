#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import copy
import re
import yaml
from datetime import datetime

TEMPLATE_FILE='tmpl.html'
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

def split_frontmatter(lines):
    n = 0
    if lines[0].strip() != '---':
        return ('', ''.join(lines))
    else:
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                n = i + 1
                break
    return (''.join(lines[1:n-1]), ''.join(lines[n:]))

def merge_dict(_base, _dict):
    try:
        _base.update(_dict)
    except:
        pass
    return _base

def curfile(file):
    return os.path.join(os.path.dirname(__file__), file)


## main

if len(sys.argv) < 2:
    sys.stderr.write('Illegal Argument: please specify the yaml for converted.\n')
    sys.exit(1)

lines = open(sys.argv[1], 'r').readlines()
frontmatter, body = split_frontmatter(lines)

fm = merge_dict({
    'lang': 'en',
    'title': '',
    'description': '',
    'date': datetime.now().isoformat()
}, yaml.load(frontmatter))
gloss = yaml.load(body)

items = []
indexes = []
keywords = sorted(gloss.keys(), key=lambda x: len(x), reverse=True)

for k, v in gloss.items():
    indexes.append(TMPL_INDEX % (k, k))
    v = v.strip().replace("\n","<br>\n")
    # replace keywords
    for i in range(len(keywords)):
        v = v.replace(keywords[i], '{{ #KEYWORD#%d }}' % i)
    for i in range(len(keywords)):
        v = v.replace('{{ #KEYWORD#%d }}' % i, '<a href="#%s">%s</a>' % (keywords[i], keywords[i]))
    # replace link
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
tmpl = open(curfile(TEMPLATE_FILE)).read()

print replace(tmpl, data)