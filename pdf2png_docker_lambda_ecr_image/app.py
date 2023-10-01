import boto3
import os
import sys
import uuid
import json
import cv2
import numpy as np

try:
 from PIL import Image, ImageEnhance, ImageFilter
except ImportError:
 import Image
from pdf2image  import convert_from_path
#import pypdfium2 as pdfium


s3_client = boto3.client('s3')

def image_rut(image_path):
    
    # Load the PNG image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise and improve contour detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use Canny edge detection to find edges in the image
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edged image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a list to store cropped images
    cropped_images = []

    # Iterate through the detected contours
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Check if the polygon has 4 vertices (indicating a rectangle)
        if len(approx) == 4:
            # Get the bounding box of the rectangle
            x, y, w, h = cv2.boundingRect(approx)

            # Crop the rectangle region from the original image
            if h>100 and w>300 and w<800 and y<300 and x>900:
                #print(f'h:{h}-w:{w}')
                cropped = image[y:y+h, x:x+w]

                # Append the cropped image to the list
                cropped_images.append(cropped)

    # Save each cropped image as a separate file
    for i, cropped in enumerate(cropped_images):

        filename = image_path.replace('.png','_rut.png')
        cv2.imwrite(filename, cropped)
        return filename

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

    list_files_ephemeral_storage2=[]
    for imag in list_files_ephemeral_storage:
        if len(imag)>5:
            rut=image_rut(imag)
            print(rut)
            list_files_ephemeral_storage2.append(rut)


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
        if file is not None:
            print(file)
            s3_client.upload_file(file, bucket_out, file.replace('/tmp/',''))##COPIAR EL ARCHIVO desde tmp a s3

            os.remove(file) 
    if len(list_files_ephemeral_storage2) >0:       
        for file in list_files_ephemeral_storage2:
            if file is not None:
                print(file)
                s3_client.upload_file(file, bucket_out, file.replace('/tmp/',''))##COPIAR EL ARCHIVO desde tmp a s3

                os.remove(file) 

    ##    resize_image(download_path, upload_path)
    #s3_client.upload_file(upload_path, 'mloaiza.test','rs-{}'.format(key))



    return {
        'statusCode':200,
        'body':f'png cargados :{len(list_files_ephemeral_storage)}\n en:'}

