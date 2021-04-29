import requests 
from bs4 import BeautifulSoup 
import re
import os
  
''' 
URL of the archive web-page which provides link to 
all pdfs.
'''
  
# specify the URL of the archive here 
archive_url = "http://www.madrid.org/cs/Satellite?pagename=ICMFramework/Comunes/Logica/ICM_WrapperGetion&op=PCIU_&language=es&c=CM_ConvocaPrestac_FA&cid=1354822557475&nombreVb=listas&other=1"
def get_pdf_links(): 
      
    # create response object 
    r = requests.get(archive_url) 
      
    # create beautiful-soup object 
    soup = BeautifulSoup(r.content,'html.parser') 
    
    # find all links on web-page 
    links = soup.findAll('a') 
    

    # filter the link containing with PDF 
    pdf_links = ["http://www.madrid.org" + link['href'] for link in links if ('PDF' in link['href'] or 'pdf' in link['href'])] 
    
    return pdf_links 
  
  
def download_pdfs(pdf_links):   
    for link in pdf_links: 
  
        '''iterate through all links in pdf_links 
        and download them one by one'''
          
        file_name = re.findall("3D(.+?)&blobkey", link)[0].replace('+', '_')  #obtain filename

        print( "Downloading file:%s"%file_name) 
        # 'http://www.madrid.org/cs/Satellite?pagename=ICMFramework/Comunes/Logica/ICM_WrapperGetion&op=PCIU_&language=es&c=CM_ConvocaPrestac_FA&cid=1354822557475&nombreVb=listas&other=1/cs/Satellite?blobcol=urldata&blobheader=application%2Fpdf&blobheadername1=Content-Disposition&blobheadervalue1=filename%3DResol.+LP-3413736.PDF&blobkey=id&blobtable=MungoBlobs&blobwhere=1353014133075&ssbinary=true'
        # 'http://www.madrid.org/cs/Satellite?pagename=ICMFramework/Comunes/Logica/ICM_WrapperGetion&op=PCIU_&language=es&c=CM_ConvocaPrestac_FA&cid=1354822557475&nombreVb=listas&other=1/cs/Satellite?blobcol=urldata&blobheader=application%2Fpdf&blobheadername1=Content-Disposition&blobheadervalue1=filename%3DANEXO+CONCORDANCIA.pdf&blobkey=id&blobtable=MungoBlobs&blobwhere=1353014133195&ssbinary=true'
        # create response object 
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'}
        r = requests.get(link, headers=headers)
        if not os.path.exists('./reto2/pdfs/'):
            os.mkdir('./reto2/pdfs/')
        elif not os.path.isdir('./reto2/pdfs/'):
            return #you may want to throw some error or so.
        
        with open('./reto2/pdfs/'+file_name, 'wb') as f: 
            f.write(r.content)
          
        print( "%s downloaded!\n"%file_name+'\n'+link )
  
    print ("All pdfs downloaded!")
    return
  
  
if __name__ == "__main__": 
  
    # getting all video links 
    pdf_links = get_pdf_links() 
    # download all pdfs 
    download_pdfs(pdf_links) 

   