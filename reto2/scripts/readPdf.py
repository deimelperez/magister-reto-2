from tabula import read_pdf
import PyPDF2
import pandas as pd
import os


# Reads Tables from files
def readTables(path_file, table,start_page, end_page=False):
    '''
        Return a list of pandas Data Frames with the tables

        path_file: Path to file
        table: [top, left, bottom, width] in cm where the table is located
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

    return read_pdf(path_file, pages=arrPages, area=box)


# Reads all files and all tables and returns it
def readAdmitted():                   
    # Change the directory
    os.chdir('./reto2/pdfs')
    path = os.getcwd()

    df_result = pd.DataFrame()

    # iterate through all file
    for file in os.listdir():
        # Check if contains tables or not
        if 'ADMITIDOS' in file:      
            file_path = f"{path}\{file}"
            df_result = df_result.append(other=readTables(file_path,[5,0,26,21],2))
    
    # Combines columns that were misreaded with tabula
    df_result["NOMBRE"] = df_result["NOMBRE"].combine_first(df_result["NOMBRE L.INTE"])
    df_result["L.INTE"] = df_result["L.INTE"].combine_first(df_result["Unnamed: 0"])
    df_result["PRIMER APELLIDO"] = df_result["PRIMER APELLIDO"].combine_first(df_result["PRIMER APELLIDO  SEGUNDO APELLIDO"])

    # Drops columns that were misreaded with tabula
    df_result = df_result.drop(labels=["PRIMER APELLIDO  SEGUNDO APELLIDO","NOMBRE L.INTE","Unnamed: 0"],axis=1)

    return df_result


def readExcluded():                   
    # Change the directory
    os.chdir('../pdfs')
    path = os.getcwd()

    # Variable to get the exclusions description
    readed = False


    df_result = pd.DataFrame()
    df_exlusions = pd.DataFrame()

    # iterate through all file
    for file in os.listdir():
        # Check if contains tables or not
        if 'EXCLU' in file:
            file_path = f"{path}\{file}"
            if not readed:
                df_exlusions = readTables(file_path, [3.5,0,19,29], 2, 3)
                readed = True
            df_result = df_result.append(other=readTables(file_path, [4,0,19,28.5], 4))
    
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
                df_result.loc[i-1, 'PR. IDIOM  ACCESO  ESPECIALIDAD'] += ' ' + str(df_result.loc[i, 'PR. IDIOM  ACCESO  ESPECIALIDAD']) + ' ' + str(df_result.loc[i + 1, 'PR. IDIOM  ACCESO  ESPECIALIDAD'])
            else:
                df_result.loc[i-1, 'APELLIDOS Y NOMBRE'] += str(df_result.loc[i, 'APELLIDOS Y NOMBRE']) if str(df_result.loc[i, 'APELLIDOS Y NOMBRE']) != 'nan' else ''
                df_result.loc[i-1, 'PR. IDIOM  ACCESO  ESPECIALIDAD'] += ' ' + str(df_result.loc[i, 'PR. IDIOM  ACCESO  ESPECIALIDAD']) if str(df_result.loc[i, 'PR. IDIOM  ACCESO  ESPECIALIDAD']) != 'nan' else ''
    
    # Drops rows misreaded
    df_result = df_result.dropna(subset=['D.N.I.'])
    
    # Separates columns misreaded by tabula and appends it the df
    df_result['ACCESO'] = df_result['PR. IDIOM  ACCESO  ESPECIALIDAD'].str.split(" ",expand=True,)[0]
    
    for i in df_result.index:
        df_result.loc[i,'ESPECIALIDAD'] = ' '.join(df_result.loc[i,'PR. IDIOM  ACCESO  ESPECIALIDAD'].split(" ")[1:])
        df_result.loc[i,'NOMBRE'] = df_result.loc[i,'APELLIDOS Y NOMBRE'].split(",")[1].strip()
        df_result.loc[i,'PRIMER APELLIDO'] = df_result.loc[i,'APELLIDOS Y NOMBRE'].split(",")[0].strip().split()[0]
        df_result.loc[i,'SEGUNDO APELLIDO'] = ' '.join(df_result.loc[i,'APELLIDOS Y NOMBRE'].split(",")[0].strip().split()[1:])
    # Eliminates columns misreaded
    df_result = df_result.drop(labels=['APELLIDOS Y NOMBRE','PR. IDIOM  ACCESO  ESPECIALIDAD','Unnamed: 0','Unnamed: 1'], axis=1)

    # Sorts columns
    df_result = df_result[['D.N.I.','PRIMER APELLIDO','SEGUNDO APELLIDO', 'NOMBRE', 'D.A.T.', 'ACCESO','ESPECIALIDAD','L. INTER', 'EXCLUSIONES']]


    
    return (df_result,df_exlusions)
