# -*- coding: utf-8 -*- 
from pydub import AudioSegment
import os
from pydub.playback import play
import utils


# create silence
def create_silence(duration):
	# create a silence audio segment, duration is in miliseconds
	silence_segment = AudioSegment.silent(duration=duration)
	return silence_segment

# join audio and silence
def mixed_silence(audio_file,cut_times):
	# read wav file to an audio segment
	audio = AudioSegment.from_wav(audio_file)
	# Add above two audio segments    
	final_audio = audio + create_silence(700)
	# Either save modified audio
	path = utils.get_path(audio_file)
	name_audio = utils.get_name_without_ext_file(audio_file)
	silince_plus_audio = path+name_audio+"_silence_"+str(cut_times)
	final_audio.export(silince_plus_audio, format="wav")
	return silince_plus_audio


def mixed_audio(audios,audio_file):
	final_audio = 0
	for audio in audios:
		segment_audio = AudioSegment.from_wav(audio)
		#Add above audio segments
		final_audio = final_audio + segment_audio
		#Either save modified audio
	path = utils.get_path(audio_file)
	name_audio = utils.get_name_without_ext_file(audio_file)
	name_audio_file = path+name_audio+"_clear"
	final_audio.export(name_audio_file, format="wav")


def detect_speech(audio_file):
	os.system("auditok -e 55 -i "+audio_file+" -m 10 --time-format \"%h:%m:%s.%i\" >> result.txt")
	

def reduce_silence(audio_file):
	cut_times = 0
	start_time = 0
	audios_with_silence = []
	new_audios = []
	end_time = 0
	silence_time = 0
	score_final = 0
	detect_speech(audio_file)
	text_file = open("result.txt", "r")
	for text_line in text_file.readlines():
		text_line = text_line.rstrip()
		items = text_line.split(" ")
		time1 = items[1].split(":")
		time2 = items[2].split(":")
		time_mil_1 = time1[2].split(".")
		time_mil_2 = time2[2].split(".")
		time_mil_1_final = 0
		time_mil_2_final = 0
		time_mil_1_final = float(float(time_mil_1[1])/1000)+float(time_mil_1[0])
		time_mil_2_final = float(float(time_mil_2[1])/1000)+float(time_mil_2[0])
		if score_final != 0:
			silence_time = time_mil_1_final-score_final
		if silence_time > 1.0:
			end_time = score_final
			new_audio_file = split_audios(start_time,end_time,audio_file,cut_times)
			new_audios.append(new_audio_file)
			audios_with_silence.append(mixed_silence(new_audio_file,cut_times))
			start_time = time_mil_1_final
			cut_times = cut_times + 1
		score_final = time_mil_2_final
	audios_with_silence.append(split_audios(start_time,30,audio_file,cut_times+1))
	mixed_audio(audios_with_silence,audio_file)
	utils.delete_files(new_audios)
	utils.delete_files(audios_with_silence)
	utils.delete_file("result.txt")


def split_audios(start_time,end_time,audio_file,cut_times):
	#Example, 00:00:00.240 00:00:01.780, Works in milliseconds
	t1 = start_time * 1000 
	t2 = end_time * 1000
	newAudio = AudioSegment.from_wav(audio_file)
	newAudio = newAudio[t1:t2]
	path = utils.get_path(audio_file)
	name_audio = utils.get_name_without_ext_file(audio_file)
	new_audio_file = path+name_audio+"_"+str(cut_times)
	newAudio.export(new_audio_file, format="wav") #Exports to a wav file in the current path.
	return new_audio_file