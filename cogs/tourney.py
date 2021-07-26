


#@client.group(aliases = ['t', 'tourney'])
#async def tournament(ctx): 
#    '''
#    Get Tourney info
#    '''
#    if ctx.invoked_subcommand is None:
#        await ctx.send('Invalid sub command passed...')

#@tournament.command(aliases = ['addp'])
#async def addParticipant(ctx, a :str = '', b :str = ''):
#    response = 'empty'
#    if a=='' or b == '':
#        await ctx.send("Please enter participants name and id.\n eg: `h.t addp vinay 506018589904470047`")
#    else:
#        c = a + ' ' + b
#        response = challonge.participants.create('a9mlgb9p', c)
#        await ctx.send(response)