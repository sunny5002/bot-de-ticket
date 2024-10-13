import discord 
import json
import asyncio
from discord import app_commands
from discord.ext import commands 
from discord.ext import commands
from discord.ui import View, Select
from discord import Interaction, Embed, Color
import time
from datetime import datetime
import pytz
from discord import Embed, Color, ButtonStyle, Button, Interaction, ui
from discord.ui import Button, View

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents = discord.Intents.default()
intents.message_content = True
intents = discord.Intents.default()
intents.message_content = True
permissoes =discord.Intents.default()
permissoes.message_content = True
permissoes.members = True

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())







@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, id=1287261529716031529)  # Substitua pelo nome do canal
    if channel is not None:
        embed = discord.Embed(
            title=f'Seja bem-vindo(a), {member.name}!',
            description='Você entrou no servidor Advanced Bots!',
            color=0x0099ff
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name='Verifique nossos produtos e entre em contato com o suporte!',
                        value='Se tiver alguma dúvida, estamos aqui para ajudar!')
        embed.set_footer(text='Advanced Bots - todos os direitos reservados.')

        await channel.send(embed=embed)
 






@bot.command(name='dm')
async def dm(ctx, member: discord.Member, *, mensagem: str):
    if ctx.author.id in [1264180097573978216, 630620171983126568]:
        try:
            await member.send(mensagem)
            await ctx.send(f'Mensagem enviada para {member.mention}.')
        except discord.Forbidden:
            await ctx.send(f'Não foi possível enviar a mensagem para {member.mention}.')
        except Exception as e:
            print(f"Erro ao enviar mensagem direta: {e}")
            await ctx.send('Esta interação falhou.')
    else:
        await ctx.send('Você não tem permissão para usar este comando.')

@bot.command()
async def regras(ctx: commands.Context, *, titule: str):
    try:
        meu_embed = discord.Embed(title='**Regras**', description=titule, color=discord.Color.red())
        
        await ctx.send(embed=meu_embed)
    except discord.Forbidden:
        await ctx.reply('Não foi possível enviar a mensagem.')
    except Exception as e:
        print(f"Erro ao enviar o embed: {e}")
        await ctx.send('Esta interação falhou.')
               



@bot.command()
async def enviar(ctx: commands.Context, *, titule: str):
    try:
        meu_embed = discord.Embed(description=titule, color=discord.Color.purple())
        
        await ctx.send(embed=meu_embed)
    except discord.Forbidden:
        await ctx.reply('Não foi possível enviar a mensagem.')
    except Exception as e:
        print(f"Erro ao enviar o embed: {e}")
        await ctx.send('Esta interação falhou.')




@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and after.channel.name == "╰➕criar-sua-sala":
        try:
            guild = member.guild
            channel_name = "🌍temporaria"
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(connect=False),
                member: discord.PermissionOverwrite(connect=True)
            }

            # Permitir que todos os bots se conectem
            for bot in guild.members:
                if bot.bot:
                    overwrites[bot] = discord.PermissionOverwrite(connect=True, speak=True)

            # Cria o canal de voz temporário
            channel = await guild.create_voice_channel(name=channel_name, overwrites=overwrites)
            print(f"Canal de voz '{channel_name}' criado.")

            # Move o membro para o canal criado
            await member.move_to(channel)
            print(f"Membro {member.display_name} movido para o canal '{channel_name}'.")

            # Aguarda até que o membro saia do canal temporário
            def check(member_check, before_check, after_check):
                return member_check == member and before_check.channel == channel and after_check.channel is None

            await bot.wait_for('voice_state_update', check=check, timeout=None)

            # Deleta o canal temporário após o membro sair
            await channel.delete()
            print(f"Canal '{channel_name}' deletado após {member.display_name} sair.")

        except discord.Forbidden:
            print("Não tenho permissão para criar ou deletar canais de voz.")
        except discord.HTTPException as e:
            print(f"Ocorreu um erro ao criar ou deletar o canal de voz: {e}")



@bot.event
async def on_ready():
    print(f'Bot está pronto. Nome: {bot.user.name}')
    await bot.change_presence(activity=discord.Streaming(name="Advenced Bots", url="http://twitch.tv/streamer"))
    try:
        # Sync commands to the Discord API
        await bot.tree.sync()
        print("Comandos sincronizados com sucesso.")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")






    




adm_id =1264180097573978216
@bot.command()
async def botao(ctx: commands.Context, *, txt: str):

    # Função que será chamada ao clicar no botão de notificação
    async def notificar_usuario(interaction: discord.Interaction, cliente: discord.Member, canal_ticket: discord.TextChannel):
        # Verifica se o usuário que interagiu tem o cargo autorizado
        cargo_autorizado = discord.utils.get(interaction.guild.roles, id=1287280534409576510)
        
        if cargo_autorizado in interaction.user.roles:
            # Notifica o cliente (quem abriu o ticket)
            await cliente.send(f'{cliente.mention},Seu ticket está sendo atendido agora! {canal_ticket.mention}')
            await interaction.response.send_message('Notificação enviada ao cliente!', ephemeral=True)
        else:
            await interaction.response.send_message('Você não tem permissão para notificar o usuário.', ephemeral=True)

    # Função que será chamada ao clicar no botão de abrir ticket
    async def abrir_ticket_suport_or_comprar(interaction: discord.Interaction):
        
        categoria_ticket = discord.utils.get(interaction.guild.categories, id=1287462281961013268)
        
        # Cria o canal do ticket
        canal_ticket = await interaction.guild.create_text_channel(
            f'📂{interaction.user}', 
            category=categoria_ticket
        )
        
        # Define as permissões do canal
        
        
        await canal_ticket.set_permissions(interaction.guild.default_role, view_channel=False)  # Ninguém pode ver
        await canal_ticket.set_permissions(interaction.user, view_channel=True, send_messages=True)  # Criador pode ver
        
        # Permissões para administradores
        for role in interaction.guild.roles:
            if role.permissions.manage_channels:
                await canal_ticket.set_permissions(role, view_channel=True)

        # Embed de sucesso
        meu_embed1 = discord.Embed(
            title='**Ticket criado com sucesso!📌**',
            description=f'''**{interaction.user.mention}, por favor, aguarde o atendimento. **

> **• Para cancelar, clique no botão vermelho.**
> **• Os botões cinzas são exclusivos para a equipe de suporte.**

> **DESCREVA O MOTIVO DO CONTATO COM O MÁXIMO DE DETALHES POSSÍVEIS PARA FACILITAR O ATENDIMENTO.**


''',
            
            color=discord.Color.from_rgb(128, 0, 128)
        )
        meu_embed1.set_footer(text='Advenced Bots - SUPORTE')

        # Criação da view com os botões
        view_ticket = View(timeout=None)

        # Botão de cancelar ticket
        botao_cancelar = Button(label="Cancelar Ticket", style=discord.ButtonStyle.red)
        botao_cancelar.callback = lambda i: canal_ticket.delete()
        view_ticket.add_item(botao_cancelar)

        # Botão de notificar usuário (cinza)
        cliente = interaction.user  # Armazena o cliente para futuras interações
        botao_notificar = Button(label="Notificar Usuário", style=discord.ButtonStyle.grey)
        botao_notificar.callback = lambda i: notificar_usuario(i, cliente, canal_ticket)
        view_ticket.add_item(botao_notificar)

        # Função para criar uma chamada de voz
        async def criar_call(interaction: discord.Interaction):
            cargo_autorizado = discord.utils.get(interaction.guild.roles, id=1287280534409576510)
            if cargo_autorizado in interaction.user.roles:
                canal_chamada = await interaction.guild.create_voice_channel(
                    name=f'📞call-{interaction.user}',
                    user_limit=2,
                    category=categoria_ticket
                )
                
                # Define permissões do canal de chamada
                await canal_chamada.set_permissions(interaction.guild.default_role, view_channel=False)
                await canal_chamada.set_permissions(interaction.user, view_channel=True, connect=True)
                await canal_chamada.set_permissions(cargo_autorizado, view_channel=True, connect=True)

                # Verifica se o usuário está em um canal de voz
                if interaction.user.voice is not None:
                    # Move o usuário para a chamada de voz
                    await interaction.user.move_to(canal_chamada)
                    await interaction.response.send_message(f'Você foi movido para {canal_chamada.mention}.', ephemeral=True)
                else:
                    await interaction.response.send_message('Você precisa estar em um canal de voz para ser movido.', ephemeral=True)
            else:
                await interaction.response.send_message('Você não tem permissão para criar uma chamada.', ephemeral=True)

        # Botão de criar chamada de voz (verde)
        botao_chamada = Button(label="Criar Chamada", style=discord.ButtonStyle.green)
        botao_chamada.callback = criar_call
        view_ticket.add_item(botao_chamada)

        # Envia a mensagem no canal do ticket com os botões
        await canal_ticket.send(embed=meu_embed1, view=view_ticket)
        adm = interaction.guild.get_member(adm_id)  # Busca o membro pelo ID
        if adm is not None:
            await adm.send(f'{adm.mention}, novo ticket criado. Atenda o mais rápido possível: {canal_ticket.mention}')
        else:
            await interaction.response.send_message('Não foi possível encontrar o administrador para notificação.', ephemeral=True)
        await interaction.response.send_message(f'Ticket criado: {canal_ticket.mention}', ephemeral=True)

    # Botão principal para abrir o ticket
    botao_abrir_ticket = Button(label="Suporte", style=discord.ButtonStyle.primary, emoji="🎫")
    botao_abrir_ticket.callback = abrir_ticket_suport_or_comprar

    # Criação da view principal
    view_principal = View(timeout=None)
    view_principal.add_item(botao_abrir_ticket)

    # Embed da mensagem principal
    meu_embed_principal = discord.Embed(
        title='<:logo:1287461766741102703> | Advanced bots',
        description=txt,
        color=discord.Color.from_rgb(128, 0, 128)
    )

    # Envia a mensagem com o botão de abrir ticket
    await ctx.send(embed=meu_embed_principal, view=view_principal)


























@bot.tree.command(name='fechebk')
async def fechebk1(interaction: Interaction, *, fechebk: str, estrelas: int):
   
    
    if estrelas > 5:
        estrelas = 5
    estrelas_visuais = '⭐' * estrelas

    canal_avalições_id = 1287502102347780147
    canal_avaliçoes = interaction.guild.get_channel(canal_avalições_id)

    if canal_avaliçoes is None:
        await interaction.response.send_message("Canal de avaliações não encontrado!", ephemeral=True)
        return

    
    fuso_horario = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(fuso_horario)

    
    hora_formatada = agora.strftime('%d de %B de %Y às %H:%M')

    
    meu_embed = Embed(
        title='Advanced bots | fechebk',
        description=(f'''
        > **<:pessoa:1290833690636849172> | Avaliador.**
        >    • {interaction.user.mention}

        > **💬 | O breve resumo do Avaliador.**
        >    • `{fechebk}`

        > **⭐| Estrelas**
        >    • {estrelas_visuais}

        > **⏰ | Avaliado em**
        >    <:seta:1290833782810873929> `{hora_formatada}`
        '''),
        color=Color.blue()
    )

    
    await canal_avaliçoes.send(embed=meu_embed)

    
    await interaction.response.send_message(
        f'{interaction.user.mention}, muito obrigado por avaliar a Advanced bots! '
        f'Confira sua avaliação no canal: {canal_avaliçoes.mention}'
    )
    





@bot.command(name='send_dms')
async def send_dms(ctx, message:str):
    if ctx.author.id ==1264180097573978216:
    
        for guild in bot.guilds:
            
            for member in guild.members:
                try:
                    
                    await member.send(message)
                    print(f"DM enviada para {member.name}#{member.discriminator}")
                except discord.Forbidden:
                    print(f"Não foi possível enviar DM para {member.name}#{member.discriminator}")

    
        




@bot.command()
@commands.has_permissions(administrator=True)
async def menu(ctx, *, mensagem: str):
    print("Comando menu foi chamado")  # Log para confirmar que o comando foi executado
    
    async def notificar_usuario(interaction: discord.Interaction, cliente: discord.Member, canal_ticket: discord.TextChannel):
        await interaction.response.defer()
        cargo_autorizado = discord.utils.get(interaction.guild.roles, id=1287280534409576510)
        
        if cargo_autorizado in interaction.user.roles:
            await cliente.send(f'{cliente.mention}, Seu ticket está sendo atendido agora! {canal_ticket.mention}')
            await interaction.followup.send('Notificação enviada ao cliente!', ephemeral=True)
        else:
            await interaction.followup.send('Você não tem permissão para notificar o usuário.', ephemeral=True)

    async def abrir_ticket_suport_or_comprar(interaction: discord.Interaction):
        await interaction.response.defer()
        categoria_ticket = discord.utils.get(interaction.guild.categories, id=1287462281961013268)
        
        # Cria o canal do ticket
        canal_ticket = await interaction.guild.create_text_channel(
            f'📂{interaction.user}', 
            category=categoria_ticket
        )
        
        # Define as permissões do canal
        await canal_ticket.set_permissions(interaction.guild.default_role, view_channel=False)  # Ninguém pode ver
        await canal_ticket.set_permissions(interaction.user, view_channel=True, send_messages=True)  # Criador pode ver
        
        # Permissões para administradores
        for role in interaction.guild.roles:
            if role.permissions.manage_channels:
                await canal_ticket.set_permissions(role, view_channel=True)

        # Armazena a hora de criação do ticket
        ticket_criado_em = datetime.now()

        # Embed de sucesso
        meu_embed1 = discord.Embed(
            title='**Ticket criado com sucesso!📌**',
            description=f'''**{interaction.user.mention}, por favor, aguarde o atendimento. **

> **• Para cancelar, clique no botão vermelho.**
> **• Os botões cinzas são exclusivos para a equipe de suporte.**

> **DESCREVA O MOTIVO DO CONTATO COM O MÁXIMO DE DETALHES POSSÍVEIS PARA FACILITAR O ATENDIMENTO.**
''',
            color=discord.Color.from_rgb(128, 0, 128)
        )
        meu_embed1.set_footer(text='Advanced Bots - SUPORTE')

        # Criação da view com os botões
        view_ticket = discord.ui.View(timeout=None)

        # Botão de cancelar ticket
        botao_cancelar = discord.ui.Button(label="Cancelar Ticket", style=discord.ButtonStyle.red,emoji='<:X_:1290801455250407455>')
        async def cancelar_callback(interaction):
            await canal_ticket.delete()
        botao_cancelar.callback = cancelar_callback
        view_ticket.add_item(botao_cancelar)

        # Botão de notificar usuário (cinza)
        cliente = interaction.user
        botao_notificar = discord.ui.Button(label="Notificar Usuário", style=discord.ButtonStyle.grey,emoji='<:sininho:1290802427452461078>')
        botao_notificar.callback = lambda i: notificar_usuario(i, cliente, canal_ticket)
        view_ticket.add_item(botao_notificar)

        # Botão de assumir ticket (cinza)
        botao_assumir = discord.ui.Button(label="Assumir Ticket", style=discord.ButtonStyle.grey,emoji='🔒')

        async def botao_assumir_callback(interaction: discord.Interaction):
            membro = interaction.user
            cargo_autorizado = discord.utils.get(interaction.guild.roles, id=1287280534409576510)

            if cargo_autorizado in membro.roles:
                # Calcula o tempo que o ticket levou para ser assumido
                tempo_decorrido = datetime.now() - ticket_criado_em
                tempo_decorrido_str = str(tempo_decorrido).split(".")[0]  # Remove os microssegundos

                meu_embed1.add_field(name='Ticket assumido por', value=f'{membro.mention}')
                meu_embed1.add_field(name='Tempo até ser assumido', value=tempo_decorrido_str)  # Adiciona o tempo decorrido
                await interaction.response.edit_message(embed=meu_embed1)
            else:
                await interaction.response.send_message('Você não tem permissão para assumir este ticket.', ephemeral=True)

        botao_assumir.callback = botao_assumir_callback
        view_ticket.add_item(botao_assumir)

        

        async def criar_call(interaction: discord.Interaction):
            await interaction.response.defer()
            cargo_autorizado = discord.utils.get(interaction.guild.roles, id=1287280534409576510)
            if cargo_autorizado in interaction.user.roles:
                canal_chamada = await interaction.guild.create_voice_channel(
                    name=f'💎call-{interaction.user}',
                    user_limit=2,
                    category=categoria_ticket
                )
                
                # Define permissões do canal de chamada
                await canal_chamada.set_permissions(interaction.guild.default_role, view_channel=False)
                await canal_chamada.set_permissions(interaction.user, view_channel=True, connect=True)
                await canal_chamada.set_permissions(cargo_autorizado, view_channel=True, connect=True)

                # Move o usuário para a chamada de voz
                if interaction.user.voice is not None:
                    await interaction.user.move_to(canal_chamada)
                    await interaction.followup.send(f'Você foi movido para {canal_chamada.mention}.', ephemeral=True)
                else:
                    await interaction.followup.send('Você precisa estar em um canal de voz para ser movido.', ephemeral=True)
            else:
                await interaction.followup.send('Você não tem permissão para criar uma chamada.', ephemeral=True)

        botao_chamada = discord.ui.Button(label="Criar Chamada", style=discord.ButtonStyle.grey,emoji='<:suporte:1290796850848206959>')
        botao_chamada.callback = criar_call
        view_ticket.add_item(botao_chamada)

        # Envia a mensagem no canal do ticket com os botões
        await canal_ticket.send(embed=meu_embed1, view=view_ticket)
        
        # Notifica um administrador sobre o ticket criado
        adm_id = 1264180097573978216  # Substitua pelo ID real do administrador
        adm = interaction.guild.get_member(adm_id)
        if adm is not None:
            await adm.send(f'{adm.mention}, novo ticket criado. Atenda o mais rápido possível: {canal_ticket.mention}')
        else:
            await interaction.followup.send('Não foi possível encontrar o administrador para notificação.', ephemeral=True)
        
        await interaction.followup.send(f'Ticket criado: {canal_ticket.mention}', ephemeral=True)

    async def mensagem_Parceria(interaction: discord.Interaction):
        id_canal = 1290338242826338355
        canal_denuncias = ctx.guild.get_channel(id_canal)
        await interaction.response.send_message(f'Mande sua Parceria aqui <:seta:1290833782810873929>  {canal_denuncias.mention}', ephemeral=True)

    # Função que será chamada ao selecionar uma opção no menu
    async def seleção_escolhida(interaction: discord.Interaction):
        selected_value = select.values[0]

        if selected_value == 'Loja':
            await abrir_ticket_suport_or_comprar(interaction)
        elif selected_value == 'Suporte':
            await abrir_ticket_suport_or_comprar(interaction)
        elif selected_value == 'Parceria':
            await mensagem_Parceria(interaction)

    # Opções para o seletor
    options = [
        discord.SelectOption(label='Loja', description='Adquira nossos produtos.', emoji='<:carinho:1290798641715613716>'),
        discord.SelectOption(label='Suporte', description='Podemos te auxiliar no que for necessário.', emoji='<:suporte:1290796850848206959>'),
        discord.SelectOption(label='Parceria', description='Seja Parceiro.', emoji='<:parceiro:1290802635557048352>')
    ]

    # Criação do seletor
    select = discord.ui.Select(placeholder='Selecione uma opção...', options=options)
    select.callback = seleção_escolhida

    # Criação da view
    view = discord.ui.View(timeout=None)
    view.add_item(select)

    # Embed e envio da mensagem no canal
    meu_embed = discord.Embed(
        title='**Advanced Bots**',
        description=mensagem,
        color=discord.Color.purple(),
    )
    meu_embed.add_field(name='', value='` Advanced Bots - Suporte `')

    meu_embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1287259978599628821/1290346349430308894/Ultra_bots_2.png?ex=66fc202f&is=66faceaf&hm=e4e597cfd308db37232a03c43e2b72a31aea99a74bf5c80fd0f3cf3f3364f6fe&')

    await ctx.send(embed=meu_embed, view=view)



bot.run("SEU_TOKEN")
