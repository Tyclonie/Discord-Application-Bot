print("Getting system information and Importing/Downloading necessary libraries.")

from sys import platform
from datetime import datetime
import os
import json
import sqlite3
import subprocess

try:
    import discord

    discpylog = None
except Exception:
    if platform == "win32":
        discpylog = subprocess.check_output("pip install discord.py")
    else:
        discpylog = subprocess.check_output("pip3 install discord.py")
try:
    from colorama import Fore

    coloramalog = None
except Exception:
    if platform == "win32":
        coloramalog = subprocess.check_output("pip install colorama")
    else:
        coloramalog = subprocess.check_output("pip3 install colorama")

import discord
from discord.ext import commands
from colorama import Fore


def validate(dpylog, colorlog):
    print("Checking file system.")
    try:
        os.listdir("./data")
    except Exception:
        print("Data folder not found, generating data folder.")
        os.mkdir("./data")
    try:
        os.listdir("./dl logs")
    except Exception:
        print("Log folder not found, generating log folder.")
        os.mkdir("./dl logs")
        if dpylog is not None or colorlog is not None:
            print("Pasting library download logs.")
            with open("./dl logs/discordpy-dl-log.txt", "w") as f:
                if dpylog is not None:
                    f.write(dpylog.decode("utf-8"))
            with open("./dl logs/colorama-dl-log.txt", "w") as f:
                if colorlog is not None:
                    f.write(colorlog.decode("utf-8"))
    files = os.listdir("./data")
    if "config.json" not in files:
        print("No config found. Starting generation.")
        token = input("Input bot token: ")
        prefix = input("Input bot prefix: ")
        role = input("Input application manager role id: ")
        channel = input("Input application log channel id: ")
        appchannel = input("Input application channel id: ")
        with open("./data/config.json", "w") as f:
            f.write(
                "{   \n    \"bot_token\": \"" + token + "\",\n    \"bot_prefix\": \"" + prefix + "\",\n    \"manager_role_id\": \"" + role + "\",\n    \"applog_channel_id\": \"" + channel + "\",\n    \"apply_channel_id\": \"" + appchannel + "\",\n    \"apply_with_command\": \"" + "" + "\",\n    \"applications_open\": \"" + "" + "\",\n    \"botlog_channel_id\": \"" + "none" + "\",\n    \"welcome_leave_channel_id\": \"" + "none" + "\",\n    \"welcome_message\": \"" + "Welcome to the server!" + "\",\n    \"leave_message\": \"" + "Sad to see you go!" + "\"\n}")
        with open("./data/config.json", "r+") as f:
            config = json.load(f)
            config["apply_with_command"] = False
            config["applications_open"] = False
            f.seek(0)
            json.dump(config, f, indent=4)
            f.truncate()
        print("Config generated.")
    if "questions.txt" not in files:
        print("No questions file found. Starting generation.")
        with open("./data/questions.txt", "w") as _:
            pass
        print("Questions file generated.")
    if "apps.sqlite" not in files:
        print("No app database found.")
        with open("./data/apps.sqlite", "w") as _:
            pass
        print("App database generated.")
        print("Creating open apps table.")
        conn = sqlite3.connect("./data/apps.sqlite")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS openapps (userid integer, messageid integer)")
        conn.commit()
        conn.close()
    with open("./data/questions.txt") as f:
        questions = f.read()
    if len(questions) < 1:
        print("Found an error with questions file.")
        with open("./data/questions.txt", "w") as f:
            f.write("What is your IGN?\nWhat is your Discord Name and #?")
        print("Error fixed.")


def getinfo(info):
    with open("./data/config.json") as f:
        config = json.load(f)
    if info == "t":
        token = config.get("bot_token")
        return token
    elif info == "p":
        prefix = config.get("bot_prefix")
        return prefix
    elif info == "c":
        appchannelid = config.get("apply_channel_id")
        return appchannelid
    elif info == "l":
        applogchannelid = config.get("applog_channel_id")
        return applogchannelid
    elif info == "r":
        roleid = config.get("manager_role_id")
        return roleid
    elif info == "a":
        command = config.get("apply_with_command")
        return command
    elif info == "o":
        openapps = config.get("applications_open")
        return openapps
    elif info == "j":
        jandl = config.get("welcome_leave_channel_id")
        return jandl
    elif info == "jm":
        join_message = config.get("welcome_message")
        return join_message
    elif info == "lm":
        leave_message = config.get("leave_message")
        return leave_message
    elif info == "b":
        bot_logs = config.get("botlog_channel_id")
        return bot_logs


validate(discpylog, coloramalog)

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix=getinfo("p"), help_command=None, intents=intents)


@client.event
async def on_ready():
    if platform == "win32":
        os.system("cls")
    else:
        os.system("clear")
    print(f"{Fore.MAGENTA}Tyclonie's Application Bot v1.1{Fore.RESET}")
    print(f"Successfully Logged Into: {client.user}")


# MODERATION

@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(colour=discord.Colour.from_rgb(160, 32, 240))
    embed.add_field(name="Purge Log",
                    value=f"{ctx.author.mention} purged {str(amount)} message(s) in {ctx.channel.mention}.")
    embed.set_author(icon_url=client.user.avatar_url, name=client.user)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
    embed.timestamp = datetime.now()
    channel = await client.fetch_channel(getinfo("b"))
    await channel.send(embed=embed)


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason=None):
    await ctx.message.delete()
    embed = discord.Embed(colour=discord.Colour.from_rgb(160, 32, 240))
    embed.add_field(name="Kick Log", value=f"{ctx.author.mention} kicked {user.mention} for {reason}.")
    embed.set_author(icon_url=client.user.avatar_url, name=client.user)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
    embed.timestamp = datetime.now()
    channel = await client.fetch_channel(getinfo("b"))
    await channel.send(embed=embed)
    await user.kick(reason=reason)


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason=None):
    await ctx.message.delete()
    embed = discord.Embed(colour=discord.Colour.from_rgb(160, 32, 240))
    embed.add_field(name="Ban Log", value=f"{ctx.author.mention} banned {user.mention} for {reason}.")
    embed.set_author(icon_url=client.user.avatar_url, name=client.user)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
    embed.timestamp = datetime.now()
    channel = await client.fetch_channel(getinfo("b"))
    await channel.send(embed=embed)
    await user.ban(reason=reason)


# WELCOME + LEAVE

@client.event
async def on_member_join(member):
    channel_id = getinfo("j")
    if channel_id != "none":
        embed = discord.Embed(colour=discord.Colour.from_rgb(160, 32, 240))
        embed.add_field(name="Welcome", value=getinfo("jm"))
        embed.set_author(icon_url=client.user.avatar_url, name=client.user)
        embed.set_footer(icon_url=member.avatar_url, text=member)
        embed.timestamp = datetime.now()
        channel = await client.fetch_channel(channel_id)
        await channel.send(embed=embed)


@client.event
async def on_member_remove(member):
    channel_id = getinfo("j")
    if channel_id != "none":
        embed = discord.Embed(colour=discord.Colour.from_rgb(160, 32, 240))
        embed.add_field(name="Goodbye", value=getinfo("lm"))
        embed.set_author(icon_url=client.user.avatar_url, name=client.user)
        embed.set_footer(icon_url=member.avatar_url, text=member)
        embed.timestamp = datetime.now()
        channel = await client.fetch_channel(channel_id)
        await channel.send(embed=embed)


# APPLICATIONS + MESSAGE HANDLER

@client.event
async def on_message(message):
    prefix = getinfo("p")
    apply_channel_id = getinfo("c")
    if str(message.channel.id) == apply_channel_id and message.content == f"{prefix}apply" and getinfo("o") and getinfo(
            "a"):
        await client.process_commands(message)
    elif str(message.channel.id) == apply_channel_id and message.content == f"{prefix}apply" and getinfo("a"):
        await message.channel.send(f"{message.author.mention} Applications are closed at the moment.", delete_after=10)
    elif str(message.channel.id) != apply_channel_id and message.content == f"{prefix}apply" and getinfo("a"):
        channel = await client.fetch_channel(apply_channel_id)
        await message.channel.send(f"Please apply in: {channel.mention}.")
    elif message.content != f"{prefix}apply":
        await client.process_commands(message)


@client.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name == "📋":
        if payload.channel_id == int(getinfo("c")):
            if payload.user_id != client.user.id:
                with open("./data/questions.txt") as f:
                    questions = f.readlines()
                guild = await client.fetch_guild(payload.guild_id)
                channel = await client.fetch_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                user = await guild.fetch_member(payload.user_id)
                await message.remove_reaction(payload.emoji.name, user)
                if getinfo("o"):
                    embed = discord.Embed(title="Application", colour=discord.Colour.from_rgb(160, 32, 240))
                    embed.set_author(icon_url=client.user.avatar_url, name=client.user)
                    embed.set_footer(icon_url=user.avatar_url, text=user)
                    embed.timestamp = datetime.now()
                    application = await user.send(embed=embed)
                    await channel.send(
                        f"{user.mention} Application has been started in DM's. If you havent recieved a DM, please make sure your DM's are open.",
                        delete_after=10)
                    for q in questions:
                        await user.send(q)
                        msg = await client.wait_for('message', timeout=300, check=lambda
                            m: m.author == user and m.channel.type is discord.ChannelType.private)
                        embed.add_field(name=q, value=msg.content)
                        await application.edit(embed=embed)
                    submit = discord.Embed(title="Submit Application?", colour=discord.Colour.from_rgb(160, 32, 240))
                    submit.add_field(name="To send in your application please type:", value="```\"YES\"```",
                                     inline=False)
                    submit.add_field(name="To cancel your application:", value="```Don't respond.```", inline=False)
                    submit.set_author(icon_url=client.user.avatar_url, name=client.user)
                    submit.set_footer(icon_url=user.avatar_url, text=user)
                    await user.send(embed=submit)
                    msg = await client.wait_for('message', timeout=300, check=lambda
                        m: m.author == user and m.channel.type is discord.ChannelType.private)
                    if msg.content.upper() == "YES":
                        application_channel = await client.fetch_channel(int(getinfo("l")))
                        application_message = await application_channel.send(embed=embed)
                        await application_message.add_reaction("✅")
                        await application_message.add_reaction("❎")
                        conn = sqlite3.connect("./data/apps.sqlite")
                        cur = conn.cursor()
                        cur.execute("INSERT INTO openapps VALUES(?,?)", (user.id, application_message.id,))
                        conn.commit()
                        conn.close()
                        await user.send("Application Sent!")
                    else:
                        await user.send("Application Cancelled!")
                else:
                    await channel.send(f"{user.mention} Applications are closed at the moment.", delete_after=10)
    if payload.channel_id == int(getinfo("l")):
        if payload.user_id != client.user.id:
            guild = await client.fetch_guild(payload.guild_id)
            channel = await client.fetch_channel(payload.channel_id)
            user = await guild.fetch_member(payload.user_id)
            manager_role = discord.utils.get(guild.roles, id=int(getinfo("r")))
            if manager_role in user.roles:
                await channel.send("Leave a message for the user?: ")
                note = await client.wait_for('message', timeout=300,
                                             check=lambda m: m.author == user and m.channel == channel)
                await channel.send("Give the user a role? (none for none) (enter name CaSE SeNSitTIVe): ")
                role = await client.wait_for('message', timeout=300,
                                             check=lambda m: m.author == user and m.channel == channel)
                if role.content != "none":
                    role_given = discord.utils.get(guild.roles, name=role.content)
                else:
                    role_given = None
                conn = sqlite3.connect("./data/apps.sqlite")
                cur = conn.cursor()
                cur.execute("SELECT userid FROM openapps WHERE messageid = ?", (payload.message_id,))
                userid = cur.fetchone()[0]
                conn.commit()
                conn.close()
                if payload.emoji.name == "✅":
                    if userid is None:
                        await channel.send(f"{user.mention} this application has already been reviewed.")
                    else:
                        member = await guild.fetch_member(userid)
                        if member is None:
                            await channel.send(f"{user.mention} this user has left the server.")
                        else:
                            embed = discord.Embed(colour=discord.Colour.from_rgb(160, 32, 240))
                            embed.add_field(name="Application Accepted",
                                            value=f"Accepted By: {user.mention}\nNote: {note.content}\nRole Given: {role.content}")
                            embed.set_author(icon_url=client.user.avatar_url, name=client.user)
                            embed.set_footer(icon_url=member.avatar_url, text=member)
                            embed.timestamp = datetime.now()
                            if role_given is not None:
                                await member.add_roles(role_given)
                            await member.send(embed=embed)
                            await channel.send(f"{member.mention}'s application was reviewed by {user.mention}")
                elif payload.emoji.name == "❎":
                    if userid is None:
                        await channel.send(f"{user.mention} this application has already been reviewed.")
                    else:
                        member = await guild.fetch_member(userid)
                        if member is None:
                            await channel.send(f"{user.mention} this user has left the server.")
                        else:
                            embed = discord.Embed(colour=discord.Colour.from_rgb(160, 32, 240))
                            embed.add_field(name="Application Denied",
                                            value=f"Accepted By: {user.mention}\nNote: {note.content}\nRole Given: {role.content}")
                            embed.set_author(icon_url=client.user.avatar_url, name=client.user)
                            embed.set_footer(icon_url=member.avatar_url, text=member)
                            embed.timestamp = datetime.now()
                            if role_given is not None:
                                await member.add_roles(role_given)
                            await member.send(embed=embed)
                            await channel.send(f"{member.mention}'s application was reviewed by {user.mention}")
                conn = sqlite3.connect("./data/apps.sqlite")
                cur = conn.cursor()
                cur.execute("DELETE FROM openapps WHERE messageid = ?", (payload.message_id,))
                conn.commit()
                conn.close()

            else:
                guild = await client.fetch_guild(payload.guild_id)
                channel = await client.fetch_channel(payload.channel_id)
                user = await guild.fetch_member(payload.user_id)
                embed = discord.Embed(colour=discord.Colour.from_rgb(160, 32, 240))
                embed.add_field(name="Permission Error:",
                                value=f"{user.mention} does not have permission to review applications.")
                embed.set_author(icon_url=client.user.avatar_url, name=client.user)
                embed.set_footer(icon_url=user.avatar_url, text=user)
                embed.timestamp = datetime.now()
                await channel.send(embed=embed)


@client.command()
async def apply(ctx):
    await ctx.message.delete()
    with open("./data/questions.txt") as f:
        questions = f.readlines()
    embed = discord.Embed(title="Application", colour=discord.Colour.from_rgb(160, 32, 240))
    embed.set_author(icon_url=client.user.avatar_url, name=client.user)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
    embed.timestamp = datetime.now()
    application = await ctx.author.send(embed=embed)
    await ctx.send(
        f"{ctx.author.mention} Application has been started in DM's. If you havent recieved a DM, please make sure your DM's are open.",
        delete_after=10)
    for q in questions:
        await ctx.author.send(q)
        msg = await client.wait_for('message', timeout=300, check=lambda
            m: m.author == ctx.author and m.channel.type is discord.ChannelType.private)
        embed.add_field(name=q, value=msg.content)
        await application.edit(embed=embed)
    submit = discord.Embed(title="Submit Application?", colour=discord.Colour.from_rgb(160, 32, 240))
    submit.add_field(name="To send in your application please type:", value="```\"YES\"```", inline=False)
    submit.add_field(name="To cancel your application:", value="```Don't respond.```", inline=False)
    submit.set_author(icon_url=client.user.avatar_url, name=client.user)
    submit.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
    await ctx.author.send(embed=submit)
    msg = await client.wait_for('message', timeout=300, check=lambda
        m: m.author == ctx.author and m.channel.type is discord.ChannelType.private)
    if msg.content.upper() == "YES":
        application_channel = await client.fetch_channel(int(getinfo("l")))
        application_message = await application_channel.send(embed=embed)
        await application_message.add_reaction("✅")
        await application_message.add_reaction("❎")
        conn = sqlite3.connect("./data/apps.sqlite")
        cur = conn.cursor()
        cur.execute("INSERT INTO openapps VALUES(?,?)", (ctx.author.id, application_message.id,))
        conn.commit()
        conn.close()
        await ctx.author.send("Application Sent!")
    else:
        await ctx.author.send("Application Cancelled!")


@client.command()
async def applicationmenu(ctx, *, applymessage="To apply, react below!"):
    await ctx.message.delete()
    embed = discord.Embed(colour=discord.Colour.from_rgb(160, 32, 240))
    embed.add_field(name="Application Menu", value=applymessage)
    embed.set_author(icon_url=client.user.avatar_url, name=client.user)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
    embed.timestamp = datetime.now()
    applicationmenumsg = await ctx.send(embed=embed)
    await applicationmenumsg.add_reaction("📋")


@client.command()
async def settings(ctx, *, args=None):
    manager_role = discord.utils.get(ctx.guild.roles, id=int(getinfo("r")))
    if manager_role in ctx.author.roles:
        if args is not None:
            args = args.split()
            new_id = args[1].strip("<").strip(">").strip("#").strip("@").strip("&")
            embed = discord.Embed(colour=discord.Colour.from_rgb(160, 32, 240))
            if args[0] == "manager_role_id":
                with open("./data/config.json", "r+") as f:
                    config = json.load(f)
                    config["manager_role_id"] = new_id
                    f.seek(0)
                    json.dump(config, f, indent=4)
                    f.truncate()
                    set_to = discord.utils.get(ctx.guild.roles, id=int(new_id))
                    embed.add_field(name="Setting Changed", value=f"{args[0]} has been set to {set_to.mention}")
            elif args[0] == "applog_channel_id":
                with open("./data/config.json", "r+") as f:
                    config = json.load(f)
                    config["applog_channel_id"] = new_id
                    f.seek(0)
                    json.dump(config, f, indent=4)
                    f.truncate()
                    set_to = await client.fetch_channel(new_id)
                    embed.add_field(name="Setting Changed", value=f"{args[0]} has been set to {set_to.mention}")
            elif args[0] == "apply_channel_id":
                with open("./data/config.json", "r+") as f:
                    config = json.load(f)
                    config["apply_channel_id"] = new_id
                    f.seek(0)
                    json.dump(config, f, indent=4)
                    f.truncate()
                    set_to = await client.fetch_channel(new_id)
                    embed.add_field(name="Setting Changed", value=f"{args[0]} has been set to {set_to.mention}")
            elif args[0] == "apply_with_command":
                appcommand = not bool(getinfo("a"))
                with open("./data/config.json", "r+") as f:
                    config = json.load(f)
                    config["apply_with_command"] = appcommand
                    f.seek(0)
                    json.dump(config, f, indent=4)
                    f.truncate()
                    embed.add_field(name="Setting Changed", value=f"{args[0]} has been set to ```{str(appcommand)}```")
            elif args[0] == "applications_open":
                appcommand = not bool(getinfo("o"))
                with open("./data/config.json", "r+") as f:
                    config = json.load(f)
                    config["applications_open"] = appcommand
                    f.seek(0)
                    json.dump(config, f, indent=4)
                    f.truncate()
                    embed.add_field(name="Setting Changed", value=f"{args[0]} has been set to ```{str(appcommand)}```")
            elif args[0] == "botlog_channel_id":
                with open("./data/config.json", "r+") as f:
                    config = json.load(f)
                    config["botlog_channel_id"] = new_id
                    f.seek(0)
                    json.dump(config, f, indent=4)
                    f.truncate()
                    set_to = await client.fetch_channel(new_id)
                    embed.add_field(name="Setting Changed", value=f"{args[0]} has been set to {set_to.mention}")
            elif args[0] == "welcome_leave_channel_id":
                with open("./data/config.json", "r+") as f:
                    config = json.load(f)
                    config["welcome_leave_channel_id"] = new_id
                    f.seek(0)
                    json.dump(config, f, indent=4)
                    f.truncate()
                    set_to = await client.fetch_channel(new_id)
                    embed.add_field(name="Setting Changed", value=f"{args[0]} has been set to {set_to.mention}")
            elif args[0] == "welcome_message":
                sentence = ""
                for x in range(len(args) - 1):
                    sentence += args[x + 1] + " "
                with open("./data/config.json", "r+") as f:
                    config = json.load(f)
                    config["welcome_message"] = sentence
                    f.seek(0)
                    json.dump(config, f, indent=4)
                    f.truncate()
                    embed.add_field(name="Setting Changed", value=f"{args[0]} has been set to ```{sentence}```")
            elif args[0] == "leave_message":
                sentence = ""
                for x in range(len(args) - 1):
                    sentence += args[x + 1] + " "
                with open("./data/config.json", "r+") as f:
                    config = json.load(f)
                    config["leave_message"] = sentence
                    f.seek(0)
                    json.dump(config, f, indent=4)
                    f.truncate()
                    embed.add_field(name="Setting Changed", value=f"{args[0]} has been set to ```{sentence}```")
            embed.set_author(icon_url=client.user.avatar_url, name=client.user)
            embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
            embed.timestamp = datetime.now()
            await ctx.send(embed=embed)
        else:
            p = getinfo("p")
            re = getinfo("r")
            l = getinfo("l")
            c = getinfo("c")
            a = getinfo("a")
            o = getinfo("o")
            b = getinfo("b")
            jandl = getinfo("j")
            jm = getinfo("jm")
            lm = getinfo("lm")
            log = await client.fetch_channel(int(l))
            app = await client.fetch_channel(int(c))
            bot_log = await client.fetch_channel(int(b))
            jandl_channel = await client.fetch_channel(int(jandl))
            embed = discord.Embed(colour=discord.Colour.from_rgb(160, 32, 240))
            embed.add_field(name="Set channel command format:",
                            value=f"```{p}settings <name> <#channel/@role/toggle>\n{p}settings apply_channel_id #apply-here\n{p}settings applications_open toggle```",
                            inline=False)
            embed.add_field(name="Current Setup:",
                            value=f"**manager_role_id** » {discord.utils.get(ctx.guild.roles, id=int(re)).mention}\n**applog_channel_id** » {log.mention}\n**apply_channel_id** » {app.mention}\n**apply_with_command** » {a}\n**applications_open** » {o}\n**botlog_channel_id** » {bot_log.mention}\n**welcome_leave_channel_id** » {jandl_channel.mention}\n**welcome_message** » {jm}\n**leave_message** » {lm}")
            embed.set_author(icon_url=client.user.avatar_url, name=client.user)
            embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
            embed.timestamp = datetime.now()
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(colour=discord.Colour.from_rgb(160, 32, 240))
        embed.add_field(name="Permission Error:",
                        value=f"{ctx.author.mention} does not have permission to change settings.")
        embed.set_author(icon_url=client.user.avatar_url, name=client.user)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)


@client.command()
async def questions(ctx):
    with open("./data/questions.txt") as f:
        embed = discord.Embed(colour=discord.Colour.from_rgb(160, 32, 240))
        embed.add_field(name="Questions:", value=f.read())
        embed.set_author(icon_url=client.user.avatar_url, name=client.user)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)


@client.command()
async def qadd(ctx, *, question):
    with open("./data/questions.txt", "a") as f:
        embed = discord.Embed(colour=discord.Colour.from_rgb(160, 32, 240))
        embed.add_field(name="Added Question:", value=f"```{question}```", inline=False)
        f.write(f"\n{question}")
    with open("./data/questions.txt") as f:
        embed.add_field(name="Questions Now:", value=f.read(), inline=False)
    embed.set_author(icon_url=client.user.avatar_url, name=client.user)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
    embed.timestamp = datetime.now()
    await ctx.send(embed=embed)


@client.command()
async def qremove(ctx, *, question):
    with open("./data/questions.txt") as f:
        questions = f.read().split("\n")
    questions.remove(question)
    with open("./data/questions.txt", "w") as f:
        f.write("")
    with open("./data/questions.txt", "a") as f:
        for question in questions:
            if questions.index(question) == 0:
                f.write(question)
            else:
                f.write(f"\n{question}")
    embed = discord.Embed(colour=discord.Colour.from_rgb(160, 32, 240))
    embed.add_field(name="Removed Question:", value=f"```{question}```", inline=False)
    with open("./data/questions.txt") as f:
        embed.add_field(name="Questions Now:", value=f.read(), inline=False)
    embed.set_author(icon_url=client.user.avatar_url, name=client.user)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
    embed.timestamp = datetime.now()
    await ctx.send(embed=embed)


# INFORMATION + HELP/GUIDES

@client.command()
async def botinfo(ctx):
    embed = discord.Embed(colour=discord.Colour.from_rgb(160, 32, 240))
    embed.add_field(name="Developer:", value="Tyclonie", inline=False)
    embed.add_field(name="GitHub:", value="[GitHub Page](https://github.com/Tyclonie/Discord-Application-Bot)",
                    inline=False)
    embed.add_field(name="Download:",
                    value="[GitHub Page](https://github.com/Tyclonie/Discord-Application-Bot/releases)", inline=False)
    embed.add_field(name="Coded In:", value="Python 3.10", inline=False)
    embed.add_field(name="Version:", value="1.1", inline=False)
    embed.set_author(icon_url=client.user.avatar_url, name=client.user)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
    embed.timestamp = datetime.now()
    await ctx.send(embed=embed)


@client.command()
async def help(ctx):
    p = getinfo("p")
    embed = discord.Embed(colour=discord.Colour.from_rgb(160, 32, 240))
    embed.add_field(name="Commands:",
                    value=f"**{p}apply** » Start an application with a command\n**{p}applicationmenu** » Open a menu to allow reaction applications\n**{p}questions** » Lists the questions that are used for applications\n**{p}qremove** » Removes the stated question\n**{p}qadd** » Adds the stated question\n**{p}settings** » Change the bot settings/config\n**{p}botinfo** » Basic information about the bot\n**{p}help** » List of commands\n**{p}purge** » Delete a chunk of messages\n**{p}kick** » Kick a member\n**{p}ban** » Ban a member")
    embed.set_author(icon_url=client.user.avatar_url, name=client.user)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
    embed.timestamp = datetime.now()
    await ctx.send(embed=embed)


print("Starting bot.")
client.run(getinfo("t"))
