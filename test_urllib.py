import urllib.request
from ffmpeg import FFmpeg
import asyncio

url = "https://alpha-obs.yunshicloud.com/7674F33E470D459E/QMTNRK_YUNSHI/D52CB54DB7FE4AB0AA8FF77C7093AB84/D01BEFCB93CA47E099513C78BDC7CB30.mp4"

#filename,headers = urllib.request.urlretrieve(url)

fileavi = "test.avi"
filename = "test.mp4"

ff = FFmpeg()

@ff.on('start')
def on_start(arguments):
    print('Arguments:', arguments)

@ff.on('progress')
def on_pregress(progress):
    print(progress)

ff.input(filename)
ff.input(fileavi)
ff.output("-",{'filter_complex':'psnr'},f="null")
loop = asyncio.get_event_loop()
loop.run_until_complete(ff.execute())
loop.close
