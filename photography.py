"""Gallery thumbnail creator

Simple script to take the images from the gallery on the website and 
create a set of thumbnail images that are pushed to the gallery-self/thumbs
folder, in a max 200px resolution to optimize load times. Is meant to 
be run every time images are added to the gallery.

This tool accepts .png and .jpeg files. 

This script requires that `Pillow` version 9.5.0 be installed within the Python
environment you are running this script in. ( pip install Pillow==9.5.0 )

This file is not intended to be imported as a module.
"""
import colorsys
import math
import os
import shutil
from pprint import pprint

from imagedominantcolor import DominantColor
from PIL import Image, ImageOps

cur_dir = __file__.rpartition('\\')[0]
            
thumbs_folder = f'{cur_dir}\\resources\\media\\photography\\thumbs\\'
pages_folder = f'{cur_dir}\\resources\\media\\photography\\pages\\'
count = 0
for filename in os.listdir(thumbs_folder):
    file_path = os.path.join(thumbs_folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
        #print(f"removed {count}/{len(os.listdir(thumbs_folder))}  {filename} from {thumbs_folder})", end="\r")
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

count = 0
for filename in os.listdir(pages_folder):
    
    file_path = os.path.join(pages_folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
        #print(f"removed {count}/{len(os.listdir(pages_folder))}  {filename} from {pages_folder})", end="\r")
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))


list_of_imgs = os.listdir(f'{cur_dir}\\resources\\media\\photography')
list_of_imgs = [elm for elm in list_of_imgs if '.' in elm]

for i in range(len(list_of_imgs)):
    if '.' in list_of_imgs[i]:  
        print(f"checking image ({i+1}/{len(list_of_imgs)})", end="\r")
        if(i==0):
            prev_img = f'{list_of_imgs[i-1]}'
        else:
            prev_img = f'{list_of_imgs[i-1]}'
        try:
            next_img = f'{list_of_imgs[i+1]}'
        except IndexError:
            next_img = f'{list_of_imgs[0]}'

        f = open(f'{cur_dir}\\resources\\media\\photography\\pages\\{list_of_imgs[i]}.html', 'w')
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

    <div class="runner header">
        <div class="header-items">
            <a href="../../../../about.html" class="header-item">About me&nbsp;&nbsp;•</a>
            <a href="../../../../index.html" class="header-item">&nbsp;&nbsp;Work&nbsp;&nbsp;•</a>
            <a href="../../../../contact.html" class="header-item">&nbsp;&nbsp;Contact</a>
        </div>
    </div>
    <div class="content">
        <a class="clickback" href="../../../index.html"><-</a>
        <div class="img-container">
            <img 
                class="full-img" 
                src="https://raw.githubusercontent.com/dogtiered/dogtiered.github.io/main/resources/media/photography/{list_of_imgs[i]}" 
            alt="why no here">
        </div>
        <a class="clickleft" href="{prev_img}.html"><</a>        
        <a class="clickright" href="{next_img}.html">></a>
    </div>
    <div class="runner footer">
        <a href="https://nixie.digital" class="footer-item">made by nixie.digital</a>
    </div>
</body>
<script>

</script>
</html>""")
        print(prev_img, next_img)
        

        image = Image.open(f'{cur_dir}\\resources\\media\\photography\\{list_of_imgs[i]}')
        image = ImageOps.exif_transpose(image)  #correct quirk with images 
                                                #not rotating correctly
        image.thumbnail((400,400))
        image.save(f'{cur_dir}\\resources\\media\\photography\\thumbs\\{list_of_imgs[i]}')

    
pprint(list_of_imgs)

html_string = ""
for img in list_of_imgs:
    html_string += f'<li><a href="../resources/media/photography/pages/{img}.html"><img src="../resources/media/photography/thumbs/{img}" alt="{img}"><div class="image-hover">{img.split(".")[0]}</div></a></li>'

print(html_string)


