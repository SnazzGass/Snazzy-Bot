import keep_alive
import discord
import os
import time
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
#^ basic imports for other features of discord.py and python ^

from preview import Preview
from level_presets import presets


active_channel_name = "bot"
previewer = Preview(max_level_size=256)
client = commands.Bot(command_prefix = "!")


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    

@client.command(
  brief="shows a preview of a level string"
  )
async def preview(ctx, *, level_string):
  if level_string in presets:
    level_string = presets[level_string]
  if len(level_string) >= 6:
    if level_string[:3] + level_string[-3:] == '``````':
      level_string = level_string[3:-3]
  result = previewer.preview(level_string)
  print("parsed string: " if result[0] else "can't parse string: " + level_string)
  if result[0]:
    previewer.save_image()
    embed = discord.Embed(title=result[1], description=result[2], color=0x0f3e67)  # creates embed
    file = discord.File("preview.png", filename="image.png")
    embed.set_image(url="attachment://image.png")
    await ctx.channel.send(file=file, embed=embed)
  else:
    await ctx.channel.send(result[1])

@client.command(
  brief="prints a level string"
  )
async def getstring(ctx, *, level_name):
  if level_name in presets:
    await ctx.channel.send('```' + presets[level_name] + '```')
    
@client.event
async def on_message(message):
  if message.channel.type.name == 'private':  # got a DM
    if message.author != client.user:
      print('got direct message: ', message.content, " from ", message.author)
      await message.channel.send('beep boop')
  elif message.channel.name == active_channel_name:
    await client.process_commands(message)



keep_alive.keep_alive()
client.run(os.getenv("TOKEN"))
