#!/usr/bin/env python3

import time
import arxiv

QUERY = "cat:cs.CL AND (ti:generate OR ti:dialog OR ti:understanding)"

res = arxiv.query(query=QUERY, max_results=100, sort_by="submittedDate", sort_order="descending")


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

print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>ArXiv search results</title>
    <link rel="stylesheet" href="https://arxiv.org/css/arXiv.css">
</head>
<body class="with-cu-identity">
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
print("</body>\n</html>")
