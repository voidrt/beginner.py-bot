from beginner.colors import BLUE
from beginner.cog import Cog, commands
from beginner.scheduler import schedule
from beginner.tags import tag
from datetime import datetime, timedelta
import nextcord
import nextcord.ext.commands
import dateutil.tz


class AdventOfCode(Cog):
    @property
    def raw_now(self):
        return datetime.now(dateutil.tz.gettz("America/New_York"))

    @property
    def now(self):
        return self.raw_now.replace(hour=0, minute=0, second=0, microsecond=0)

    @property
    def christmas(self):
        return datetime(
            2021, 12, 25, 0, 0, 0, tzinfo=dateutil.tz.gettz("America/New_York")
        )

    @property
    def days_till_christmas(self):
        return (self.christmas - self.now).days

    @commands.command(name="aoc")
    async def toggle_aoc_role(self, ctx: commands.Context):
        role = nextcord.utils.get(ctx.guild.roles, name="aoc-announcement")
        if role in ctx.author.roles:
            await ctx.author.remove_roles(role)
            action = "removed from"
        else:
            await ctx.author.add_roles(role)
            action = "given"

        await ctx.send(
            f"🎄 {ctx.author.mention} you've been {action} the Advent of Code announcement role.",
            delete_after=10,
        )

    async def ready(self):
        if self.now < self.christmas + timedelta(days=1):
            print("🎄🎅☃️ 🤶🎄🤶☃️ 🎅🎄")
            print(self.days_till_christmas, "days until Christmas!!!")
            self.schedule_next_challenge_announcement()

    def schedule_next_challenge_announcement(self):
        if self.days_till_christmas:
            schedule(
                "beginnerpy-advent-of-code-2021",
                self.now + timedelta(days=1, minutes=1) - self.raw_now,
                self.send_daily_link,
                no_duplication=True,
            )

    @tag("schedule", "advent-of-code-announcement")
    async def send_daily_link(self):
        role = nextcord.utils.get(self.server.roles, name="aoc-announcement")
        channel = self.get_channel("🎅aoc-announcements")
        show_off = self.get_channel("⛄aoc-discussion")
        help_1 = self.get_channel("🤶advent-of-code-help")
        help_2 = self.get_channel("🎄advent-of-code-help")
        suffixes = {1: "st", 21: "st", 2: "nd", 22: "nd", 3: "rd", 23: "rd"}
        await channel.send(
            content=role.mention,
            embed=nextcord.Embed(
                description=(
                    f"**Here's the [{self.now.day}{suffixes.get(self.now.day, 'th')} challenge]"
                    f"(https://adventofcode.com/2021/day/{self.now.day})!!!**\n\n"
                    f"Show off (spoiler tag please) & discuss in {show_off.mention}!!! Get help in {help_1.mention} or "
                    f"{help_2.mention}.\n\n"
                    f"**Good luck!!!**"
                ),
                title=(
                    f"🎄 {self.days_till_christmas} Days Until Christmas 🎄"
                    if self.days_till_christmas
                    else "🎄🎅☃️  MERRY CHRISTMAS ☃️ 🎅🎄"
                ),
                color=BLUE,
            )
            .add_field(
                name="Beginner.codes Leaderboard",
                value=(
                    "To join our server's leaderboard go [here](https://adventofcode.com/2021/leaderboard/private), "
                    "enter our code in the text box, and then click join.\n\n"
                    "**Beginner.codes Leaderboard Code:** `990847-0adb2be3`"
                ),
            )
            .set_footer(text="Toggle pings for new challenges with the !aoc command"),
        )

        await self.get_channel("🎁aoc-solutions").send(
            embed=nextcord.Embed(
                description=f"🎄🎅❄️ Share your Day {self.now.day} solutions!!! ❄️🎅🎄"
            )
        )

        self.schedule_next_challenge_announcement()


def setup(client):
    client.add_cog(AdventOfCode(client))
