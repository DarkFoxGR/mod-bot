import discord
from discord.ext import commands
import os

# --- ΡΥΘΜΙΣΕΙΣ ---
# Το Token θα το πάρει αυτόματα από το Render (Βήμα 3)
TOKEN = os.getenv('DISCORD_TOKEN')

# ΤΑ IDs ΠΟΥ ΜΟΥ ΕΔΩΣΕΣ
WELCOME_CHANNEL_ID = 1459285588904775727  # Κανάλι: ⛔bot-chat⛔
AUTO_ROLE_ID = 1459285587671646211        # Ρόλος: ⬜️ Friends ⬜️
OWNER_ID = 364849864611201026             # Το δικό σου ID

# Ενεργοποίηση Intents
intents = discord.Intents.default()
intents.members = True          # Για να βλέπει πότε μπαίνει κάποιος
intents.message_content = True  # Για να διαβάζει μηνύματα
intents.moderation = True       # Για να βλέπει Audit Logs (Kick/Ban)

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------ Bot is Online ------')

# 1. Όταν ΜΠΑΙΝΕΙ νέος χρήστης
@bot.event
async def on_member_join(member):
    # Βρίσκουμε το κανάλι και τον ρόλο με βάση τα IDs
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    role = member.guild.get_role(AUTO_ROLE_ID)

    # Προσπάθεια απόδοσης ρόλου
    if role:
        try:
            await member.add_roles(role)
            print(f"Δόθηκε ο ρόλος στον {member.name}")
        except discord.Forbidden:
            print("ΣΦΑΛΜΑ: Το bot δεν έχει δικαίωμα να δώσει τον ρόλο. Ελέγξτε το Role Hierarchy.")
    
    # Αποστολή μηνύματος (Embed)
    if channel:
        embed = discord.Embed(
            title="✨ Νέο Μέλος!",
            description=f"Καλωσόρισες στην παρέα μας, {member.mention}!",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"User ID: {member.id}")
        await channel.send(embed=embed)

# 2. Όταν ΦΕΥΓΕΙ χρήστης (ή τρώει Kick/Ban)
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if not channel:
        return

    # Προεπιλογή: Απλή αποχώρηση
    title = "Αποχώρηση"
    desc = f"Ο χρήστης **{member.name}** έφυγε από τον server."
    color = discord.Color.light_grey()

    # Έλεγχος Audit Logs για να δούμε αν ήταν Kick ή Ban
    try:
        async for entry in member.guild.audit_logs(limit=3):
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
        print(f"Error checking audit logs: {e}")

    embed = discord.Embed(title=title, description=desc, color=color)
    embed.set_footer(text=f"User ID: {member.id}")
    await channel.send(embed=embed)

# Εκκίνηση
if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN not found on Render.")
