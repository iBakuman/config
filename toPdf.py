# import os
# from fpdf import FPDF
# from PIL import Image
#
# pdf = FPDF()
# pdf.set_auto_page_break(0)  # 自动分页设为False
#
# path = r"E:\tmp"
# imagelist = [i for i in os.listdir(path)]
#
# for imageName in sorted(imagelist):
#     image_path = path + '\\' + imageName
#     img = Image.open(image_path)
#     aspectRatio = img.width / img.height
#     h = 150
#     w = aspectRatio * h
#     print(h, w)
#     pdf.add_page()
#     pdf.image(os.path.join(path, imageName), w=w, h=h)  # 指定宽高
#
# pdf.output(os.path.join(path, "佩奇.pdf"), "F")

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak
from reportlab.lib.pagesizes import A4, A3, A2, A1, legal, landscape
from reportlab.lib.utils import ImageReader
import PIL.Image, PIL.ExifTags
from os import listdir
import os, re
import time
from reportlab.lib.units import inch


def img_search(mypath, filenames):
    for lists in os.listdir(mypath):
        path = os.path.join(mypath, lists)
        if os.path.isfile(path):
            expression = r'[\w]+\.(jpg|png|jpeg)$'
            if re.search(expression, path, re.IGNORECASE):
                filenames.append(path)
        elif os.path.isdir(path):
            img_search(path, filenames)


def img_search1(mypath, filenames):
    for lists in os.listdir(mypath):
        path = os.path.join(mypath, lists)
        if os.path.isfile(path):
            a = path.split('.')
            if a[-1] in ['jpg', 'png', 'JPEG']:
                filenames.append(path)
        elif os.path.isdir(path):
            img_search1(path, filenames)


def rotate_img_to_proper(image):
    try:
        # image = Image.open(filename)
        if hasattr(image, '_getexif'):  # only present in JPEGs
            for orientation in PIL.ExifTags.TAGS.keys():
                if PIL.ExifTags.TAGS[orientation] == 'Orientation':
                    break
            e = image._getexif()  # returns None if no EXIF data
            if e is not None:
                # log.info('EXIF data found: %r', e)
                exif = dict(e.items())
                orientation = exif[orientation]
                # print('found, ',orientation)

                if orientation == 3:
                    image = image.transpose(Image.ROTATE_180)
                elif orientation == 6:
                    image = image.transpose(Image.ROTATE_270)
                elif orientation == 8:
                    image = image.rotate(90, expand=True)
    except:
        pass
    return image


def main(fileName, src_folder=None):
    output_file_name = 'E:\\tmp\\out\\' + fileName + '.pdf'
    # save_file_name = 'ex.pdf'
    # doc = SimpleDocTemplate(save_file_name, pagesize=A1,
    #                     rightMargin=72, leftMargin=72,
    #                     topMargin=72, bottomMargin=18)
    imgDoc = canvas.Canvas(output_file_name)  # pagesize=letter
    imgDoc.setPageSize(A4)
    document_width, document_height = A4
    if src_folder is None:
        mypath = input('Input the image folder please:')
    else:
        mypath = src_folder
    filenames = []
    start = time.clock()
    img_search(mypath, filenames)
    end = time.clock()
    print('find file cost time: ', end - start, 'find files: ', len(filenames))
    # for f in filenames:
    #     print(f)
    for image in filenames:
        try:
            image_file = PIL.Image.open(image)
            image_file = rotate_img_to_proper(image_file)

            image_width, image_height = image_file.size
            print('img size:', image_file.size)
            if not (image_width > 0 and image_height > 0):
                raise Exception
            image_aspect = image_height / float(image_width)
            # Determins the demensions of the image in the overview
            print_width = document_width
            print_height = document_width * image_aspect
            imgDoc.drawImage(ImageReader(image_file), document_width - print_width,
                             document_height - print_height, width=print_width,
                             height=print_height, preserveAspectRatio=True)
            # inform the reportlab we want a new page
            imgDoc.showPage()
        except Exception as e:
            print('error:', e, image)
    imgDoc.save()
    print('Done')


if __name__ == '__main__':
    main('恋人じゃ…ない。瀬戸花恋編', src_folder='E:\\tmp\\恋人じゃ…ない。瀬戸花恋編')
