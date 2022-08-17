import discord
from discord.ext import commands, tasks
import discord.ext.forms as forms
import json
import requests

bot = commands.AutoShardedBot(command_prefix = '!')
bot.remove_command('help')

@bot.command()
async def login(ctx, authorizationCode):
    url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
    payload=f'grant_type=authorization_code&code={authorizationCode}'
    headers = {
        'Authorization': 'basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    url2 = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{json.loads(response.text)['account_id']}/deviceAuth"
    payload2={}
    headers2 = {
      'Authorization': f'bearer {json.loads(response.text)["access_token"]}'
    }
    response2 = requests.request("POST", url2, headers=headers2, data=payload2)
    f = open(f"./accounts/{ctx.author}.json", 'w')
    f.write(response2.text)
    url1 = f"https://avatar-service-prod.identity.live.on.epicgames.com/v1/avatar/fortnite/ids?accountIds={json.loads(response.text)['account_id']}"
    payload1={}
    headers1 = {
      'Authorization': f'bearer {json.loads(response.text)["access_token"]}'
    }
    response1 = requests.request("GET", url1, headers=headers1, data=payload1)
    cid = "{}".format(json.loads(json.loads(response1.text))[0]['avatarId']).replace("ATHENACHARACTER:", "")
    embed = discord.Embed(title=f"logged in as {json.loads(response.text)['displayName']}")
    embed.set_thumbnail(url=f"https://fortnite-api.com/images/cosmetics/br/{cid}/icon.png")
    await ctx.send(embed=embed)

@bot.command()
async def accStats(ctx):
    with open(f"./accounts/{ctx.author}.json") as f:
        l = json.load(f)
        url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
        payload=f'grant_type=device_auth&account_id={l["accountId"]}&device_id={l["deviceId"]}&secret={l["secret"]}'
        headers = {
          'Authorization': 'basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=',
          'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload) 
        url1 = f"https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{json.loads(response.text)['account_id']}/client/QueryProfile?profileId=athena&rvn=-1"
        payload1 = json.dumps({})
        headers1 = {
          'Authorization': f'bearer {json.loads(response.text)["access_token"]}',
          'Content-Type': 'application/json'
        }
        response1 = requests.request("POST", url1, headers=headers1, data=payload1)
        embed = discord.Embed(title=f"fortnite account stats for {json.loads(response.text)['displayName']}")
        embed.add_field(name="created at", value=json.loads(response1.text)["profileChanges"][0]["profile"]["created"],inline=False)
        embed.add_field(name="account level", value=json.loads(response1.text)["profileChanges"][0]["profile"]["stats"]["attributes"]["accountLevel"],inline=False)
        embed.add_field(name="battlestars", value=json.loads(response1.text)["profileChanges"][0]["profile"]["stats"]["attributes"]["battlestars"],inline=False)
        embed.add_field(name="level", value=json.loads(response1.text)["profileChanges"][0]["profile"]["stats"]["attributes"]["level"],inline=False)
        embed.add_field(name="lifetime wins", value=json.loads(response1.text)["profileChanges"][0]["profile"]["stats"]["attributes"]["lifetime_wins"],inline=False)
        for i in json.loads(response1.text)["profileChanges"][0]["profile"]["stats"]["attributes"]["past_seasons"]:
            embed.add_field(name="played in season", value=i["seasonNumber"],inline=True)
        await ctx.send(embed=embed)

@bot.command()
async def stats(ctx):
    with open(f"./accounts/{ctx.author}.json") as f:
        l = json.load(f)
        url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
        payload=f'grant_type=device_auth&account_id={l["accountId"]}&device_id={l["deviceId"]}&secret={l["secret"]}'
        headers = {
          'Authorization': 'basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=',
          'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload) 
        url1 = f"https://statsproxy-public-service-live.ol.epicgames.com/statsproxy/api/statsv2/account/{json.loads(response.text)['account_id']}"
        payload1 = {}
        headers1 = {
          'Authorization': f'bearer {json.loads(response.text)["access_token"]}',
          'Content-Type': 'application/json'
        }
        response1 = requests.request("GET", url1, headers=headers1, data=payload1)
        solo=discord.Embed(title="solo-stats")
        solo.add_field(name="solo wins", value=json.loads(response1.text)['stats']['br_placetop1_gamepad_m0_playlist_defaultsolo'], inline=False)
        solo.add_field(name="solo top 10", value=json.loads(response1.text)['stats']['br_placetop10_gamepad_m0_playlist_defaultsolo'], inline=False)
        solo.add_field(name="solo top 25", value=json.loads(response1.text)['stats']['br_placetop25_gamepad_m0_playlist_defaultsolo'], inline=False) 
        solo.add_field(name="solo matches played", value=json.loads(response1.text)['stats']['br_matchesplayed_gamepad_m0_playlist_defaultsolo'], inline=False)
        solo.add_field(name="solo kills", value=json.loads(response1.text)['stats']['br_kills_gamepad_m0_playlist_defaultsolo'], inline=False) 
        solo.add_field(name="players outlived", value=json.loads(response1.text)['stats']['br_playersoutlived_gamepad_m0_playlist_defaultsolo'], inline=False) 
        solo.add_field(name="solo minutes played", value=json.loads(response1.text)['stats']['br_minutesplayed_gamepad_m0_playlist_defaultsolo'], inline=False)

        duo=discord.Embed(title="duo-stats")
        duo.add_field(name="duo wins", value=json.loads(response1.text)['stats']['br_placetop1_gamepad_m0_playlist_defaultduo'], inline=False)
        duo.add_field(name="duo top 12", value=json.loads(response1.text)['stats']['br_placetop12_gamepad_m0_playlist_defaultduo'], inline=False)
        duo.add_field(name="duo matches played", value=json.loads(response1.text)['stats']['br_matchesplayed_gamepad_m0_playlist_defaultduo'], inline=False)
        duo.add_field(name="duo kills", value=json.loads(response1.text)['stats']['br_kills_gamepad_m0_playlist_defaultduo'], inline=False) 
        duo.add_field(name="players outlived", value=json.loads(response1.text)['stats']['br_playersoutlived_gamepad_m0_playlist_defaultduo'], inline=False) 
        duo.add_field(name="duo minutes played", value=json.loads(response1.text)['stats']['br_minutesplayed_gamepad_m0_playlist_defaultduo'], inline=False)
    
        squad=discord.Embed(title="squad-stats")
        squad.add_field(name="squad wins", value=json.loads(response1.text)['stats']['br_placetop1_gamepad_m0_playlist_defaultsquad'], inline=False)
        squad.add_field(name="squad top 6", value=json.loads(response1.text)['stats']['br_placetop6_gamepad_m0_playlist_defaultsquad'], inline=False)
        #squad.add_field(name="squad top 25", value=json.loads(response1.text)['stats']['br_placetop25_gamepad_m0_playlist_defaultsquad'], inline=False) 
        squad.add_field(name="squad matches played", value=json.loads(response1.text)['stats']['br_matchesplayed_gamepad_m0_playlist_defaultsquad'], inline=False)
        squad.add_field(name="squad kills", value=json.loads(response1.text)['stats']['br_kills_gamepad_m0_playlist_defaultsquad'], inline=False) 
        squad.add_field(name="players outlived", value=json.loads(response1.text)['stats']['br_playersoutlived_gamepad_m0_playlist_defaultsquad'], inline=False) 
        squad.add_field(name="squad minutes played", value=json.loads(response1.text)['stats']['br_minutesplayed_gamepad_m0_playlist_defaultsquad'], inline=False)
        rmenu = forms.ReactionMenu(ctx, [solo, duo, squad])
        await rmenu.start()

@bot.command()
async def vbucks(ctx):
    with open(f"./accounts/{ctx.author}.json") as f:
        l = json.load(f)
        url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
        payload=f'grant_type=device_auth&account_id={l["accountId"]}&device_id={l["deviceId"]}&secret={l["secret"]}'
        headers = {
          'Authorization': 'basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=',
          'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload) 
        url1 = f"https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{json.loads(response.text)['account_id']}/client/QueryProfile?profileId=common_core&rvn=-1"
        payload1 = json.dumps({})
        headers1 = {
          'Authorization': f'bearer {json.loads(response.text)["access_token"]}',
          'Content-Type': 'application/json'
        }
        response1 = requests.request("POST", url1, headers=headers1, data=payload1)
        for i in json.loads(response1.text)["profileChanges"][0]["profile"]["items"]:
            if json.loads(response1.text)["profileChanges"][0]["profile"]["items"][i]['templateId'] == 'Currency:MtxGiveaway':
                await ctx.send(f"you have {json.loads(response1.text)['profileChanges'][0]['profile']['items'][i]['quantity']} vbucks")

@bot.command()
async def gold(ctx):
    with open(f"./accounts/{ctx.author}.json") as f:
        l = json.load(f)
        url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
        payload=f'grant_type=device_auth&account_id={l["accountId"]}&device_id={l["deviceId"]}&secret={l["secret"]}'
        headers = {
          'Authorization': 'basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=',
          'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload) 
        url1 = f"https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/br-inventory/account/{json.loads(response.text)['account_id']}"
        payload1 ={}
        headers1 = {
          'Authorization': f'bearer {json.loads(response.text)["access_token"]}'
        }
        response1 = requests.request("GET", url1, headers=headers1, data=payload1)
        await ctx.send(f"you have {json.loads(response1.text)['stash']['globalcash']} gold")

@bot.command()
async def claimstw(ctx):
    with open(f"./accounts/{ctx.author}.json") as f:
        l = json.load(f)
        url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
        payload=f'grant_type=device_auth&account_id={l["accountId"]}&device_id={l["deviceId"]}&secret={l["secret"]}'
        headers = {
          'Authorization': 'basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=',
          'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload) 
        url1 = f"https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{json.loads(response.text)['account_id']}/client/ClaimLoginReward?profileId=campaign"
        payload1 = json.dump("{}")
        headers1 = {
          'Authorization': f'bearer {json.loads(response.text)["access_token"]}'
        }
        response1 = requests.request("POST", url1, headers=headers1, data=payload1)
        await ctx.send(f"claimed stw daily login reward")

@bot.command()
async def shopselections(ctx):
    with open(f"./accounts/{ctx.author}.json") as f:
        l = json.load(f)
        url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
        payload=f'grant_type=device_auth&account_id={l["accountId"]}&device_id={l["deviceId"]}&secret={l["secret"]}'
        headers = {
          'Authorization': 'basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=',
          'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload) 
        url1 = f"https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/calendar/v1/timeline"
        payload1 ={}
        headers1 = {
          'Authorization': f'bearer {json.loads(response.text)["access_token"]}'
        }
        response1 = requests.request("GET", url1, headers=headers1, data=payload1)
        embed = discord.Embed(title="Current Fortnite Shop Selections")
        for i in json.loads(response1.text)['channels']['client-events']['states'][0]['state']['sectionStoreEnds']:
            embed.add_field(name='selection found', value=i, inline=False)
        await ctx.send(embed=embed)

bot.run("")
