from core.models import FooterList

def footer_items(request):
    footer_items = FooterList.objects.all()
    return {'footer_items': footer_items}