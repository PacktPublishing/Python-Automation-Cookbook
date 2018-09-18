import argparse
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import PyPDF2
from pdf2image import convert_from_path

DEFAULT_OUTPUT = 'watermarked.pdf'
DEFAULT_BY = 'default user'
INTERMEDIATE_ENCRYPT_FILE = 'temp.pdf'

WATERMARK_SIZE = (200, 200)


def encrypt(out_pdf, password):
    print('Encrypting the document')

    output_pdf = PyPDF2.PdfFileWriter()

    in_file = open(out_pdf, "rb")
    input_pdf = PyPDF2.PdfFileReader(in_file)
    output_pdf.appendPagesFromReader(input_pdf)
    output_pdf.encrypt(password)

    # Intermediate file
    with open(INTERMEDIATE_ENCRYPT_FILE, "wb") as out_file:
        output_pdf.write(out_file)

    in_file.close()

    # Rename the intermediate file
    os.rename(INTERMEDIATE_ENCRYPT_FILE, out_pdf)


def create_watermark(watermarked_by):
    print('Creating a watermark')
    mask = Image.new('L', WATERMARK_SIZE, 0)
    draw = ImageDraw.Draw(mask)
    font = ImageFont.load_default()
    text = 'WATERMARKED BY {}\n{}'.format(watermarked_by, datetime.now())
    draw.multiline_text((0, 100), text, 55, font=font)

    watermark = Image.new('RGB', WATERMARK_SIZE)
    watermark.putalpha(mask)
    watermark = watermark.resize((1950, 1950))
    watermark = watermark.rotate(45)
    # Crop to only the watermark
    bbox = watermark.getbbox()
    watermark = watermark.crop(bbox)

    return watermark


def apply_watermark(watermark, in_pdf, out_pdf):
    print('Watermarking the document')
    # Transform from PDF to images
    images = convert_from_path(in_pdf)

    # Get the location for the watermark
    hi, wi = images[0].size
    hw, ww = watermark.size
    position = ((hi - hw) // 2, (wi - ww) // 2)

    # Paste the watermark in each page
    for image in images:
        image.paste(watermark, position, watermark)

    # Save the resulting PDF
    images[0].save(out_pdf, save_all=True, append_images=images[1:])


def main(in_pdf, out_pdf, watermarked_by, password):

    watermark = create_watermark(watermarked_by)
    apply_watermark(watermark, in_pdf, out_pdf)

    if password:
        encrypt(out_pdf, password)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='pdf', type=str,
                        help='PDF to watermark')
    parser.add_argument('-o', type=str,
                        help=f'Output PDF filename, default: {DEFAULT_OUTPUT}',
                        default=DEFAULT_OUTPUT)
    parser.add_argument('-u', type=str,
                        help=f'Watermarked by, default: {DEFAULT_BY}',
                        default=DEFAULT_BY)
    parser.add_argument('-p', type=str,
                        help='Password')
    args = parser.parse_args()
    main(args.pdf, args.o, args.u, args.p)
