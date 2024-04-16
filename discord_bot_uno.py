import discord
from discord.ext import commands
import json
import random
import asyncio
from UNO_data import d, color_emojis


bot = commands.Bot(command_prefix='sm ')

@bot.event
async def on_ready():
    print('Bot is ready.')


@bot.command()
async def uno(ctx):
    async def u_input(info, correct_responses):
        correct_responses.append('quit')
        await user_line(info, bottom_line)  #creates a embed that contains information
        while (msg := await bot.wait_for('message', check=lambda m: m.channel == ctx.channel)).content not in correct_responses:
            await msg.delete()
            await user_line('Sorry, that input is not valid. Enter another value.', bottom_line)
        
        if msg.content == 'quit':
            return 

        await msg.delete()
        return msg.content


    async def who_goes_first(t, v, msg):
        embed = discord.Embed(
            title = 'Who goes first?',
            colour = 0x2875A4 
        )
        embed.set_author(name=f"{ctx.author.display_name}'s Uno Game", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/UNO_Logo.svg/1200px-UNO_Logo.svg.png')
        embed.add_field(name=f'You drawed a {t[0][-1]} while the opponent drawed a {t[1][-1]} . . .', value=v)
        await msg.edit(embed=embed)
        await asyncio.sleep(3)


    async def information(turn: str, desc: str, msg, time=3):
        embed = discord.Embed(
            title = turn,
            colour = 0x2875A4 
        )
        embed.set_author(name=f"{ctx.author.display_name}'s Uno Game", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/UNO_Logo.svg/1200px-UNO_Logo.svg.png')
        embed.add_field(name=desc, value='-'*65)
        await msg.edit(embed=embed)
        await asyncio.sleep(time)


    async def user_line(desc: str, msg):
        embed = discord.Embed(
            colour = 0x2875A4 
        )
        embed.add_field(name=desc, value='-'*65)
        await msg.edit(embed=embed)


    async def card_display(color=None):
        await opp_cards.edit(content='<:UNOBack_0:812327040991625246>'*len(enemy_hand))
        await dc.edit(content=top_discard_card[-1])
        player_hand.sort(key=lambda x: (type(x[1]) == str, x[1]))
        await p_cards.edit(content=''.join([card[-1] for card in player_hand]))
        try:
            await dc.add_reaction(color_emojis[color])
        except KeyError:
            await dc.clear_reactions()


    deck = d.copy()
    random.shuffle(deck)
    top_discard_card = ''
    goes_first = ''
    
    #Setting the discard pile
    for c in deck:
        if c[0] != 'nocolor':
            top_discard_card = c
            break   
    
    top_line = await ctx.send(embed=discord.Embed(title='Template'))

    #Checking who goes first
    a = iter(deck)
    for t in zip(a, a):
        p, e = t[0][1], t[1][1]
        
        if isinstance(p, int) and isinstance(e, int):
            if p > e:
                await who_goes_first(t, 'You go first! Shuffling deck....', top_line)
                goes_first = 'Player'
                break
            elif p < e:
                await who_goes_first(t, 'Opponent goes first! Shuffling deck....', top_line)
                goes_first = 'Enemy'
                break   
            else:
                pass #nums are same
        
        await who_goes_first(t, 'Drawing again . . .', top_line)
    random.shuffle(deck)

    #Dealing out cards
    player_hand, enemy_hand = [], []
    for i in range(7):
        player_hand.append(deck.pop(i))
    for i in range(7):
        enemy_hand.append(deck.pop(i))

    
    await information('Waiting for game to start...', '...', top_line)
    
    #Card startup display
    opp_cards = await ctx.send('<:UNOBack_0:812327040991625246>'*len(enemy_hand))
    dc = await ctx.send(top_discard_card[-1])
    player_hand.sort(key = lambda x: (type(x[1]) == str, x[1]))
    p_cards = await ctx.send(''.join([card[-1] for card in player_hand]))

    bottom_line = await ctx.send(embed=discord.Embed(title='Template'))
    await user_line('. . .', bottom_line)


    #Functions
    async def is_card_playable(played, discarded):
        if played[1] == 'anynum':
            return True
        elif discarded[1] == 'anynum': #any num/special can be played(color needs to be matched)
            if played[0] == discarded[0]:
                return True
            else:
                return False
        elif played[0] == discarded[0] or played[1] == discarded[1]:
            return True
        else:
            return False


    async def draw(p):
        if len(deck) != 0:
            p.append(deck.pop(0))
        else:
            await ctx.send('Deck is out of cards!')


    async def player_move(special=None):
        await information('YOUR TURN', 'waiting for response . . .', top_line)
        if special == 'skip':
            await information('YOUR TURN', 'You were skipped!', top_line, time=1.75)
            return 
        elif special == 'reverse':
            await information('YOUR TURN', 'The direction was reversed!', top_line, time=1.75)
            return
        elif special == 'draw2':
            await information('YOUR TURN', 'You have to draw 2 cards and your turn is over! Drawing 2 cards . . .', top_line)
            for _ in range(2): await draw(player_hand)
            await card_display()
            return
        elif special == '+4':
            await information('YOUR TURN', 'You have to draw 4 cards and your turn is over! Drawing 4 cards . . .', top_line)
            for _ in range(4): await draw(player_hand)
            await card_display()
            return
  
        #Check if there are no cards available to play
        if not any([await is_card_playable(card, top_discard_card) for card in player_hand]):
            await information('YOUR TURN', "You can't play anything. Drawing a card . . .", top_line, time=2)
            #If you STILL can't play a card.
            if not await is_card_playable(deck[0], top_discard_card):
                await information('YOUR TURN', "Your drawed card is still not playable. Your turn ends.", top_line, time=2)
                await draw(player_hand)
                return

            await draw(player_hand)
            await information('YOUR TURN', 'waiting for a response...', top_line)
            await card_display()

        while True:
            i = await u_input('Enter the number corresponding to your card of choice.', [str(n+1) for n in range(len(player_hand))])
            #User quit
            if not i:
                return 'quit'
            
            if await is_card_playable(player_hand[int(i)-1], top_discard_card):
                break
            else:
                await user_line('Sorry, you cannot play that card.', bottom_line)
                await asyncio.sleep(2)
            
        if player_hand[int(i) - 1][1] == 'anynum':  #wild card
            color = await u_input('What color do you want to change it to? Enter R, B, G or Y.', ['R', 'B', 'G', 'Y'])
            #User quit
            if not color:
                return 'quit'

            await user_line('. . . ', bottom_line)
            player_hand[int(i) - 1][0] = color

        await user_line('. . .', bottom_line)    
        await information('YOUR TURN', 'Placing card . . .', top_line, time=1.5)
        return player_hand.pop(int(i)-1)


    async def enemy_move(special=None):
        if special == 'skip':
            await information("OPPONENT'S TURN", 'The opponent was skipped!', top_line)
            return 
        elif special == 'reverse':
            await information("OPPONENT'S TURN", 'The direction was reversed!', top_line)  #In 2 player Uno, reverse=skip
            return
        elif special == 'draw2':
            await information("OPPONENT'S TURN", 'Opponent has to draw 2 cards and your turn starts! Drawing 2 cards . . .', top_line)
            for _ in range(2): await draw(enemy_hand)
            await card_display()
            return
        elif special == '+4':
            await information("OPPONENT'S TURN", 'Opponent has to draw 4 cards and your turn starts! Drawing 4 cards . . .', top_line)
            for _ in range(4): await draw(enemy_hand)
            await card_display()
            return

        if not any([await is_card_playable(card, top_discard_card) for card in enemy_hand]):
            await information("OPPONENT'S TURN", "Opponent can't play anything. Drawing a card . . .", top_line, time=2)
            #If the opp STILL can't play a card.
            if not await is_card_playable(deck[0], top_discard_card):
                await information("OPPONENT'S TURN",  "Opponent's card is still not playable. Your turn starts.", top_line, time=2)
                await draw(enemy_hand)
                return
            await draw(enemy_hand)

        await card_display()
        #Dumb AI
        for i, card in enumerate(enemy_hand):
            if await is_card_playable(card, top_discard_card):
                if card[1] == 'anynum':  #wild card
                    color = random.choice(['R', 'B', 'Y', 'G'])
                    await information("OPPONENT'S TURN", f'The opponent chose the color {color}!', top_line, time=2)
                    card[0] = color
                    await asyncio.sleep(1)

                await information("OPPONENT'S TURN", 'Opponent placing card . . .', top_line, time=1.5)
                return enemy_hand.pop(i)
                

    #Setting the order of the match
    if goes_first == 'Player':
        func_list = [player_move, enemy_move] 
    else:
        func_list = [enemy_move, player_move]

    s = ''
    while len(player_hand) > 0 and len(enemy_hand) > 0:
        for f in func_list:
            if len(player_hand) == 0:
                await ctx.send('You won!')
                return
            elif len(enemy_hand) == 0:
                await ctx.send('Opponent won!')
                return

            if s in ('skip', 'reverse', 'draw2', '+4'):
                await f(s)
                s = ''  #reset
                continue
            else:
                card_played = await f()

            if not card_played:
                continue
            elif card_played == 'quit':
                await ctx.send('Bye bye!')
                return

            #Checks if card is Wild +4
            s = card_played[2] if len(card_played) == 4 else card_played[1]
        
            
            top_discard_card = card_played
            
            
            try:
                await card_display(card_played[0] if card_played[1] == 'anynum' or not card_played else 'remove reaction') 
            except discord.errors.HTTPException:
                if len(player_hand) == 0:
                    await p_cards.delete()
                else:
                    await opp_cards.delete()
    

@bot.command() 
async def getemoji(ctx, *emoji: discord.Emoji):
    for e in emoji:
        u_list.append(f'<:{e.name}:{e.id}>')
        print(u_list)


@bot.command()
async def dump(ctx):
    with open('color_emojis.json', 'w') as f:
        json.dump(u_list, f, indent=4)
        u_list.clear()


@bot.command()
async def cow(ctx):
    embed = discord.Embed(
        title = 'Who goes first?',
        colour = 0x2875A4 
    )
    embed.set_author(name=f"{ctx.author.display_name}'s Uno Game", icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/UNO_Logo.svg/1200px-UNO_Logo.svg.png')
    embed.add_field(name='you drawed a blah and opp drawed a blah', value='oofer')
    embed.set_footer(text='hello down here')
    await ctx.send(embed=embed)




@bot.command(aliases=['rememberword'])
async def remember_word(ctx):
    def check(m):
        return m.content == word 

    words = ['mathematics', 'compiler', 'cookies']
    word = (random.choice(words)).upper()
    await ctx.send('Watch the following letters carefully.')
    start = await ctx.send('-')
    for l in word:
        await start.edit(content=l)
        await asyncio.sleep(1)
    await start.delete()
    try:
        msg = await bot.wait_for('message', check=check, timeout=10)
        await ctx.send(f'{word} is correct!')
    except asyncio.TimeoutError:
        await ctx.send(f'Correct answer was {word}.')





@bot.command(aliases=['8ball', 'test'])
async def _8ball(ctx):
    responses = [
        'As I see it, yes.',
        'Ask again later.',
        'Better not tell you now.',
        'Cannot predict now.',
        'Concentrate and ask again.',
        'Don’t count on it.',
        'It is certain.',
        'It is decidedly so.',
        'Most likely.',
        'My reply is no.',
        'My sources say no.',
        'Outlook not so good.',
        'Outlook good.',
        'Reply hazy, try again.',
        'Signs point to yes.',
        'Very doubtful.',
        'Without a doubt.',
        'Yes.',
        'Yes – definitely.',
        'You may rely on it.'
    ]
    await ctx.send(random.choice(responses))


bot.run('ODA5MTI4MDk5MDQ3NDA3NjM2.YCQlQw.YGBwhc039bbn8utWg-mgio4GJLI')