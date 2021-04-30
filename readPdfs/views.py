from django.shortcuts import render
from django.views.generic import TemplateView
from reto2.scripts.readPdf import readAdmitted, readExcluded
from reto2.scripts.downloadLinks import download_pdfs


# Create your views here.
class ReadPdf(TemplateView):
    template_name='homePage.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'Download':download_pdfs(),'Admitted': readAdmitted(), 'Excluded':readExcluded()})
    pass

