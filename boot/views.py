from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
# Create your views here.

def index(request):
    return render(request,'index.html')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    return (
        None
        if pdf.err
        else HttpResponse(result.getvalue(), content_type='application/pdf')
    )


data = {
    "company": "Suprit Kumar Company",
    "address": "123 Street name",
    "city": "Banglore",
    "state": "KTK",
    "zipcode": "560078",

    "phone": "999-555-2945",
    "email": "youremail@supritkumar.com",
    "website": "skumar.com",
}


# Opens up page as PDF
class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        pdf = render_to_pdf('pdf_template.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


# Automaticly downloads to PDF file
class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        pdf = render_to_pdf('pdf_template.html', data)

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = 'Invoice_12341231.pdf'
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response