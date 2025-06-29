import discord
import requests
import json


def get_agent(): # get agent information from valorant API
     response = requests.get('https://valorant-api.com/v1/agents?isPlayableCharacter=true') #response from valo API
     if response.status_code ==200:
        return response.json()['data'] # response with json file
     else:
         print("Failed to fetch agent data.")
         
class MyClient(discord.Client):
  async def on_ready(self):
    print('Logged on as {0}!'.format(self.user))

  async def on_message(self, message):
    if message.author == self.user:
      return
    
    if message.content.startswith('$ValAgent'): #initialization message
        _, _, agent_name = message.content.partition(' ')
        agent_name = agent_name.strip().lower()
        
        data = get_agent() #passing json data to data 
        
        for agent in data: #iterate through the data
         if agent['displayName'].lower() == agent_name: #find agent match from the data
            name = agent['displayName']
            role = agent['role']['displayName'] if agent['role'] else "Unknown"
            desc = agent['description']
            portrait = agent.get('displayIcon')
            abilities = agent['abilities']

            ability_names = "\n".join([
                f"{a['displayName']} - [Icon]({a['displayIcon']})"
                for a in abilities
                if a['displayName'] and a['displayIcon']
            ])
            #concat every data 
            embed = discord.Embed(title=name, description=desc)
            embed.set_thumbnail(url=portrait)
            embed.add_field(name="Role", value=role)
            embed.add_field(name="Abilities", value=ability_names or "Unknown")

            await message.channel.send(embed=embed) #display every data 
            return  # <- exits after successful match
            

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('TOKEN HERE') # Replace with your own token