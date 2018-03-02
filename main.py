import asyncio
import json
import os

import aiofiles
import discord


class Bot(discord.Client):
    def __init__(self):
        super(Bot, self).__init__()

    async def on_ready(self):

        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if message.author == self.user:
            content = message.content  # type: str

            if content.startswith('>tex'):
                content = content[4:].strip()

                image_file = await compile_tex(content)

                await self.send_file(message.channel, image_file)
            elif content.startswith('>bigify'):
                await make_str(self, message, False)
            elif content.startswith('>Bigify'):
                await make_str(self, message, True)

async def make_str(self, message, newline):
    content = message.content[7:].strip()
    if len(content) == 0:
        await self.delete_message(message)
    msg = ''
    for letter in content:
        if letter == ' ' and newline:
            msg += '\n'
        elif not letter.isalpha():
            msg += ''
        else:
            msg += (':regional_indicator_%s: ' % letter)
    await self.delete_message(message)
    await self.send_message(message.channel, msg)

async def compile_tex(snippet):
    async with aiofiles.open('template.tex') as f:
        template = await f.read()

    source = template.replace('{_user_code_}', snippet)

    async with aiofiles.open('tmp/snippet.tex', mode='w') as f:
        await f.write(source)

    proc_latex = await asyncio.create_subprocess_exec('pdflatex', 
                                                      '-shell-escape',
                                                      'snippet.tex', cwd='tmp/')
    await proc_latex.wait()

    proc_convert = await asyncio.create_subprocess_exec('convert',
                                                        '-density', '300',
                                                        'snippet.pdf',
                                                        '-trim',
                                                        '-border', '16x16',
                                                        '-background', 'white',
                                                        '-alpha', 'remove',
                                                        '-quality', '90',
                                                        'snippet.png', cwd='tmp/')
    await proc_convert.wait()

    return 'tmp/snippet.png'


def main():
    with open('config.json') as f:
        config = json.load(f)

    os.makedirs('tmp', exist_ok=True)

    client = Bot()

    client.run(config['token'], bot=False)


if __name__ == '__main__':
    main()
