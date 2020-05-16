#!/usr/bin/env python3

import cgi
import time
import arxiv
import os
import sys
import urllib

QUERY = "cat:cs.CL AND (ti:generate OR ti:dialog OR ti:understanding)"


def cgi_to_dict():
    """ Get a plain dictionary rather than the '.value' system used by the
    cgi module's native fieldStorage class. """
    cgi_storage = cgi.FieldStorage()
    params = {}
    for key in cgi_storage.keys():
        params[key] = cgi_storage[key].value
    return params


def get_item_html(arxiv_id, title, authors, comments):
    html = f"""
<dt><span class="list-identifier"><a href="https://arxiv.org/abs/{arxiv_id}" title="Abstract">arXiv:{arxiv_id}</a></span></dt>
<dd>
<div class="meta">
<div class="list-title mathjax"><span class="descriptor">Title:</span> {title}</div>
<div class="list-authors"><span class="descriptor">Authors:</span> {authors} </div>
    """
    if comments:
        html += f"""<div class="list-comments mathjax"><span class="descriptor">Comments:</span> {comments}</div>"""
    html += """
</div>
</dd>
    """
    return html

def print_links(query, lenght, position):
    """Print forward and backward links"""
    print("<div>")
    if position > 0:
        print('<a href="?start=%d&amp;length=%d&amp;query=%s"">&lt;&lt; Later</a> ' % (max(0, position - 50), length, urllib.parse.quote(query)))
    print('<a href="?start=%d&amp;length=%d&amp;query=%s">Earlier &gt;&gt;</a> ' % (position + 50, length, urllib.parse.quote(query)))
    print("</div>")


if 'GATEWAY_INTERFACE' in os.environ:
    args = cgi_to_dict()
else:
    args = dict(arg.split('=') for arg in sys.argv[1:])


#
## Main
#

start = int(args.get('start', 0))
length = int(args.get('length', 50))
query = args.get('query', QUERY)
res = arxiv.query(query=query, max_results=50, sort_by="submittedDate", sort_order="descending", start=start)

print(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>ArXiv search results</title>
    <link rel="stylesheet" href="https://arxiv.org/css/arXiv.css">
</head>
<body class="with-cu-identity">
<div id="header">
<h1>arXiv.org – {query} – start={start}</h1>
</div>""")
print_links(query, start, length)
print("""
<div id="content">
<div id="dlpage">
      """)

last_date = None
for entry in res:
    entry_date = time.strftime('%Y-%m-%d', entry['published_parsed'])
    if entry_date != last_date:
        if last_date:
            print("</dl>")
        print("""<h3>%s</h3>\n<dl>""" % time.strftime('%a, %d %b %Y', entry['published_parsed']))
        last_date = entry_date
    arxiv_id = entry['id'].split('/')[-1]
    authors = ', '.join(entry['authors'])
    print(get_item_html(arxiv_id, entry['title'], authors, entry['arxiv_comment']))

print("</dl>\n</div>\n</div>")
print_links(query, start, length)
print('<footer style="clear: both"></footer>')
print("</body>\n</html>")
