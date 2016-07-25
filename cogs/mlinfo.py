import discord
from discord.ext import commands

Class MLRules:

    async def __init__(self, bot)
        self.bot = bot

    @commands.command(no_pm=True, hidden=True, pass_context=True)
    async def mlinfo(self, ctx, user: discord.Member=None)
        await self.bot.send_message(user, "**__WELCOME TO THE OFFICIAL MONSTERLYRICS DISCORD SERVER!__**\n"

"*Take some time to read this all through. We have tried to keep this as short as possible, but there is a lot of important stuff.*\n"

"\n__Never used Discord before? Worry not!__\n"

"\n**1.** Change your profile picture. Click the gear in the bottom left next to your name, and click the big coloured circle."
"\n**2.** Set your theme to dark mode (Settings > Appearance). Seriously. It's 10x better. Your eyes will thank you."
"\n**3.** Setup your microphone. Go to Settings > Voice. *We highly recommend push-to-talk mode*, but you can use Voice Activity as well. "
"\n**Please change your input sensitivity to about 60-70% of the bar.** We don't want to hear you typing! (*But if we will, you will be forced to use PTT (we can actually do that*.))"
"\n**4.** Download the PTB. This is better than the standard build, and allows you to access all the cool features before they come out to the normies! Be cool!"
"\nAvailable at https://discordapp.com/download/. See the gif below for how to install. https://i.imgur.com/X05amh7.gif"


"\n\n\n**__Remember that you have to verify your Discord account with your email to be able to send messages.__**"

"\n\nOurs is a very laid back community, and very accepting, so feel free to join in the conversation. However, we know that not everyone on the internet is mature enough to have a normal conversation, so we have a few rules that must be followed (apart from in #shitpost, where most of the rules do not apply)."

"\n\n__**COMMANDMENTS (THE LAW,** correct punishment included, if broken)__"

"\n\n```"
"\ni. No self promotion. - 1 strike"
"\nii. No spam. - 1 strike"
"\niii. No racism, sexism, or any kind of harassment. - 1 strike"
"\niv. No spoilers. - 1 strike"
"\nv. The only allowed language is English. - 1/2 strike"
"\nvi. No coloured, backwards, upside-down, or in any way flipped text.  - 1/2 strike"
"\nvii. No doxing; Do not share pictures or other personal information without the subject's consent."
"\nviii. No pornographic or in any other way NSFW content. - 1 strike"
"\nix. Request songs at http://monsterlyrics.co/ - You will be corrected"
"\nx. Respect the authority and their instructions. - 1 strike"
"\n```"


"\n\n\n__**RULES **(NOT SERIOUS)__"

"\n\n\n```"
"\n1. Send Jovan your nudes."
"\n2. Send Nik your hate mail."
"\n3. No fangirling/fanboying."
"\n4. Add women when possible to make the chat better."
"\n5. You shall not be liked as the new guy until you send something that will make us chuckle."
"\n6. If you mention that you know someone famous, you must to add them to this chat."
"\n7. No Gyazo links, no links to @Bead210#7892'schannel."
"\n8. No ugly pics of anyone unless they don't get offended."
"\n9. No Valentines rhymes. \N{BROKEN HEART}"
"\n10. Don't death grip."
"\n34. If it exists, there's porn of it."
"\n```"


"\n\n\n**__TIMEOUT__**"
"\nYou will not be able to send messages, or join or speak in voice channels."
"\n```"
"\nCommand breaking - 30 minutes"
"\nBeing a major cunt - 30 minutes"
"\nMultiple Offences At Once - 90 minutes"
"\n```"


"\n\n\n__**STRIKES**__"

"\n\n**Role-based Strike System (RBSS):** For people with the role HJ or above (people with only the anime and/or coding role not included)"

"\n\n```"
"\nFirst (1st) strike - Ninety (90) minutes of timeout."
"\nSecond (2nd) strike - Three (3) hours of timeout and demoted for twenty four (24) hours."
"\nThird (3rd) strike - Twenty four (24) hours of timeout and demoted for the rest of the month, or at least fifteen days, whichever is longer. During this period, the mods will evaluate if the former role should be restored."
"\nFourth (4th) strike - Banned indefinitely."
"\n```"

"\n\n**Jail-based Strike System (JBSS):** For people with either no role or only the anime and/or coding role. "

"\n\n```"
"\nFirst (1st) strike - Thirty (30) minutes of timeout."
"\nSecond (2nd) strike - Three (3) hours of timeout."
"\nThird (3rd) strike - Twenty four (24) hours of timeout."
"\nFourth (4th) strike - Banned indefinitely."
"\n```"

"\n\n***BREAKING THE LAW WITH THE INTENTION OF GETTING PUNISHED WILL RESULT IN TWO STRIKES.***"

"\n\n**__The rules listed above also apply to the Voice Channels. Also remember that we have no voice equivalent of #shitpost.?__**"

"\n\nThe law system above is mainly universal across the channels, but some channels may have more (e.g. #faq) or less (e.g. #shitpost) rules. Not following these rules may result in you losing your permissions in said channels along with getting the normal punishment."
"\n**__Please read the Channel Topics in the channels you speak in. It is as much your responsibility as reading this page is.__**"

"\n\nIf you need any help with the server, feel free to ping the mods! Just tag @Mods or @Helpers, and we will be notified!"

"\n\nIf you have any questions regarding @FishBot, use `!contact <message goes here>`, and you will receive help to fix the issue ASAP. "
"\n*Regarding to the bots in general:* Currently we have only a few bots that can be used in #general. Our main bot, @FishBot, can only be used there by Nerds and above. For the rest of you, and the rest of the bots that are not special, __the bot playgrounds are #shitpost and #test_stuff.__ The audio commands belong in #music."
"\n**__We will not be taking in new bots made by you guys.__**"

"\n\nThis server has a fairly basic role system. You will see people with different roles, such as @Nerds and @HJ (Happy Jammers), but getting these roles is just a matter of patience and loyalty."
"\nWe would like to ask you to not ask for these roles, the mods will give them to you once they feel you've earned them. Type the command `!role promotion` to get more info on our system."

"\n\nHowever, there is one role you may ask for. This role will allow you to access #animewars, a channel dedicated to discussing about, you guessed it, anime. Just type `!selfrole hentai`, or if this doesn't work, tag the @Mods if you watch anime and would like to be a part of the channel. "
"\nEvery three weeks, we will evaluate your chance for promotion to HJ. By being active and nice, you might get promoted to HJ. During the three-week periods we will monitor your performace, picking out people who do well. We compile the candidates into a list, and let the current Nerds vote for their favourites. After the poll, the mods will have their final decision on who they should promote."
"\nThe same principle applies to the Nerd promotion as well, but instead of three-week cycles, we have six-week cycles. "
"\nIn short, this means that you have to wait three weeks to get a chance at becoming a Happy Jammer, and then six weeks on top of that for getting a chance to become a Nerd."
"\nSo, in theory the system will work like this:"
"\nThree weeks after the promotional video of this server went live, aka week 22, we will have our first HJ candidacy poll. Another three weeks later (week 25) we will have another HJ candidacy poll. Then, another three weeks later (week 28), we will have our third HJ candidacy poll, and, since it has been six weeks after the first HJ candidacy poll, we will have our first Nerd candidacy poll, once again, on week 28. "

"\n\nThis is a bit confusing, I know, but apart from the mods, you won't really need to worry about this, since we will keep the rest of you updated."



"\n\n\n\nWe use Message Pinning as our announcement system. Our main announcements will be in #general, while other smaller, channel-specific announcements can be found in the appropriate channels. *A few notes on the system:* at this point, the system is new, and likely to be improved, so there will be changes. The notifications at this point aren't anything grand. This picture will show you what the simple notification will look like, and how you can access the pinned messages. And lastly, the pinned messages are not yet on the mobile builds, so sorry to those who are affected. http://i.imgur.com/sTLnUqN.png"

"\n\nIt is stated in your greeting message that reading thoroughly through this channel is your responsibility, so there is no need for you to complain to us after your possible punishments saying you did not know of the rules, unless we really have left something out on this page."

"\n\n**__By staying on this server you agree to the terms and rules listed above. If you do not, however, you are advised to leave.__**")

    def setup(bot)
        n = MLInfo(bot)
        bot.add_cog(n)