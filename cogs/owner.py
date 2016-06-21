import subprocess
import shutil
import discord
from discord.ext import commands
from cogs.utils import checks
from __main__ import set_cog, send_cmd_help, settings

import importlib
import traceback
import logging
import asyncio
import threading
import datetime
import glob
import os
import time
import aiohttp 


log = logging.getLogger("red.owner")


class CogNotFoundError(Exception):
    pass


class CogLoadError(Exception):
    pass


class NoSetupError(CogLoadError):
    pass


class CogUnloadError(Exception):
    pass


class OwnerUnloadWithoutReloadError(CogUnloadError):
    pass


class Owner:
    """All owner-only commands that relate to debug bot operations.
    """

    def __init__(self, bot):
        self.bot = bot
        self.setowner_lock = False
        self.session = aiohttp.ClientSession(loop=self.bot.loop) 
 
    def __unload(self): 
        self.session.close() 

    @commands.command()
    @checks.is_owner()
    async def load(self, *, module: str):
        """Loads a module

        Example: load mod"""
        module = module.strip()
        if "cogs." not in module:
            module = "cogs." + module
        try:
            self._load_cog(module)
        except CogNotFoundError:
            await self.bot.say("That module could not be found.")
        except CogLoadError as e:
            log.exception(e)
            traceback.print_exc()
            await self.bot.say("There was an issue loading the module."
                               " Check your console/logs for more information.")
        except Exception as e:
            log.exception(e)
            traceback.print_exc()
            await self.bot.say('Module was found and possibly loaded but '
                               'something went wrong.'
                               ' Check your console/logs for more information.')
        else:
            set_cog(module, True)
            await self.bot.say("Module enabled.")

    @commands.group(invoke_without_command=True) 
    @checks.is_owner()
    async def unload(self, *, module: str):
        """Unloads a module

        Example: unload mod"""
        module = module.strip()
        if "cogs." not in module:
            module = "cogs." + module
        if not self._does_cogfile_exist(module):
            await self.bot.say("That module file doesn't exist. I will not"
                               " turn off autoloading at start just in case"
                               " this isn't supposed to happen.")
        else:
            set_cog(module, False)
        try:  # No matter what we should try to unload it
            self._unload_cog(module)
        except OwnerUnloadWithoutReloadError:
            await self.bot.say("I cannot allow you to unload the Owner plugin"
                               " unless you are in the process of reloading.")
        except CogUnloadError as e:
            log.exception(e)
            traceback.print_exc()
            await self.bot.say('Unable to safely disable that module.')
        else:
            await self.bot.say("Module disabled.")

    @unload.command(name="all") 
    @checks.is_owner() 
    async def unload_all(self): 
        """Unloads all modules""" 
        cogs = self._list_cogs() 
        still_loaded = [] 
        for cog in cogs: 
            set_cog(cog, False) 
            try: 
                self._unload_cog(cog) 
            except OwnerUnloadWithoutReloadError: 
                pass 
            except CogUnloadError as e: 
                log.exception(e) 
                traceback.print_exc() 
                still_loaded.append(cog) 
        if still_loaded: 
            still_loaded = ", ".join(still_loaded) 
            await self.bot.say("I was unable to unload some cogs: " 
                "{}".format(still_loaded)) 
        else: 
            await self.bot.say("All cogs are now unloaded.")  
 

    @checks.is_owner()
    @commands.command(name="reload")
    async def _reload(self, module):
        """Reloads a module

        Example: reload audio"""
        if "cogs." not in module:
            module = "cogs." + module

        try:
            self._unload_cog(module, reloading=True)
        except:
            pass

        try:
            self._load_cog(module)
        except CogNotFoundError:
            await self.bot.say("That module cannot be found.")
        except NoSetupError:
            await self.bot.say("That module does not have a setup function.")
        except CogLoadError as e:
            log.exception(e)
            traceback.print_exc()
            await self.bot.say("That module could not be loaded. Check your"
                               " console/logs for more information.")
        else:
            set_cog(module, True)
            await self.bot.say("Module reloaded.")

    @commands.command(pass_context=True, hidden=True)
    @checks.is_owner()
    async def debug(self, ctx, *, code):
        """Evaluates code

        Modified function, originally made by Rapptz"""
        code = code.strip('` ')
        python = '```py\n{}\n```'
        result = None

        global_vars = globals().copy() 
        global_vars['bot'] = self.bot 
        global_vars['ctx'] = ctx 
        global_vars['message'] = ctx.message 
        global_vars['author'] = ctx.message.author 
        global_vars['channel'] = ctx.message.channel 
        global_vars['server'] = ctx.message.server 

        try:
            result = eval(code, global_vars, locals()) 
        except Exception as e:
            await self.bot.say(python.format(type(e).__name__ + ': ' + str(e)))
            return

        if asyncio.iscoroutine(result):
            result = await result

        result = python.format(result)
        if not ctx.message.channel.is_private:
            censor = (settings.email, settings.password)
            r = "[EXPUNGED]"
            for w in censor:
                if w != "":
                    result = result.replace(w, r)
                    result = result.replace(w.lower(), r)
                    result = result.replace(w.upper(), r)
        await self.bot.say(result)

    @commands.group(name="set", pass_context=True)
    async def _set(self, ctx):
        """Changes Red's global settings."""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return

    @_set.command(pass_context=True)
    async def owner(self, ctx):
        """Sets owner"""
        if settings.owner != "id_here":
            await self.bot.say("Owner ID has already been set.")
            return

        if self.setowner_lock:
            await self.bot.say("A set owner command is already pending.")
            return

        await self.bot.say("Confirm in the console that you're the owner.")
        self.setowner_lock = True
        t = threading.Thread(target=self._wait_for_answer,
                             args=(ctx.message.author,))
        t.start()

    @_set.command()
    @checks.is_owner()
    async def prefix(self, *prefixes):
        """Sets prefixes

        Must be separated by a space. Enclose in double
        quotes if a prefix contains spaces."""
        if prefixes == ():
            await self.bot.say("Example: setprefix [ ! ^ .")
            return

        self.bot.command_prefix = sorted(prefixes, reverse=True)
        settings.prefixes = sorted(prefixes, reverse=True)
        log.debug("Setting prefixes to:\n\t{}".format(settings.prefixes))

        if len(prefixes) > 1:
            await self.bot.say("Prefixes set")
        else:
            await self.bot.say("Prefix set")

    @_set.command(pass_context=True)
    @checks.is_owner()
    async def name(self, ctx, *, name):
        """Sets Red's name"""
        name = name.strip()
        if name != "":
            await self.bot.edit_profile(settings.password, username=name)
            await self.bot.say("Done.")
        else:
            await send_cmd_help(ctx)

    @_set.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def nickname(self, ctx, *, nickname=""):
        """Sets Red's nickname

        Leaving this empty will remove it."""
        nickname = nickname.strip()
        if nickname == "":
            nickname = None
        try:
            await self.bot.change_nickname(ctx.message.server.me, nickname)
            await self.bot.say("Done.")
        except discord.Forbidden:
            await self.bot.say("I cannot do that, I lack the "
                "\"Change Nickname\" permission.")

    @_set.command(pass_context=True)
    @checks.is_owner()
    async def status(self, ctx, *, status=None):
        """Sets Red's status

        Leaving this empty will clear it."""

        if status:
            status = status.strip()
            await self.bot.change_status(discord.Game(name=status))
            log.debug('Status set to "{}" by owner'.format(status))
        else:
            await self.bot.change_status(None)
            log.debug('status cleared by owner')
        await self.bot.say("Done.")

    @_set.command()
    @checks.is_owner()
    async def avatar(self, url):
        """Sets Red's avatar"""
        try:
            async with self.bot.session.get(url) as r:
                data = await r.read()
            await self.bot.edit_profile(settings.password, avatar=data)
            await self.bot.say("Done.")
            log.debug("changed avatar")
        except Exception as e:
            await self.bot.say("Error, check your console/logs for more information.")
            log.exception(e)
            traceback.print_exc()

    @_set.command(name="token")
    @checks.is_owner()
    async def _token(self, token):
        """Sets Red's login token"""
        if len(token) < 50:
            await self.bot.say("Invalid token.")
        else:
            settings.login_type = "token"
            settings.email = token
            settings.password = ""
            await self.bot.say("Token set. Restart me.")
            log.debug("Just converted to a bot account.")
            

    @_set.command(pass_context=True) 
    @checks.is_owner() 
    async def stream(self, ctx, stream_name=None, *, status=None): 
        """Sets Red's streaming status 
 
        Leaving both stream and status empty will clear it.""" 
 
        if status: 
            status = status.strip() 
            if "twitch.tv/" not in stream: 
                stream = "https://www.twitch.tv/" + stream 
            await self.bot.change_status(discord.Game(type=1, url=stream, name=status)) 
            log.debug('Owner has set streaming status and url to "{}" and {}'.format(status, stream)) 
        elif stream is not None: 
            await send_cmd_help(ctx) 
            return 
        else: 
            await self.bot.change_status(None) 
            log.debug('status cleared by owner') 
        await self.bot.say("Done.") 
 

    @commands.command()
    @checks.is_owner()
    async def shutdown(self):
        """Shuts down Red"""
        await self.bot.logout()

    @commands.command()
    async def join(self, invite_url: discord.Invite=None):
        """Joins new server"""
        msg = ("I have a **BOT** tag, so I must be invited with an OAuth2"
               " link:\n**More perms:** https://l.fishyfing.xyz/moreperms *(allows admin stuffs)*"
               " \n**Less perms:** https://l.fishyfing.xyz/lessperms *(allows general functionality)*")
        await self.bot.say(msg)

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def leave(self, ctx):
        """Leaves server"""
        message = ctx.message

        await self.bot.say("Are you sure you want me to leave this server?"
                           " Type yes to confirm.")
        response = await self.bot.wait_for_message(author=message.author)

        if response.content.lower().strip() == "yes":
            await self.bot.say("Alright. Bye :wave:")
            log.debug('Leaving "{}"'.format(message.server.name))
            await self.bot.leave_server(message.server)
        else:
            await self.bot.say("Ok I'll stay here then.")

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def servers(self, ctx):
        """Lists and allows to leave servers"""
        owner = ctx.message.author
        servers = list.sorted(self.bot.servers)
        server_list = {}
        msg = ""
        for i in range(0, len(servers)):
            server_list[str(i)] = servers[i]
            msg += "{}: {}\n".format(str(i), servers[i].name)
        msg += "\nTo leave a server just type its number."
        await self.bot.say(msg)
        while msg != None:
            msg = await self.bot.wait_for_message(author=owner, timeout=15)
            if msg != None:
                msg = msg.content.strip()
                if msg in server_list.keys():
                    await self.leave_confirmation(server_list[msg], owner, ctx)
                else:
                    break
            else:
                break

    @commands.command(pass_context=True)
    async def users(self, ctx):
        """Current total user count"""
        users = len(set(bot.get_all_members()))
        await self.bot.say(users)    

    @commands.command(pass_context=True) 
    async def contact(self, ctx, *, message : str): 
        """Sends message to the owner""" 
        if settings.owner == "id_here": 
            await self.bot.say("I have no owner set.") 
            return 
        owner = discord.utils.get(self.bot.get_all_members(), id=settings.owner) 
        author = ctx.message.author 
        sender = "New message from `{} ({})` on server `{}`:\n\n".format(author, author.id, message.server.name) 
        message = sender + message 
        try: 
            await self.bot.send_message(owner, message) 
        except discord.errors.InvalidArgument: 
            await self.bot.say("I cannot send your message, I'm unable to find" 
                               "my owner... *sigh*") 
        except discord.errors.HTTPException: 
            await self.bot.say("Your message is too long.") 
        except: 
            await self.bot.say("I'm unable to deliver your message. Sorry.") 
 
    @commands.command() 
    async def info(self): 
        """Shows info about the MonsterLyrics bot"""
        msg = "Hey there! I'm a _fully modular_ bot made by Twentysix and modified by the ***MonsterLyrics Team***.\n"
        msg += "Some stuff about me:\n"
        msg += "\n"
        msg += "**Language:** Python/discord.py\n"
        msg += "**Owner:** <@!116079569349378049>\n"
        msg += "**Scrutinise my code:** <https://fishyfing.xyz/github>\n"
        msg += "**Need more help? Visit the official server and ping me!** <https://discord.me/Red-DiscordBot>\n"
        msg += "**More info:** <https://fishyfing.xyz/bot.html/>\n"
        msg += "**Want me on your server? Use this link:** <https://fishyfing.xyz/invite>"
        await self.bot.say(msg) 
 

    async def leave_confirmation(self, server, owner, ctx):
        if not ctx.message.channel.is_private:
            current_server = ctx.message.server
        else:
            current_server = None
        answers = ("yes", "y")
        await self.bot.say("Are you sure you want me "
                    "to leave {}? (yes/no)".format(server.name))
        msg = await self.bot.wait_for_message(author=owner, timeout=15)
        if msg is None:
            await self.bot.say("I guess not.")
        elif msg.content.lower().strip() in answers:
            await self.bot.leave_server(server)
            if server != current_server:
                await self.bot.say("Done.")
        else:
            await self.bot.say("Alright then.")

    @commands.command()
    async def uptime(self):
        """Shows Red's uptime"""
        up = abs(self.bot.uptime - int(time.perf_counter()))
        up = str(datetime.timedelta(seconds=up))
        await self.bot.say("`Uptime: {}`".format(up))

    @commands.command()
    async def version(self):
        """Shows Red's current version"""
        response = self.bot.loop.run_in_executor(None, self._get_version)
        result = await asyncio.wait_for(response, timeout=10)
        await self.bot.say(result)

    def _load_cog(self, cogname):
        if not self._does_cogfile_exist(cogname):
            raise CogNotFoundError(cogname)
        try:
            mod_obj = importlib.import_module(cogname)
            importlib.reload(mod_obj)
            self.bot.load_extension(mod_obj.__name__)
        except SyntaxError as e:
            raise CogLoadError(*e.args)
        except:
            raise

    def _unload_cog(self, cogname, reloading=False):
        if not reloading and cogname == "cogs.owner":
            raise OwnerUnloadWithoutReloadError(
                "Can't unload the owner plugin :P")
        try:
            self.bot.unload_extension(cogname)
        except:
            raise CogUnloadError

    def _list_cogs(self):
        cogs = glob.glob("cogs/*.py")
        clean = []
        for c in cogs:
            c = c.replace("/", "\\")  # Linux fix
            clean.append("cogs." + c.split("\\")[1].replace(".py", ""))
        return clean

    def _does_cogfile_exist(self, module):
        if "cogs." not in module:
            module = "cogs." + module
        if module not in self._list_cogs():
            return False
        return True

    def _wait_for_answer(self, author):
        print(author.name + " requested to be set as owner. If this is you, "
              "type 'yes'. Otherwise press enter.")
        print()
        print("*DO NOT* set anyone else as owner.")

        choice = "None"
        while choice.lower() != "yes" and choice == "None":
            choice = input("> ")

        if choice == "yes":
            settings.owner = author.id
            print(author.name + " has been set as owner.")
            self.setowner_lock = False
            self.owner.hidden = True
        else:
            print("setowner request has been ignored.")
            self.setowner_lock = False

    def _get_version(self):
        getversion = os.popen(r'git show -s HEAD --format="%cr|%s|%h"')
        getversion = getversion.read()
        version = getversion.split('|')
        return 'Last updated: ``{}``\nCommit: ``{}``\nHash: ``{}``'.format(
            *version)


def setup(bot):
    n = Owner(bot)
    bot.add_cog(n)
