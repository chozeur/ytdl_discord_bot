############################################################################
#   ╱╱       ╲╱    ╱   ╲╱        ╲╱       ╲╲╱        ╲╱    ╱   ╲╱        ╲ #
#  ╱╱        ╱         ╱         ╱-        ╱         ╱         ╱         ╱ #
# ╱       --╱         ╱         ╱        _╱        _╱         ╱        _╱  #
# ╲________╱╲___╱____╱╲________╱╲________╱╲________╱╲________╱╲____╱___╱   #
############################################################################

from	__future__		import	unicode_literals
import	interactions
import	time
import	re
import	os
from	yt_dlp			import	YoutubeDL
from	yt_dlp.utils	import	DownloadError
from	anonfile		import	AnonFile
import	config
import	sys

bot=interactions.Client(token=config.token)
anon=AnonFile()

dlId=0

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
async def	on_ready():
	print(time.strftime("%H:%M:%S", time.localtime()), " : Bot has started")

@bot.command(
	name="ytdl_help",
	description="Show commands",
	options=[]
)
async def	ytdl_help(ctx: interactions.CommandContext):
	embed=interactions.Embed(title="YTDL commands")
	embed.add_field(name="/ytdl", value="Generate an Anonfiles download link from URL", inline=True)
	embed.add_field(name="/ytmp3", value="Convert given video to mp3 and generate a download link", inline=True)
	await ctx.send(embeds=embed)

@bot.command(
	name="ytdl",
	description="Generate a download link for the given YouTube vvideo URL",
	options=[
		interactions.Option(
			name="url",
			description="YouTube video URL",
			type=interactions.OptionType.STRING,
			required=True,
		),
	],
)
async def	ytdl(ctx: interactions.CommandContext, url: str):
	embedError=interactions.Embed()
	embedError.add_field(name="ERROR", value="Please provide a valid video url")
	embedDLGen=interactions.Embed()
	embedDLGen.add_field(name="GENERATE", value="The download link is being generated. . .")
	if Find(url):
		await ctx.send(embeds=embedDLGen)
		title=youtube_download_video(url)
		if title=='error':
			return await ctx.edit(embeds=embedError)
		link=anonfiles_upload(title)
		embedLink=interactions.Embed()
		embedLink.add_field(name="DOWNLOAD", value=link)
		os.remove(os.path.join("./", title))
		return await ctx.edit(embeds=embedLink)
	else:
		return await ctx.send(embeds=embedError)

@bot.command(
	name="ytmp3",
	description="Extract the given video's audio in mp3 and generate a download link",
	options=[
		interactions.Option(
			name="url",
			description="YouTube video URL",
			type=interactions.OptionType.STRING,
			required=True,
		),
	]
)
async def	ytmp3(ctx: interactions.CommandContext, url: str):
	embedAudioExtract=interactions.Embed()
	embedAudioExtract.add_field(name="EXTRACT", value="The video's audio is being extracted. . .")
	embedError=interactions.Embed()
	embedError.add_field(name="ERROR", value="Please provide a valid video url")
	embedDLGen=interactions.Embed()
	embedDLGen.add_field(name="GENERATE", value="The download link is being generated. . .")
	if Find(url):
		await ctx.send(embeds=embedAudioExtract)
		title=youtube_download_mp3(url)
		if title=='error':
			return await ctx.edit(embeds=embedError)
		await ctx.edit(embeds=embedDLGen)
		link=anonfiles_upload(title)
		embedLink=interactions.Embed()
		embedLink.add_field(name="DOWNLOAD", value=link)
		os.remove(os.path.join("./", title))
		await ctx.edit(embeds=embedLink)
	else:
		await ctx.send(embeds=embedError)

bot.start()
