import re
from django.conf import settings
from django.db.models import Q
from string import Formatter

def site_title(request):
  title = settings.SITE_NAME.title()
  return {'site_title':title}

def admin_site_header(request):
  admin_header = settings.SITE_NAME.title() + " administration"
  return {'site_header':admin_header}

# Splits the query string in invidual keywords, getting rid of unecessary spaces
# and grouping quoted words together.
# Example:
# >>> normalize_query('  some random  words "with   quotes  " and   spaces')
# ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
  return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

# Returns a query, that is a combination of Q objects. That combination
# aims to search keywords within a model by testing the given search fields.
def get_query(query_string, search_fields):
  query = None # Query to search for every search term
  terms = normalize_query(query_string)
  for term in terms:
    or_query = None # Query to search for a given term in each field
    for field_name in search_fields:
      q = Q(**{"%s__icontains" % field_name: term})
      if or_query is None:
        or_query = q
      else:
        or_query = or_query | q
    if query is None:
      query = or_query
    else:
      query = query & or_query
  return query

# returns timedelta acording to format
# format smples:
# "{D} days {H}:{M}:{S}"
# "{H} hours and {M} to go"
#"{H:02}h{M:02}m{S:02}s"
def strfdelta(tdelta, fmt):
    f = Formatter()
    d = {}
    l = {'D': 86400, 'H': 3600, 'M': 60, 'S': 1}
    k = map( lambda x: x[1], list(f.parse(fmt)))
    rem = int(tdelta.total_seconds())

    for i in ('D', 'H', 'M', 'S'):
        if i in k and i in l.keys():
            d[i], rem = divmod(rem, l[i])

    return f.format(fmt, **d)