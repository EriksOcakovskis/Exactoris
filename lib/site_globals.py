from django.conf import settings

def site_title(request):
  title = settings.SITE_NAME.title()
  return {'site_title':title}

def admin_site_header(request):
  admin_header = settings.SITE_NAME.title() + " administration"
  return {'site_header':admin_header}
