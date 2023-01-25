import disnake
from disnake.ext import commands
import math
import asyncio
import requests
import datetime

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True


bot = commands.Bot(command_prefix=commands.when_mentioned_or('g!'), intents=intents)


@bot.event
async def on_ready():
    activity = disnake.Game(name='Ta olhando oq?', type=3)
    await bot.change_presence(status=disnake.Status.online, activity=activity)
    print('Bot Online')


@bot.event
async def on_member_join(membro: disnake.Member):
    servidor = membro.guild
    if servidor.system_channel:
        await servidor.system_channel.send(f'{membro.mention} bem vindo(a) ao {servidor.name}')


@bot.event
async def on_member_remove(membro: disnake.Member):
    servidor = membro.guild
    if servidor.system_channel:
        await servidor.system_channel.send(f'Até mais! {membro.mention}')


@bot.command()
async def ping(ctx):
    botPing = round(bot.latency * 1000)
    await ctx.send(f'Ping: {botPing}ms')


@bot.slash_command(name='ping', description='Mostra o ping do bot')
async def ping2(inter):
    botPing2 = round(bot.latency * 1000)
    await inter.response.send_message(f'Ping: {botPing2}ms')


@bot.command()
async def raiz(ctx, number=''):
    calculo = math.sqrt(int(number))
    await ctx.send(f'A raiz quadrada de {number} é {calculo}')


@bot.slash_command(name='raiz', description='Calcula a raiz quadrada de um número')
async def raiz2(inter, número=''):
    if número == '':
        await inter.response.send_message('Por favor digite um número válido')
    else:
        calculo2 = math.sqrt(int(número))
        await inter.response.send_message(f'A raiz quadrada de {número} é {calculo2}')


@bot.slash_command(name='kick', description='Expulsa o usuário')
async def kick(inter, membro : disnake.Member, *,motivo=None):
    await membro.kick(reason=motivo)
    await inter.response.send_message(f'{inter.author.mention} expulsou {membro.mention} por {motivo}')
    

@bot.slash_command(name='ban', description='Bane o usuário')
async def ban(inter, membro : disnake.Member, *,motivo=None):
    await membro.ban(reason=motivo)
    await inter.response.send_message(f'{inter.author.mention} baniu {membro.mention} por {motivo}')


@bot.slash_command(name='help', description='Veja como utilizar o Gunter')
async def help(inter):
    embed = disnake.Embed(
        title='Ajuda',
        description='Lista de comandos:\n\n/ping - Informa o ping do bot\n\n/raiz - Calcula a raiz quadrada de um determinado número\n\n/kick <usuário> <motivo> - Expulsa um usuário do servidor\n\n/ban <usuário> <motivo> - Bane um usuário do servidor\n\n/help - Informa a lista de comandos do Gunter',
        colour=0xF0C43F,
    )
    await inter.response.send_message(embed=embed)


@bot.slash_command(name='avatar', description='Mostra o avatar do usuário')
async def avatar(inter, user: disnake.User):
    embed = disnake.Embed(
        title=f'Avatar de {user}'
        )
    embed.set_image(
        url=user.display_avatar.url
        )
    await inter.response.send_message(embed=embed)


@bot.slash_command(name='say', description='Fale pelo Gunter')
async def say(inter, message):
    await inter.response.send_message(message)


@bot.slash_command(name='mute', description='Silencia o usuária, inserir valores em minutors')
async def mute(inter, member: disnake.Member, time: int, *, reason=None):
    mute_role = disnake.utils.get(member.guild.roles, name='Muted')
    if not mute_role:
        mute_role = await member.guild.create_role(name='Muted')
    await member.add_roles(mute_role, reason=reason)
    await inter.response.send_message(f'{member.mention} foi mutado por {time} minutos.')
    await asyncio.sleep(time * 60)
    await member.remove_roles(mute_role)


@bot.command()
async def mute(ctx, member: disnake.Member, time: int, *, reason=None):
    mute_role = disnake.utils.get(member.guild.roles, name='Muted')
    if not mute_role:
        mute_role = await member.guild.create_role(name='Muted')
    await member.add_roles(mute_role, reason=reason)
    await ctx.send(f'{member.mention} foi mutado por {time} minutos.')
    await asyncio.sleep(time * 60)
    await member.remove_roles(mute_role)


@bot.slash_command(name='unmute', description='Retira o silenciamento do usuário')
async def unmute(inter, member: disnake.Member, *, reason=None):
    mute_role = disnake.utils.get(member.guild.roles, name='Muted')
    await member.remove_roles(mute_role)
    await inter.response.send_message(f'{member.mention} foi desmutado.')


@bot.slash_command(name='drivers', description='Mostra a tabela de pontos de pilotos do ano atual da Fórmula 1')
async def drivers(inter):
    date = datetime.date.today()
    ano = date.year

    urlDrivers = f'https://ergast.com/api/f1/{ano}/driverStandings.json'
    response = requests.get(urlDrivers)

    if response.status_code == 200:
        dadosDrivers = response.json()
        tabela_pontos = ''
        for driver in dadosDrivers['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']:
            tabela_pontos += f'{driver["position"]}º | {driver["Driver"]["givenName"]} {driver["Driver"]["familyName"]} - {driver["points"]} pontos\n'
        await inter.response.send_message(tabela_pontos)
    else:
        await inter.response.send_message(f'Erro ao obter dados: {response.status_code}')


@bot.slash_command(name='teams', description='Mostra a tabela de pontos de construtores do ano atual da Fórmula 1')
async def teams(inter):
    date = datetime.date.today()
    ano = date.year

    urlTeams = f'https://ergast.com/api/f1/{ano}/constructorStandings.json'
    response = requests.get(urlTeams)

    if response.status_code == 200:
        dadosTeams = response.json()
        tabela = ''
        for constructor in dadosTeams['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']:
            tabela += f'{constructor["position"]}º | {constructor["Constructor"]["name"]} - {constructor["points"]} pontos\n'
        await inter.response.send_message(tabela)
    else:
        await inter.response.send_message(f'Erro ao obter dados: {response.status_code}')


bot.run('MY_TOKEN_HERE')
