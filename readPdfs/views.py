from django.shortcuts import render
from django.views.generic import TemplateView
from django.template import Context
from reto2.scripts.readPdf import readAdmitted, readExcluded
from reto2.scripts.downloadLinks import download_pdfs
import pandas as pd
from readPdfs.models import Access, Corp, DAT, Exclusion, Specialty, Teacher


# Create your views here.
class HomePage(TemplateView):
    template_name='homePage.html'


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,context={"Info": "Bienvenido",})
    pass

class DownloadPDFS(TemplateView):
    template_name='homePage.html'
    def get(self, request, *args, **kwargs):
        download_pdfs()
        return render(request, self.template_name, context={"Info":"'All PDFs downloaded'",})
    pass

class ImportDB(TemplateView):
    template_name='homePage.html'
    
    def get(self, request, *args, **kwargs):
        admitted = readAdmitted()
        excluded, exclusions = readExcluded()
        for _, row in admitted.iterrows():
            try:
                a = Access(code=row['ACCESO'])
                a.save()
            except:
                pass
            try:
                a = Corp(code=row['CUERPO'][:4],name=row['CUERPO'][7:])
                a.save()
            except:
                pass

            t = Teacher(first_name=row['NOMBRE'],
                        first_last_name=row['PRIMER APELLIDO'],
                        second_last_name=row['SEGUNDO APELLIDO'],
                        dni=row['D.N.I.'],
                        l_inte=row['L.INTE'],
                        language_test=row['PRUEBA IDIOMA'],
                        admitted=True,
                        specialty=Specialty.objects.get_or_create(name=row['ESPECIALIDAD'])[0],
                        corp= Corp.objects.get(code=row['CUERPO'][:4]),
                        access= Access.objects.get(code=row['ACCESO'])
                        )
            t.save()
        
        for _, row in exclusions.iterrows():
            try:
                e = Exclusion(name=row['DESCRIPCIÓN'],code=int(row['CÓDIGO']))
                e.save()
            except:
                pass


        for _, row in excluded.iterrows():
            try:
                a = Access(code=row['ACCESO'])
                a.save()
            except:
                pass
            try:
                
                a = DAT(name=row['D.A.T.'])
                a.save()
            except:
                pass

            t = Teacher(first_name=row['NOMBRE'],
                        first_last_name=row['PRIMER APELLIDO'],
                        second_last_name=row['SEGUNDO APELLIDO'],
                        dni=row['D.N.I.'],
                        l_inte=row['L. INTER'],
                        language_test=row['PR. IDIOM'],
                        admitted=False,
                        specialty=Specialty.objects.get_or_create(name=row['ESPECIALIDAD'])[0],
                        access= Access.objects.get_or_create(code=row['ACCESO'])[0]
                        )
            t.save()
            for ex in row['EXCLUSIONES'].split():
                print(Exclusion.objects.get_or_create(code=ex)[0])
                t.exclusion.add(Exclusion.objects.get_or_create(code=ex)[0])
        return render(request, self.template_name, context={"Info":"'Data loaded to DB'",})
    pass