from __future__ import unicode_literals
import youtube_dl
import sys, traceback
import threading
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))


##Uses ffmpeg.exe to extract audio. Get the link's best .mp3 file, no printouts, go to download archive.
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        }],
    #'quiet':'opts.quiet',
    'download_archive': 'C:/Users/t_jorsz/PycharmProjects/Youtube-dl/youtube_list_2.txt',
    'outtmpl':"C:/Users/t_jorsz/Documents/music/%(title)s.%(ext)s",
    }

#Function that downloads the youtube link. If not, print out the exception.
def handleYoutubelink(link):
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
    except Exception:
        import traceback
        traceback.print_exc(file=sys.stdout)

#Gets rid of timestamp/playlist index if one exists
def cleanlink(link):
    if link.find('&') == -1: #-1 means it wasn't found
        output_link=link
    elif isinstance(link.find('&'), int):
        output_link=link[0:link.find('&')]
    return output_link

#main function
def __main__():

    ##Opens your file and splits with the newline delimiter.
    links = open('C:/Users/t_jorsz/Desktop/youtube_list.txt').read().split('\n')


    threads=[range(len(links))]
    if len(links)<=4:
        for i in range(len(links)):
            #print( cleanlink(links[i]) )
            t=threading.Thread( target=handleYoutubelink,args=(cleanlink(links[i]),) )
            threads.append(t)
            t.start()


    elif len(links)>4:#If there is less links than 4
        link_num=0
        while 1:
            if link_num<len(links) and threading.active_count()<=4:
                t=threading.Thread( target=handleYoutubelink,args=(cleanlink(links[link_num]),) )
                threads.append(t)
                t.start()
                link_num=link_num+1
            elif link_num>=len(links):
                break

__main__()

