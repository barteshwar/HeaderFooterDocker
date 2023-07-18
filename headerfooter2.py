import streamlit as st
import pandas as pd
import numpy as np
from moviepy.editor import VideoFileClip, ImageClip, TextClip, CompositeVideoClip
import tempfile
import os
import subprocess
import sys
import gizeh
import fontTools

from fontTools.ttLib import TTFont
font = TTFont('Oswald-Bold.ttf')
font.save('Oswald-Bold.ttf')
"""
An alternative text clip for Moviepy, relying on Gizeh instead of ImageMagick
Advantages:
- Super fast (20x faster)
- no need to install imagemagick
- full-vector graphic, no aliasing problems
- Easier font names
Disadvantages:
- Requires Cairo installed
- Doesnt support kerning (=letters spacing)
"""

try:
    import gizeh as gz
    GIZEH_AVAILABLE = True
except ImportError:
    GIZEH_AVAILABLE = False
import numpy as np
from moviepy.editor import ImageClip

def autocrop(np_img):
    """Return the numpy image without empty margins."""
    if len(np_img.shape) == 3:
        if np_img.shape[2] == 4:
            thresholded_img = np_img[:,:,3] # use the mask
        else:
            thresholded_img = np_img.max(axis=2) # black margins
    zone_x = thresholded_img.max(axis=0).nonzero()[0]
    xmin, xmax = zone_x[0], zone_x[-1]
    zone_y = thresholded_img.max(axis=1).nonzero()[0]
    ymin, ymax = zone_y[0], zone_y[-1]
    return np_img[ymin:ymax+1, xmin:xmax+1]

def text_clip(text, font_family, align='left',
              font_weight='normal', font_slant='normal',
              font_height = 70, font_width = None,
              interline= None, fill_color=(0,0,0),
              stroke_color=(0, 0, 0), stroke_width=2,
              bg_color=None):
    """Return an ImageClip displaying a text.
    
    Parameters
    ----------
    
    text
      Any text, possibly multiline
    
    font_family
      For instance 'Impact', 'Courier', whatever is installed
      on your machine.
    
    align
      Text alignment, either 'left', 'center', or 'right'.
      
    font_weight
      Either 'normal' or 'bold'.
    
    font_slant
      Either 'normal' or 'oblique'.
    
    font_height
      Eight of the font in pixels.
      
    font_width
      Maximal width of a character. This is only used to
      create a surface large enough for the text. By
      default it is equal to font_height. Increase this value
      if your text appears cropped horizontally.
    
    interline
      number of pixels between two lines. By default it will be
    
    stroke_width
      Width of the letters' stroke in pixels.
      
    stroke_color
      For instance (0,0,0) for black stroke or (255,255,255)
      for white.
    
    fill_color=(0,0,0),
      For instance (0,0,0) for black letters or (255,255,255)
      for white.
    
    bg_color
      The background color in RGB or RGBA, e.g. (255,100,230)
      (255,100,230, 128) for semi-transparent. If left to none,
      the background is fully transparent
    
    """
    
    if not GIZEH_AVAILABLE:
        raise ImportError("`text_clip` requires Gizeh installed.")

    stroke_color = np.array(stroke_color)/255.0
    fill_color = np.array(fill_color)/255.0
    if bg_color is not None:
        np.array(bg_color)/255.0

    if font_width is None:
        font_width = font_height
    if interline is None:
        interline = 0.3 * font_height
    line_height = font_height + interline
    lines = text.splitlines()
    max_line = max(len(l) for l in lines)
    W = int(max_line * font_width + 2 * stroke_width)
    H = int(len(lines) * line_height + 2 * stroke_width)
    surface = gz.Surface(width=W, height=H, bg_color=bg_color)
    xpoint = {
        'center': W/2,
        'left': stroke_width + 1,
        'right': W - stroke_width - 1
    }[align]
    for i, line in enumerate(lines):
        ypoint = (i+1) * line_height
        text_element = gz.text(line, fontfamily=font_family, fontsize=font_height,
                               h_align=align, v_align='top',
                               xy=[xpoint, ypoint], fontslant=font_slant,
                               stroke=stroke_color, stroke_width=stroke_width,
                               fill=fill_color)
        text_element.draw(surface)
    cropped_img = autocrop(surface.get_npimage(transparent=True))
    return ImageClip(cropped_img)

#subprocess.check_call([sys.executable, "-m", "apt", "install", 'git+https://github.com/facebookresearch/detectron2.git'])
st.title('Add header and footer')
#st.text_area(env)
#vc=st.file_uploader("Upload video",type=['mp4'])
f = st.file_uploader("Upload file",type=['mp4'])

if f is not None:
  tfile = tempfile.NamedTemporaryFile(delete=False)
  tfile.write(f.read())
  st.video(f)

header=st.text_input("Header")
footer=st.text_input("Footer")

def replace_character(string, index, new_char):
        # Check if the index is within the bounds of the string
        if index < 0 or index >= len(string):
            return string  # Return the original string if the index is invalid

        # Create a new string by slicing the original string
        new_string = string[:index] + new_char + string[index + 1:]

        return new_string

def split_two(text):
    mid=round(len(text)/2)
    print(mid)
    print(text[mid])
    i=1
    while(1):
        if(text[mid]==" "):
            text=replace_character(text, mid, "\n")
            return text
        if(text[mid+i]==" "):
        #print('here')
            text=replace_character(text, mid+i, "\n")
            return text
        if(text[mid-i]==" "):
            text=replace_character(text, mid-i, "\n")
            return text
        i=i+1
        print("i is: ",i)


def make_video(vc,ht,ft):
#age = st.slider('How old are you?', 0, 130, 25)
#st.write("I'm ", age*2, 'years old')

#video_clip = VideoFileClip("C:\\Users\\Dell\\Downloads\\scraper\\horz.mp4")
    video_clip=vc
    image_clip = ImageClip('black1000.jpg').set_duration(video_clip.duration)
    image_clip=image_clip.resize((video_clip.w,video_clip.w))
    print(image_clip.size)
    video_clip = video_clip.set_position(("center", "center"))


    header_text=ht
    #header_text="THE HEADER FOOTER TOOL ALLOWS ANYONE TO ADD TEXT TO A VIDEO"
    header_text_split=split_two(header_text)
    print(header_text_split)

    header_fontsize=20
    #header_fontheight=20
    header = text_clip(header_text_split,font_family="Oswald-Bold.ttf",align='center',font_height = header_fontsize, fill_color=(255,255,255),stroke_width=0).set_duration(video_clip.duration)

    while(header.size[0]<image_clip.size[0]*0.9 and header.size[1]<(image_clip.size[1]-video_clip.size[1])/2*0.8):
        header = text_clip(header_text_split,font_family="Oswald-Bold.ttf",align='center',font_height = header_fontsize, fill_color=(255,255,255),stroke_width=0).set_duration(video_clip.duration)
        header_fontsize=header_fontsize+1
        print(header_fontsize)
    header = text_clip(header_text_split,font_family=font,font_height = header_fontsize, align='center',fill_color=(255,255,255),stroke_width=0).set_duration(video_clip.duration)

    header_y=((image_clip.h-video_clip.h)/2 - header.size[1])/2
    print(header_y)
    header=header.set_position(('center', header_y))

    footer_text=ft
    #footer_text="WHAT AN AMAZING NEW INNOVATION!"
    footer_text_split=split_two(footer_text)
    print(footer_text_split)

    footer_fontsize=20
    footer = text_clip(footer_text_split,font_family="https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap",align='center',font_height=footer_fontsize, fill_color=(255,255,255),stroke_width=0).set_duration(video_clip.duration)

    while(footer.size[0]<image_clip.size[0]*0.9 and footer.size[1]<(image_clip.size[1]-video_clip.size[1])/2*0.9 ):
        footer = text_clip(footer_text_split, font_family="https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap",align='center',font_height = footer_fontsize, fill_color=(255,255,255),stroke_width=0).set_duration(video_clip.duration)
        footer_fontsize=footer_fontsize+1
        print(footer_fontsize)
    footer = text_clip(footer_text_split, font_family=font,align='center',font_height = footer_fontsize, fill_color=(255,255,255),stroke_width=0).set_duration(video_clip.duration)

    footer_y=image_clip.h-(image_clip.h-video_clip.h)/2+((image_clip.h-video_clip.h)/2 - footer.size[1])/2
    footer=footer.set_position(('center', footer_y))

    # Overlay the video on the image
    final_clip = CompositeVideoClip([image_clip, video_clip,header,footer])
    final_clip.set_duration(video_clip.duration)
    print(final_clip.size)
    # Set the output file name and save the final clip
    output_file = "output_video.mp4"
    final_clip.write_videofile(output_file, codec="libx264")
    video_file=open("output_video.mp4",'rb')
    #video_bytes = output_file.read()
    #st.video(video_bytes) 
    #video_bytes = final_clip.read()
    #st.video(video_bytes)
    #st.video(final_clip)
    #enter the filename with filepath
    #video_bytes = final_clip.read() #reading the file
    video_bytes = video_file.read() #reading the file
    st.video(video_bytes) #displaying the video
    #st.video(final_clip) #displaying the video

clicked = st.button('Start')
if(clicked is True):
    
    vf = VideoFileClip(tfile.name)
    
    make_video(vf,header,footer)

    