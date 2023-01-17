############################################################################
#   ╱╱       ╲╱    ╱   ╲╱        ╲╱       ╲╲╱        ╲╱    ╱   ╲╱        ╲ #
#  ╱╱        ╱         ╱         ╱-        ╱         ╱         ╱         ╱ #
# ╱       --╱         ╱         ╱        _╱        _╱         ╱        _╱  #
# ╲________╱╲___╱____╱╲________╱╲________╱╲________╱╲________╱╲____╱___╱   #
############################################################################

from	__future__		import	unicode_literals
import discord
import	time
import	re
import	os
from	yt_dlp			import	YoutubeDL
from	yt_dlp.utils	import	DownloadError
from	anonfile		import	AnonFile
from 	dotenv			import	load_dotenv
import	sys

load_dotenv('../.env')
bot = discord.Bot()
anon = AnonFile()

def	timeLog():
	return (time.strftime("%H:%M:%S", time.localtime()))

def	Find(string):
	regex=r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
	url=re.findall(regex,string)
	return [x[0] for x in url]

def	youtube_download_mp3(url: str)->str:
	global	dlId
	dlId += 1
	ydl_opt={
	'outtmpl': './%(id)s.mp3',
	'format': 'mp3/bestaudio/best',
	'postprocessors': [{
		'key': 'FFmpegExtractAudio',
		'preferredcodec': 'mp3',
	}]
	}
	with YoutubeDL(ydl_opt) as ydl:
		try:
			info=ydl.extract_info(url, download=True)
		except DownloadError:
			return ('error')
		title=info.get('id', None) + ".mp3"
		return (title)

def	youtube_download_video(url: str)->str:
	global	dlId
	dlId += 1
	ydl_opt={
		'outtmpl': '%(id)s.%(ext)s'
	}
	with YoutubeDL(ydl_opt) as ydl:
		try:
			info=ydl.extract_info(url, download=True)
		except DownloadError:
			return ('error')
		title=info.get('id', None) + "." + info.get('ext', None)
		return (title)

def	anonfiles_upload(title: str)->str:
	upload=anon.upload("./" + title, progressbar=True)
	print(upload.url.geturl())
	return (upload.url.geturl())

@bot.event


bot.run(token)
