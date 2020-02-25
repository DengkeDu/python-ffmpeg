import collections
import re

Progress = collections.namedtuple('Progress', [
    'frame', 'fps', 'size', 'time', 'bitrate', 'speed'
])

Progress_psnr = collections.namedtuple('Progress_psnr',['PSNR'])
Progress_vmaf = collections.namedtuple('Progress_vmaf',['VMAF'])

progress_pattern = re.compile(
    r'(frame|fps|size|time|bitrate|speed)\s*\=\s*(\S+)'
)

vmaf_pattern = re.compile(
    r'(VMAF)\s*score:\s*(\S+)'
)

psnr_pattern = re.compile(
    r'(PSNR)\s*.*average:\s*(\S+)'
)

def build_options(options):
    arguments = []

    for key, value in options.items():
        if key.startswith('-'):
            key = key[1:]

        argument = ['-{key}'.format(key=key)]
        if value is not None:
            argument.append(str(value))

        arguments.extend(argument)

    return arguments


async def readlines(stream):
    pattern = re.compile(br'[\r\n]+')

    data = bytearray()
    while not stream.at_eof():
        lines = pattern.split(data)
        data[:] = lines.pop(-1)

        for line in lines:
            yield line

        data.extend(await stream.read(1024))


def parse_progress(line):
    items = {
        key: value for key, value in progress_pattern.findall(line)
    }
    
    items_psnr = {}
    items_vmaf = {}

    if "PSNR" in line:
        items_psnr = {key:value for key, value in psnr_pattern.findall(line)}
        return Progress_psnr(PSNR=items_psnr['PSNR'])
    if "VMAF" in line:
        items_vmaf = {key:value for key, value in vmaf_pattern.findall(line)}
        return Progress_vmaf(VMAF=items_vmaf['VMAF'])

    if not items:
        return None
    if "N" in items['size']:
        items['size'] = "0"
    if "N" in items['bitrate']:
        items['bitrate'] = "0"
        
    return Progress(
        frame=int(items['frame']),
        fps=float(items['fps']),
        size=int(items['size'].replace('kB', '')) * 1024,
        time=items['time'],
        bitrate=float(items['bitrate'].replace('kbits/s', '')),
        speed=float(items['speed'].replace('x', '')),
    )
