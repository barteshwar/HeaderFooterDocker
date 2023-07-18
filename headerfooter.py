import streamlit as st
import pandas as pd
import numpy as np
from moviepy.editor import VideoFileClip, ImageClip, TextClip, CompositeVideoClip
import tempfile
import os
import subprocess
import sys

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
    image_clip = ImageClip("C:/Users/Dell/Downloads/HeaderFooterDocker/black1000.jpg").set_duration(video_clip.duration)
    image_clip=image_clip.resize((video_clip.w,video_clip.w))
    print(image_clip.size)
    video_clip = video_clip.set_position(("center", "center"))


    header_text=ht
    #header_text="THE HEADER FOOTER TOOL ALLOWS ANYONE TO ADD TEXT TO A VIDEO"
    header_text_split=split_two(header_text)
    print(header_text_split)

    header_fontsize=20
    header = TextClip(header_text_split,fontsize = header_fontsize, color = 'white').set_duration(video_clip.duration)

    while(header.size[0]<image_clip.size[0]*0.9):
        header = TextClip(header_text_split, font="Oswald-Bold.ttf",fontsize = header_fontsize, color = 'white').set_duration(video_clip.duration)
        header_fontsize=header_fontsize+1
        print(header_fontsize)
    header = TextClip(header_text_split, font="Oswald-Bold.ttf",fontsize = header_fontsize, color = 'white').set_duration(video_clip.duration)

    header_y=((image_clip.h-video_clip.h)/2 - header.size[1])/2
    print(header_y)
    header=header.set_position(('center', header_y))

    footer_text=ft
    #footer_text="WHAT AN AMAZING NEW INNOVATION!"
    footer_text_split=split_two(footer_text)
    print(footer_text_split)

    footer_fontsize=20
    footer = TextClip(footer_text_split, font="Oswald-Bold.ttf",fontsize = footer_fontsize, color = 'white').set_duration(video_clip.duration)

    while(footer.size[0]<image_clip.size[0]*0.9 and footer.size[1]<(image_clip.size[1]-video_clip.size[1])/2*0.9 ):
        footer = TextClip(footer_text_split, font="Oswald-Bold.ttf",fontsize = footer_fontsize, color = 'white').set_duration(video_clip.duration)
        footer_fontsize=footer_fontsize+1
        print(footer_fontsize)
    footer = TextClip(footer_text_split, font="Oswald-Bold.ttf",fontsize = footer_fontsize, color = 'white').set_duration(video_clip.duration)

    footer_y=image_clip.h-(image_clip.h-video_clip.h)/2+((image_clip.h-video_clip.h)/2 - footer.size[1])/2
    footer=footer.set_position(('center', footer_y))

    # Overlay the video on the image
    final_clip = CompositeVideoClip([image_clip, video_clip,header,footer])
    final_clip.set_duration(video_clip.duration)
    print(final_clip.size)
    # Set the output file name and save the final clip
    output_file = "output_video.mp4"
    final_clip.write_videofile(output_file, codec="libx264")
    video_file=open("C:\\Users\\Dell\\output_video.mp4",'rb')
    #video_bytes = output_file.read()
    #st.video(video_bytes) 
    #video_bytes = final_clip.read()
    #st.video(video_bytes)
    #st.video(final_clip)
    #enter the filename with filepath
    video_bytes = video_file.read() #reading the file
    st.video(video_bytes) #displaying the video

clicked = st.button('Start')
if(clicked is True):
    
    vf = VideoFileClip(tfile.name)
    
    make_video(vf,header,footer)

    