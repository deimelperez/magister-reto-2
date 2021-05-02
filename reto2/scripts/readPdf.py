from tabula import read_pdf
import PyPDF2
import pandas as pd
import os
import re


# Reads Tables from files
def readTables(path_file, table,columns,start_page, end_page=False):
    '''
        Return a list of pandas Data Frames with the tables

        path_file: Path to file
        table: [top, left, bottom, width] in cm where the table is located
        columns (list): X coordinates of column boundaries.
        start_page: page where the tables start
        end_page: page where the tables end
    '''
    # creating an object 
    file = open(path_file, 'rb')

    # creating a pdf reader object
    fileReader = PyPDF2.PdfFileReader(file)

    # get the number of pages in pdf file
    if not end_page:
        numPages = fileReader.numPages 
    else:
        numPages = end_page

    # creates list of pages
    arrPages = [i for i in range(start_page, numPages + 1)]

    # create box where the table is in
    box = table
    fc = 28.28
            
    for i in range(0, len(box)):
        box[i] *= fc
    for i in range(0, len(columns)):
        columns[i] *= fc

    return read_pdf(path_file,columns=columns, pages=arrPages, area=box)


# Reads all files and all tables and returns it
def readAdmitted():                   
    # Change the directory
    os.chdir('./reto2/pdfs')
    path = os.getcwd()
    df_list = []
    df_list2 = []
    df_result = pd.DataFrame()

    # iterate through all file
    for file in os.listdir():
        # Check if contains tables or not
        if 'ADMITIDOS' in file:      
            file_path = f"{path}\{file}"
            df_pages = readTables(file_path,[5,0,26,21],[3,7,12,15.5,17.5,21],2)
            # open the pdf file
            fileReader = PyPDF2.PdfFileReader(file)
            # get number of pages
            NumPages = fileReader.getNumPages()

            # define keyterms
            # extract text and do the search
            other_data = []

            for i in range(1, NumPages):
                PageObj = fileReader.getPage(i)
                Text = PageObj.extractText()

                cuerpo = re.findall('CUERPO:(.*)ESPECIALIDAD:', Text)[0].strip()
                especialidad = re.findall('ESPECIALIDAD:(.*)ACCESO:', Text)[0].strip()
                acceso =  re.findall('ACCESO:(.*\d.*) -', Text)[0].strip()

                other_data.append({'CUERPO':cuerpo,'ESPECIALIDAD':especialidad,'ACCESO':acceso})
            df_list.append(df_pages)
            df_list2.append(other_data)
    dfs = []
    for i in range(len(df_list)):    
        for j in range(len(df_list[i])):
            df_list[i][j]['CUERPO'] = df_list2[i][j]['CUERPO']
            df_list[i][j]['ESPECIALIDAD'] = df_list2[i][j]['ESPECIALIDAD']
            df_list[i][j]['ACCESO'] = df_list2[i][j]['ACCESO']
            dfs.append(df_list[i][j])

    
    df_result = df_result.append(other=dfs)
    # Change index
    df_result['index'] = range(0,len(df_result))
    df_result.set_index('index', inplace=True)

    return df_result


def readExcluded():                   
    # Change the directory
    # if not './reto2/pdfs' in os.getcwd():
    # os.chdir('./reto2/pdfs')
    path = os.getcwd()

    # Variable to get the exclusions description
    readed = False


    df_result = pd.DataFrame()
    df_exclusions = pd.DataFrame()

    # iterate through all file
    for file in os.listdir():
        # Check if contains tables or not
        if 'EXCLU' in file:
            file_path = f"{path}\{file}"
            if not readed:
                df_exclusions = readTables(file_path, [3.5,0,19,29],[1.7,28], 2,3)
                readed = True
            
            df_result = df_result.append(other=readTables(file_path, [4,0,19,28.5],[2.5, 9.7, 13.5, 15.5, 16.7, 21.5, 23, 28], 4))
    
    # Change index
    df_result['index'] = range(0,len(df_result))
    df_result.set_index('index', inplace=True)

    # Fixes row misread of tabula
    enter = -1
    for i, _ in df_result.iterrows():
        # Checks when dni is NaN because is a signal of row misread
        if str(df_result.loc[i, 'D.N.I.']) == 'nan' and i > 0 and i < len(df_result) - 1 and i != enter:  

            # Checks when dni in next position is NaN because is a signal of row misread 
            if str(df_result.loc[i + 1, 'D.N.I.']) == 'nan':
                # Variable to not reenter when misread rows == 3
                enter = i + 1
                df_result.loc[i-1, 'ESPECIALIDAD'] += ' ' + str(df_result.loc[i, 'ESPECIALIDAD']) + ' ' + str(df_result.loc[i + 1, 'ESPECIALIDAD'])
            else:
                df_result.loc[i-1, 'APELLIDOS Y NOMBRE'] += str(df_result.loc[i, 'APELLIDOS Y NOMBRE']) if str(df_result.loc[i, 'APELLIDOS Y NOMBRE']) != 'nan' else ''
                df_result.loc[i-1, 'ESPECIALIDAD'] += ' ' + str(df_result.loc[i, 'ESPECIALIDAD']) if str(df_result.loc[i, 'ESPECIALIDAD']) != 'nan' else ''
    
    # Drops rows misreaded
    df_result = df_result.dropna(subset=['D.N.I.'])
    
    
    for i in df_result.index:
        df_result.loc[i,'NOMBRE'] = df_result.loc[i,'APELLIDOS Y NOMBRE'].split(",")[1].strip()
        df_result.loc[i,'PRIMER APELLIDO'] = df_result.loc[i,'APELLIDOS Y NOMBRE'].split(",")[0].strip().split()[0]
        df_result.loc[i,'SEGUNDO APELLIDO'] = ' '.join(df_result.loc[i,'APELLIDOS Y NOMBRE'].split(",")[0].strip().split()[1:])
    # Eliminates columns misreaded
    df_result = df_result.drop(labels=['APELLIDOS Y NOMBRE'], axis=1)

    # Sorts columns
    df_result = df_result[['D.N.I.','PRIMER APELLIDO','SEGUNDO APELLIDO', 'NOMBRE', 'D.A.T.', 'PR. IDIOM', 'ACCESO','ESPECIALIDAD','L. INTER', 'EXCLUSIONES']]

    
    df1 = df_exclusions[0]
    df2 = df_exclusions[1]

    row = pd.Series({'CÓDIGO':df2.columns[0],'DESCRIPCIÓN':df2.columns[1]}, name=df2.columns[0])
    df1 = df1.append(other=row)

    df2['CÓDIGO'] = df2[df2.columns[0]]
    df2['DESCRIPCIÓN'] = df2[df2.columns[1]]
    df2 = df2.drop(labels=[df2.columns[0],df2.columns[1]],axis=1)
    df1 = df1.append(other=df2)
    df1['index'] = range(0,len(df1))
    df_exclusions = df1.set_index('index')
    clear = lambda: os.system('cls')
    clear()

    return (df_result,df_exclusions)
