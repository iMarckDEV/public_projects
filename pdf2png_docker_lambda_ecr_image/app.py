import boto3
import os
import sys
import uuid
import json
try:
 from PIL import Image, ImageEnhance, ImageFilter
except ImportError:
 import Image
from pdf2image  import convert_from_path
#import pypdfium2 as pdfium


s3_client = boto3.client('s3')



def handler(event, context):
    #funciona por un json que contenga bucket y obj_key
    #o por un evento s3

    bucket_out=event.get("bucket_out", 'facturas-test-raw-pdf2png')

    bk0 = event.get("bucket_in", None)
    pth0 = event.get("obj_key_in", None)

    if bk0==None or pth0==None:
        ####evento
        object_key = event["Records"][0]["s3"]["object"]["key"]
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
    
        object_key=str(object_key) ###casteo a string por si acaso
    else:
        object_key=str(pth0)
        bucket=str(bk0)
    
    ####extraer el nombre del archivo
    if '/' in object_key:
        archivo_name=object_key.split('/')
        archivo_name=archivo_name[len(archivo_name)-1] ###archivo.pdf
    else:
        archivo_name=object_key

    print('PROCESANDO:{}'.format(archivo_name))

    download_path='/tmp/{}'.format(archivo_name) ##RUTA PARA PDF
    download_path_file_folder='/tmp/{}/'.format(archivo_name.replace('.pdf','')) ##RUTA PARA PDF
    print(f'folder interno salida:{download_path_file_folder}')
    s3_client.download_file(bucket, object_key, download_path)##COPIAR EL ARCHIVO  AL TEMP

    if not os.path.exists(download_path_file_folder):
        os.makedirs(download_path_file_folder)
    
    print(f'archivo a procesar:{download_path}')

    images = convert_from_path(download_path) ##la lista de imagenes
    ##save the images
    list_files_ephemeral_storage=[]
    print('guardando ephemeral storage...')
    for i, img in enumerate(images, start=1):
        image_filename = f'{download_path_file_folder}f_{i}.png'
        img.save(image_filename, 'PNG')
        list_files_ephemeral_storage.append(image_filename)

    #r_img.save('/tmp/scaled_{}'.format(archivo_name))
    """
    print(f'path ephemeral:{download_path}')
    print(os.listdir('/tmp'))
    pdf = pdfium.PdfDocument(download_path)
    
    n_pages = len(pdf)

    page_indices = [i for i in range(n_pages)]  # all pages
    renderer = pdf.render(
        pdfium.PdfBitmap.to_pil,
        page_indices = page_indices,
        scale = 300/72,  # 300dpi resolution
        n_processes=1 
    )

    n_digits = len(str(n_pages))
    print(f'pages:{n_pages}')
    print(f'renders type{type(renderer)}')

    list_files_ephemeral_storage=[]
    i=0
    for image in zip(renderer):

        image_filename = f'{download_path_file_folder}f_{n_digits}_{i}.png'
        print(image_filename)
        image.save(image_filename)
        list_files_ephemeral_storage.append(image_filename)
        i=i+1
    """
    print('>>to s3')
    for file in list_files_ephemeral_storage:
        print(file)
        s3_client.upload_file(file, bucket_out, file.replace('/tmp/',''))##COPIAR EL ARCHIVO desde tmp a s3

        os.remove(file) 
        
    ##    resize_image(download_path, upload_path)
    #s3_client.upload_file(upload_path, 'mloaiza.test','rs-{}'.format(key))



    return {
        'statusCode':200,
        'body':f'png cargados :{len(list_files_ephemeral_storage)}\n en:'}

