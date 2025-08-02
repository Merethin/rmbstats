# rmbstats

A script to generate dispatch BBcode containing formatted RMB post and like stats for a certain time period.

## Prerequisites

Python, version 3.13.

Create a virtual environment and install the dependencies:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

This script uses Jinja2 templates. The documentation for them can be found here: https://jinja.palletsprojects.com/en/stable/templates/, but you can get by without knowing much Jinja2 syntax and just following the example as this doesn't use many of its features.

It exposes two variables to the template: 'mostposts' (a list containing all the nations that posted in that period in descending order of posts, with a 'name' field for the nation and a 'posts' field for the number of posts) and 'mostliked' (a list containing all the nations that have received likes in that period in descending order of likes received, with a 'name' field for the nation and a 'likes' field for the number of likes received).

An example template looks like this (can be found in templates/example.jinja2):
```
[b]Most RMB Posts[/b]

[table]
[tr][th]Nation[/th][th]Posts[/th][/tr]
{% for nation in mostposts %}[tr][td][nation]{{ nation.name }}[/nation][/td][td]{{ nation.posts }}[/td][/tr]{% endfor %}
[/table]

[b]Most RMB Likes Received[/b]

[table]
[tr][th]Nation[/th][th]Likes[/th][/tr]
{% for nation in mostliked %}[tr][td][nation]{{ nation.name }}[/nation][/td][td]{{ nation.likes }}[/td][/tr]{% endfor %}
[/table]
```

The BBCode between each {% for %} and {% endfor %} block is repeated for every nation. {{ nation.name }} and {{ nation.likes/posts }} are replaced with the actual values for every nation. Apart from that, you can add whichever BBCode you want and insert the data wherever you want.

The template you create must be placed in the `templates` folder.

After creating the template, run `main.py` and follow the instructions.