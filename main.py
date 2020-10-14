  
'''
using discord.py version 1.0.0a
'''
import discord
import asyncio
import re
import multiprocessing
import threading
import concurrent
import random

#BOT_OWNER_ROLE = 'fetch' # change to what you need
#BOT_OWNER_ROLE_ID = "619167796894629899"
  
 

 
oot_channel_id_list = ["765066876085862420",#trivia galaxy sb live
"765776448093945856",#trivia community sb live
"750013797250629653", #velocity gamming sb live
"762870192107421726",#imperio sb live
		 	"755080891004354630",#phonix challenge sb live    
		"765313766128484372", #savage trivia
	"758208917464940555",#marvel hq
	"765159846050922517",#dragon community
	"761638723334832178",#google pro sb live 
"765066876085862420",#bright trivia       
		       "765159845552193556" #dragon community
"759759847028686848"

]

answer_pattern = re.compile(r'(e|not|n|N|Not|E)?([1-3]{1})(\?)?(c|cf|w|W|cnf|conf)?(\?)?$', re.IGNORECASE)

apgscore = 700
nomarkscore = 415
markscore = 300

async def update_scores(content, answer_scores):
    global answer_pattern

    m = answer_pattern.match(content)
    if m is None:
        return False

    ind = int(m[2])-1

    if m[1] is None:
        if m[3] is None:
            if m[4] is None:
                answer_scores[ind] += nomarkscore
            else: # apg
                if m[5] is None:
                    answer_scores[ind] += apgscore
                else:
                    answer_scores[ind] += markscore

        else: # 1? ...
            answer_scores[ind] += markscore

    else: # contains not or n
        if m[3] is None:
            answer_scores[ind] -= nomarkscore
        else:
            answer_scores[ind] -= markscore

    return True

class SelfBot(discord.Client):

    def __init__(self, update_event, answer_scores):
        super().__init__()
        global oot_channel_id_list
        #global wrong
        self.oot_channel_id_list = oot_channel_id_list
        self.update_event = update_event
        self.answer_scores = answer_scores

    async def on_ready(self):
        print("======================")
        print("Lion trivia Pro")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

    # @bot.event
    # async def on_message(message):
    #    if message.content.startswith('-debug'):
    #         await message.channel.send('d')

        def is_scores_updated(message):
            if message.guild == None or \
                str(message.channel.id) not in self.oot_channel_id_list:
                return False

            content = message.content.replace(' ', '').replace("'", "")
            m = answer_pattern.match(content)
            if m is None:
                return False

            ind = int(m[2])-1

            if m[1] is None:
                if m[3] is None:
                    if m[4] is None:
                        self.answer_scores[ind] += nomarkscore
                    else: # apg
                        if m[5] is None:
                            self.answer_scores[ind] += apgscore
                        else:
                            self.answer_scores[ind] += markscore

                else: # 1? ...
                    self.answer_scores[ind] += markscore

            else: # contains not or n
                if m[3] is None:
                    self.answer_scores[ind] -= nomarkscore
                else:
                    self.answer_scores[ind] -= markscore

            return True

        while True:
            await self.wait_for('message', check=is_scores_updated)
            self.update_event.set()

class Bot(discord.Client):

    def __init__(self, answer_scores):
        super().__init__()
        self.bot_channel_id_list = []
        self.embed_msg = None
        self.embed_channel_id = None
        #global wrong
        self.answer_scores = answer_scores

        # embed creation
	
        self.embed=discord.Embed(title= "**__Lion Trivia| PRO__**",description = '***Connected with HQ Trivia....***', color=0x0099E1)
        self.embed.set_author(name ='',url=' ',icon_url='')
        self.embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/737039356249768006/737042737790189618/Screenshot_20200727-013331_Chrome.jpg")
        self.embed.add_field(name="**__ANSWER__** 1️⃣", value="0.0", inline=True)
        self.embed.add_field(name="**__ANSWER__** 2️⃣", value="0.0", inline=True)
        self.embed.add_field(name="**__ANSWER__** 3️⃣", value="0.0", inline=True)
        
        
        self.embed.set_footer(text=f"©️ HQ Trivia | Made By Sonu")
            #icon_url="https://cdn.discordapp.com/attachments/655852277550022679/666537435089600512/hqtriviaandroidapp_2.jpg")

        #await self.bot.add_reaction(embed,':spy:')


    async def clear_results(self):
        for i in range(len(self.answer_scores)):
            self.answer_scores[i]=0

    async def update_embeds(self):
      #  global wrong

         

        one_check = ""
        two_check = ""
        three_check = ""
        four_check = ""
        mark_check_one="❶"
        mark_check_two="❷"
        mark_check_three="❸"
        mark_check_four=""
        best_answer = ' :hourglass: '
        
        
        lst_scores = list(self.answer_scores)
        

        highest = max(lst_scores)
        best_answer = ' :hourglass: '
        lowest = min(lst_scores)
        answer = lst_scores.index(highest)+1
        #global wrong             

        if highest > 0:
            if answer == 1:
                one_check = "  <:emoji_1:737033795517153372>"
                mark_check_one = ":one:"
                best_answer = ':one:'
            else:
                one_check = ""

            if answer == 2:
                two_check = "  <:emoji_1:737033795517153372>"
                mark_check_two = ":two:"
                best_answer = ':two:'
            else:
                two_check = ""

            if answer == 3:
                three_check = "  <:emoji_1:737033795517153372>"
                mark_check_three = ":three:"
                best_answer = ':three:'
            else:
                three_check = ""
                
            if answer == 4:
                four_check = "✅"
                mark_check_four = ":four:"
                best_answer = ':four:'
            else:
                four_check = ""

            

        if lowest < 0:
            if answer == 1:
                one_cross = " :x:"
            if answer == 2:
                two_cross = " :x:"
            if answer == 3:
                three_cross = " :x:"            
            if answer == 4:
                four_cross = " :x:"
		
   
        self.embed.set_field_at(0, name=f"**__ANSWER__** {mark_check_one}", value="**{0}**{1}".format(lst_scores[0], one_check))
        self.embed.set_field_at(1, name=f"**__ANSWER__** {mark_check_two}", value="**{0}**{1}".format(lst_scores[1], two_check))
        self.embed.set_field_at(2, name=f"**__ANSWER__** {mark_check_three}", value="**{0}**{1}".format(lst_scores[2], three_check))
	

        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("Lion Trivia Pro")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

        await self.clear_results()
        await self.update_embeds()
        #await self.change_presence(activity=discord.Game(name='with '+str(len(set(self.get_all_members())))+' users'))
        await self.change_presence(activity=discord.Activity(type=1,name='with HQ-TRIVIA'))

    async def on_message(self, message):

        # if message is private
        if message.author == self.user or message.guild == None:
            return

        if message.content.lower() == "+hq":
		
            #if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
                self.embed_msg = None
                await self.clear_results()
                await self.update_embeds()
                self.embed_msg = \
                    await message.channel.send('',embed=self.embed)
                await self.embed_msg.add_reaction("✅")
                # await self.embed_msg.add_reaction(":white_check_mark:")
                #await self.embed_msg.add_reaction("")

                self.embed_channel_id = message.channel.id
          # else:
               #await message.channel.send("**Lol** You Not Have permission To Use This **cmd!** :stuck_out_tongue_winking_eye:")

        # process votes
        if message.channel.id == self.embed_channel_id:
            content = message.content.replace(' ', '').replace("'", "")
            updated = await update_scores(content, self.answer_scores)
            if updated:
                await self.update_embeds()

def bot_with_cyclic_update_process(update_event, answer_scores):

    def cyclic_update(bot, update_event):
        f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
        while True:
            update_event.wait()
            update_event.clear()
            f.cancel()
            f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
            #res = f.result()

    bot = Bot(answer_scores)

    upd_thread = threading.Thread(target=cyclic_update, args=(bot, update_event))
    upd_thread.start()

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start('NzY1OTUxNTQxMzAyNTI1OTYy.X4cR9g.Y19mhh4Q2FZekjEh94fVKW7sws0'))
    loop.run_forever()
	
def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('NjE5MTY3Nzk2ODk0NjI5ODk5.X4bbxg.ceXHJpWlQvRcbV98aZODrOReh6A',  
                                   bot=False))
    loop.run_forever()

if __name__ == '__main__':

    # running bot and selfbot in separate OS processes

    # shared event for embed update
    update_event = multiprocessing.Event()

    # shared array with answer results
    answer_scores = multiprocessing.Array(typecode_or_type='i', size_or_initializer=4)

    p_bot = multiprocessing.Process(target=bot_with_cyclic_update_process, args=(update_event, answer_scores))
    p_selfbot = multiprocessing.Process(target=selfbot_process, args=(update_event, answer_scores))

    p_bot.start()
    p_selfbot.start()

    p_bot.join()
    p_selfbot.join()




 
 
