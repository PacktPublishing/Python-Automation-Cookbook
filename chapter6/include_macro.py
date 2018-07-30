import zipfile
import shutil
import os
import argparse
OUTPUT_DIR = 'macro_file'


def main(spreadsheet, script):
    print("Delete and create directory with_macro")
    shutil.rmtree(OUTPUT_DIR, True)
    os.mkdir(OUTPUT_DIR)

    filename = OUTPUT_DIR + '/' + spreadsheet
    print("Open file " + spreadsheet)
    shutil.copyfile(spreadsheet, filename)

    doc = zipfile.ZipFile(filename, 'a')
    doc.write(script, 'Scripts/python/' + script)
    manifest = []
    for line in doc.open('META-INF/manifest.xml'):
        if '</manifest:manifest>' in line.decode('utf-8'):
            for path in ['Scripts/', 'Scripts/python/',
                         'Scripts/python/' + script]:
                man_line = (' <manifest:file-entry '
                            'manifest:media-type="application/binary" '
                            f'manifest:full-path="{path}"/>')
                manifest.append(man_line)
        manifest.append(line.decode('utf-8'))

    doc.writestr('META-INF/manifest.xml', ''.join(manifest))
    doc.close()
    print("File created: " + filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='spreadsheet', type=str,
                        help='File to insert the script')
    parser.add_argument(dest='script', type=str,
                        help='Script to insert in the file')
    args = parser.parse_args()
    main(args.spreadsheet, args.script)
