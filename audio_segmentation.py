from pydub import AudioSegment
from pydub.utils import make_chunks
import os
import utils

region = "puno"
institution = "ondaazul"
year = "2017"
month = "Ago"
day = "22"

def rename_audio(path,num_audio,lenght):
	chunk_name = region+"_"+institution+"_"+year+month+day+"A_"+str(num_audio)+"-"+str(lenght)
	return chunk_name


def split_audio_without_time(audio_file):
	path = utils.get_path(audio_file)
	segment_audio = AudioSegment.from_file(audio_file,"wav") 
	chunk_length_ms = 30000 # pydub calculates in millisec, e.g 30 sec
	chunks = make_chunks(segment_audio,chunk_length_ms) #Make chunks of one sec
	#Export all of the individual chunks as wav files
	lenght = len(chunks)
	for i, chunk in enumerate(chunks):
	    chunk_name = rename_audio(path,i+1,lenght)
	    chunk.export(path+chunk_name, format="wav")