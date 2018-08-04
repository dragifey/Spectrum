import discord, asyncio, random, time, datetime
from discord.ext import commands
defaultColour = 0x36393e
gifLogo = "https://cdn.discordapp.com/attachments/323045050453852170/475197666716811275/SpectrumGIF.gif"
normalLogo = "https://cdn.discordapp.com/attachments/323045050453852170/475200894397579274/Spectrum.png"

class GetInfo:
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def info(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("```Invalid Arguments. Here's what you can do:\n$info user <@user>\n$info server\n$info bot```")

    @info.command(name='user', alias="userinfo")
    async def _user(self, ctx, *, user: discord.Member=None):
        author = ctx.message.author
        guild = ctx.message.guild

        if not user:
            user = author

        roles = [x.name for x in user.roles if x.name != "@everyone"]

        since_created = (ctx.message.created_at - user.created_at).days
        since_joined = (ctx.message.created_at - user.joined_at).days
        user_created = user.created_at.strftime("%d %b %Y %H:%M")
        user_joined = user.joined_at.strftime("%d %b %Y %H:%M")

        created_on = f"{user_created}\n({since_created} days ago)"
        joined_at = f"{user_joined}\n({since_joined} days ago)"

        activity = f"Currently in {user.status} status"

        if user.activity is None:
            pass
        else:
            if str(user.activity).startswith("<discord.activity.Activity"):
                pass
            else:
                activity = f"Playing {user.activity}"

        if roles:
            roles = sorted(roles, key=[x.name for x in guild.role_hierarchy
                                       if x.name != "@everyone"].index)
            roles = "\n".join(roles)
        else:
            roles = "None"

        embed = discord.Embed(description=activity, colour=defaultColour)
        embed.add_field(name="Joined Discord on:", value=created_on, inline=False)
        embed.add_field(name="Joined Server at: ", value=joined_at, inline=False)
        embed.add_field(name="Roles:", value=roles, inline=False)
        embed.set_footer(text=f"User ID: {author.id}")

        name = str(user)
        name = " ~ ".join((name, user.nick)) if user.nick else name

        if user.bot:
            embed.set_author(name=f"{name} [Bot]", url=user.avatar_url)
        elif user.id == 276707898091110400:
            embed.set_author(name=f"{name} [My creator]", url=user.avatar_url)
        elif user.id == 320590882187247617:
            embed.set_author(name=f"{name} [You can also do $botinfo]", url=user.avatar_url)
        else:
            embed.set_author(name=name, url=user.avatar_url)

        if user.avatar_url:
            embed.set_thumbnail(url=user.avatar_url)

        await ctx.send(embed=embed)


    @info.command(name='server', alias="serverinfo", no_pm=True)
    async def _server(self, ctx):
        guild = ctx.message.guild
        online = len([m.status for m in guild.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle])
        total_users = len(guild.members)
        total_bots = len([member for member in guild.members if member.bot == True])
        total_humans = total_users - total_bots
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        passed = (ctx.message.created_at - guild.created_at).days
        created_at = ("Since {}. Over {} days ago."
                      "".format(guild.created_at.strftime("%d %b %Y %H:%M"),
                                passed))

        embed = discord.Embed(description=created_at, colour=discord.Colour(value=defaultColour))
        embed.add_field(name="Region", value=str(guild.region))
        embed.add_field(name="Users", value="{}/{}".format(online, total_users))
        embed.add_field(name="Humans", value=total_humans)
        embed.add_field(name="Bots", value=total_bots)
        embed.add_field(name="Text Channels", value=text_channels)
        embed.add_field(name="Voice Channels", value=voice_channels)
        embed.add_field(name="Roles", value=len(guild.roles))
        embed.add_field(name="Owner", value=str(guild.owner))
        embed.set_footer(text=f"Guild ID:{str(guild.id)}")

        if guild.icon_url:
            embed.set_author(name=guild.name, url=guild.icon_url)
            embed.set_thumbnail(url=guild.icon_url)
        else:
            embed.set_author(name=guild.name)

        await ctx.send(embed=embed)

    @info.command(name='bot', alias="botinfo")
    async def _bot(self, ctx):
        """Show's Spectrum's current information"""
        servers = str(len(self.bot.guilds))
        users = str(len(set(self.bot.get_all_members())))
        channels = str(len(set(self.bot.get_all_channels())))
        em = discord.Embed(description="Some current stats for Spectrum", colour=discord.Colour(value=defaultColour))
        em.add_field(name="Server count:", value=servers, inline=False)
        em.add_field(name="Users bot can see:", value=users, inline=False)
        em.add_field(name="Channels bot can see:", value=channels, inline=False)
        em.set_author(name="Bot Information", icon_url=normalLogo)
        em.set_thumbnail(url=gifLogo)
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(GetInfo(bot))