from django.urls import path
from readPdfs.views import HomePage, DownloadPDFS, ImportDB

urlpatterns = [
    path('download/',DownloadPDFS.as_view()),
    path('import/',ImportDB.as_view()),
    path('',HomePage.as_view()),
]
