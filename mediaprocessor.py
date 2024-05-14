"""Media processor for Sunny's portfolio

Simple script to take the images from the portfolio media folder 
and create a set of thumbnal images that are pushed to a thumbnail 
folder, in a max 200px resolution to optimize load times. also creates
a set of html pages for each image in the pages folder, with navigation
links to the next and previous images in the gallery.

This tool accepts .png and .jpeg files. 

This script requires that `Pillow` version 9.5.0 be installed within the Python
environment you are running this script in. ( pip install Pillow==9.5.0 )
Later 'Pillow' versions may not work with this script.

This file is not intended to be imported as a module.
"""
import os
import shutil
from pprint import pprint

from PIL import Image, ImageOps

cur_dir = __file__.rpartition('\\')[0]
folders = [
    # ? provide any number of folders, with their paths !!relative!! to this file
    "\\resources\\media\\photography",
    "\\resources\\media\\illustrations",
    "\\resources\\media\\othermedia"
]

def main(folder_name):
    thumbs_folder = f'{cur_dir}{folder_name}\\thumbs\\'
    pages_folder = f'{cur_dir}{folder_name}\\pages\\'

    for filename in os.listdir(thumbs_folder):
        file_path = os.path.join(thumbs_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    for filename in os.listdir(pages_folder):    
        file_path = os.path.join(pages_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    list_of_imgs = os.listdir(f'{cur_dir}{folder_name}')
    list_of_imgs = [elm for elm in list_of_imgs if '.' in elm]

    for i in range(len(list_of_imgs)):
        if '.' in list_of_imgs[i]:  
            print(f"checking {folder_name.split(os.sep)[-1]} image ({i+1}/{len(list_of_imgs)})", end="\r")
            if(i==0):
                prev_img = f'{list_of_imgs[i-1]}'
            else:
                prev_img = f'{list_of_imgs[i-1]}'
            try:
                next_img = f'{list_of_imgs[i+1]}'
            except IndexError:
                next_img = f'{list_of_imgs[0]}'

            f = open(f'{cur_dir}{folder_name}\\pages\\{list_of_imgs[i]}.html', 'w')
            f.write(
                f"""<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>{list_of_imgs[i]}</title>
                    <link type="image/png" sizes="120x120" rel="icon" href="../../../../imgs/logo.png">
                    <meta http-equiv="ScreenOrientation" content="autoRotate:disabled">
                    <link rel="stylesheet" href="../../../../css/main.css">
                    <link rel="stylesheet" href="../../../../work/imagepage.css">
                </head>
                <body>


                    <div class="content">
                        <div class="home-button">
                            <a class="clickback" href="../../../../index.html">Home</a>
                        </div>
                        <div class="img-container">
                            <img 
                                class="full-img" 
                                src="https://raw.githubusercontent.com/dogtiered/dogtiered.github.io/main{folder_name.replace(os.sep, '/')}/{list_of_imgs[i]}" 
                            alt="why no here">
                        </div>
                        <a class="clickleft" href="{prev_img}.html"><</a>        
                        <a class="clickright" href="{next_img}.html">></a>
                    </div>

                </body>
                <script>

                </script>
                </html>"""
            )
            
            image = Image.open(f'{cur_dir}{folder_name}\\{list_of_imgs[i]}')
            image = ImageOps.exif_transpose(image)  #correct quirk with images 
                                                    #not rotating correctly
            image.thumbnail((400,400))
            image.save(f'{cur_dir}{folder_name}\\thumbs\\{list_of_imgs[i]}')

    html_string = ""
    for img in list_of_imgs:
        html_string += f'<li><a href="..{folder_name.replace(os.sep, "/")}/pages/{img}.html"><img src="..{folder_name.replace(os.sep, "/")}/thumbs/{img}" alt="{img}"><div class="image-hover">{img.split(".")[0]}</div></a></li>'
    print('\n\n\nCOPY THIS INTO THE HTML FILE\n\n',html_string,'\n\n')

if __name__ == "__main__":
    for folder in folders:
        main(folder)
            


