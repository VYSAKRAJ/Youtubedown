import pafy
import urllib.request
from django.http import HttpResponse
from django.shortcuts import render
from django.template.defaultfilters import filesizeformat
import urllib.request

from .forms import DownloadForm


class parser:
    def __init__(self, url):
        self.url = url
        self.context=None
        self.Download_return()

    def getData(self):# return full dataframe from file
        return (self.context)

    def Download_return(self):
        # if urllib.request.urlopen(self.url).code == 200:
        pafy.set_api_key('AIzaSyCp0RX2L3eDzuNiPNJr34jom1-gUsj_ze0')
        video = pafy.new(self.url)
        stream = video.streams
        print (video.audiostreams)
        video_audio_streams = []
        for s in stream:
            video_audio_streams.append({
                'resolution': s.resolution,
                'extension': s.extension,
                # 'file_size': filesizeformat(s.get_filesize()),
                'video_url': s.url + "&title=" + video.title
            })

        stream_video = video.videostreams
        print ('video stream')

        video_streams = []
        for s in stream_video:
            video_streams.append({
                'resolution': s.resolution,
                'extension': s.extension,
                # 'file_size': filesizeformat(s.get_filesize()),
                'video_url': s.url + "&title=" + video.title
            })

        stream_audio = video.audiostreams
        audio_streams = []
        for s in stream_audio:
            audio_streams.append({
                'resolution': s.resolution,
                'extension': s.extension,
                # 'file_size': filesizeformat(s.get_filesize()),
                'video_url': s.url + "&title=" + video.title
            })
        print('before context')
        context = {
            # 'form': form,
            'title': video.title, 'streams': video_audio_streams,
            'description': video.description, 'likes': video.likes,
            'dislikes': video.dislikes, 'thumb': video.bigthumbhd,
            'duration': video.duration, 'views': video.viewcount,
            'stream_video': video_streams, 'stream_audio': audio_streams
        }
        self.context=context
        return




def download_video(request):
    global context
    form = DownloadForm(request.POST or None)
    if form.is_valid():
        video_url = form.cleaned_data.get("url")
        # if 'm.' in video_url:
        #     video_url = video_url.replace(u'm.', u'')
        #
        # elif 'youtu.be' in video_url:
        #     video_id = video_url.split('/')[-1]
        #     video_url = 'https://www.youtube.com/watch?v=' + video_id
        #
        # if len(video_url.split("=")[-1]) != 11:
        #     return HttpResponse('Enter correct url.')
        obj1=parser(video_url)
        context=obj1.getData()
        print(context)
        return render(request, 'home.html',context )

    return render(request, 'home.html', { 'form': form })

