from	__future__		import	unicode_literals
import	interactions
import	time
import	re
import	os
from	yt_dlp			import	YoutubeDL
from	yt_dlp.utils	import	DownloadError
from	anonfile		import	AnonFile
import	config

bot = interactions.Client(token = config.token)
anon = AnonFile()

def	timeLog():
	return (time.strftime("%H:%M:%S", time.localtime()))

def	Find(string):
	regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
	url = re.findall(regex,string)
	return [x[0] for x in url]

def	youtube_download(url: str)->str:
	ydl_opt = {}
	with YoutubeDL(ydl_opt) as ydl:
		try:
			info = ydl.extract_info(url, download = True)
		except DownloadError:
			return ('error')
		title = info.get('title', None) + " [" + info.get('id', None) + "]." + info.get('ext', None)
		return (title)

def	anonfiles_upload(title: str)->str:
	upload = anon.upload(os.path.join("./", title), progressbar = True)
	print(upload.url.geturl())
	return (upload.url.geturl())

@bot.event
async def	on_ready():
	print(time.strftime("%H:%M:%S", time.localtime()), " : Bot has started")

@bot.command(
	name = "ytdl",
	description = "Generate a download link for the given YouTube vvideo URL",
	scope = config.guildId,
	options = [
		interactions.Option(
			name = "url",
			description = "YouTube video URL",
			type = interactions.OptionType.STRING,
			required = True,
		),
	],
)
async def ytdl(ctx: interactions.CommandContext, url: str):
	if Find(url):
		await ctx.send("The download link is being generated. . .")
		title = youtube_download(url)
		if title == 'error':
			await ctx.edit("Please provide a valid video url")
			return
		link = anonfiles_upload(title)
		os.remove(os.path.join("./", title))
		await ctx.edit(f"The video can be downloaded from : {link}")
	else:
		await ctx.send("Please provide a valid url")

bot.start()
