import os, requests, random
from threading import Thread

# config
threadc = 5
# main
def getFollowers(userid):
    cursor = ''
    followers = []
    req = requests.Session()
    while 1:
        try:
            r = req.get(f'https://friends.roblox.com/v1/users/{userid}/followers?sortOrder=Asc&limit=100&cursor={cursor}').json()
            followers.extend([x['name'] for x in r['data'] if x['isBanned'] == False])
            cursor = r['nextPageCursor']
            if not cursor: return followers
        except Exception as e:
            print('error getting api response', e)

def thread():
    global done
    req = requests.Session()
    while usernames:
        username = usernames.pop(0)
        try:
            r = req.get(f'https://www.roblox.com/user.aspx?username={username}').url
            if 'www.roblox.com/users/' not in r:
                done += 1
                continue
            userid = r.split('/')[-2]
            followers = [x+'\n' for x in getFollowers(userid)]
            with open(f'output/{username}.txt', 'w') as f:
                f.writelines(followers)
            done += 1
        except Exception as e:
            print(f'error scraping {usernames}\'s followers', e)
            usernames.append(usernames)

usernames = open('usernames.txt', 'r').read().splitlines()

done = 0
total = len(usernames)

for i in range(threadc):
    Thread(target=thread).start()

while done < total:
    os.system(f'title Roblox Follower Scraper - {done}/{total}')

input('Finished!')
