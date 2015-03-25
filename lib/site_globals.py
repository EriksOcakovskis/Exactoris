from django.conf import settings

def site_title(request):
  title = settings.SITE_NAME.title()
  return {'site_title':title}
