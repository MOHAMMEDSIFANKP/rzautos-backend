from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

def generate_pdf(template_src, context_dict={}):
    try:
        template = get_template(template_src)
        html = template.render(context_dict)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="downloadpdf.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
    except Exception as e:
        print(e)
    return response
