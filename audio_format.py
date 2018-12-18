import os
from time import time
import utils

#All type of format can be change to wav format, 16kHz and 16 bits sample
def get_format(audio_file):
	name_audio = utils.get_name_without_ext_file(audio_file)
	path = utils.get_path(audio_file)
	audio_folder = utils.create_audio_folder(path,"audios")
	os.system("ffmpeg -i '"+audio_file+"' -acodec pcm_s16le -ac 1 -ar 16000 '"+audio_folder+name_audio+"'.wav")