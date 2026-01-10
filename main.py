import discord
from discord.ext import commands
import os
from keep_alive import keep_alive  # <--- ΝΕΑ ΓΡΑΜΜΗ 1

# --- ΡΥΘΜΙΣΕΙΣ ---
TOKEN = os.getenv('DISCORD_TOKEN')
WELCOME_CHANNEL_ID = 1459285588904775727 
AUTO_ROLE_ID = 1459285587671646211

intents = discord.Intents.default()
intents.members = True  
intents.message_content = True
intents.moderation = True 

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'ID Χρήστη: 364849864611201026')
    print('------ Bot is Online ------')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        try:
            await member.add_roles(role)
        except discord.Forbidden:
            print("Role error.")

    if channel:
        embed = discord.Embed(
            title="✨ Νέο Μέλος!",
            description=f"Καλωσόρισες στην παρέα μας, {member.mention}!",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"User ID: {member.id}")
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if not channel:
        return

    title = "Αποχώρηση"
    desc = f"Ο χρήστης **{member.name}** έφυγε από τον server."
    color = discord.Color.light_grey()

    try:
        async for entry in member.guild.audit_logs(limit=5):
            if entry.target.id == member.id:
                if entry.action == discord.AuditLogAction.ban:
                    title = "Αποκλεισμός (Ban) 🚫"
                    desc = f"Ο χρήστης **{member.name}** αποκλείστηκε από τον/την **{entry.user.name}**."
                    color = discord.Color.red()
                    break
                elif entry.action == discord.AuditLogAction.kick:
                    title = "Αποβολή (Kick) ❌"
                    desc = f"Ο χρήστης **{member.name}** αποβλήθηκε από τον/την **{entry.user.name}**."
                    color = discord.Color.orange()
                    break
    except Exception as e:
        print(f"Audit log error: {e}")

    embed = discord.Embed(title=title, description=desc, color=color)
    await channel.send(embed=embed)

# --- ΕΚΚΙΝΗΣΗ ---
keep_alive()  # <--- ΝΕΑ ΓΡΑΜΜΗ 2: Ξεκινάει τον Web Server
if TOKEN:
    bot.run(TOKEN)
