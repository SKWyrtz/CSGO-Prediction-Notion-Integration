import requests, json
import webscrape

token = 'secret_eZO4nNr15zzanm6cOn6eJi30EAsMODJLtudYxAJ5FBL'

databaseId = "ea3f6564af444aa5a1055d1afece4e08"

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}

def createPage(data):

    createUrl = 'https://api.notion.com/v1/pages'

    name = data["team1"] + " vs " + data["team2"]

    newPageData = {
        "parent": { "database_id": databaseId },
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": name
                        }
                    }
                ]
            },
            "TEAMS": {
                "multi_select": [
                    {
                        "name": data["team1"]
                    },
                    {
                        "name": data["team2"]
                    }
                ]
            },
            "HLTV Link": {
                "url": data["url"]
            },
            "Tournament": {
                "select": {
                    "name": data["tournament"]
                }
            }
        }
    }
    
    data = json.dumps(newPageData)
    # print(str(uploadData))

    res = requests.request("POST", createUrl, headers=headers, data=data)

    print(res.status_code)
    print(res.text)

def readDatabase():
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)
    # print(res.text)
    return data
    #with open('./db.json', 'w', encoding='utf8') as f:
    #    json.dump(data, f, ensure_ascii=False)


def updateNotionDatabase():
    database_matches = readDatabase()

    database_match_urls_list = []
    for e in database_matches['results']:
        database_match_url = e['properties']['HLTV Link']['url']
        database_match_urls_list.append(database_match_url)
    
    hltv_matches = webscrape.find_all_stared_matches()
    #print(database_match_urls_list)
    print(hltv_matches)

    if hltv_matches["url"] not in database_match_urls_list:
        createPage(hltv_matches)
    else:
        print ("not added")
    '''
    for m in hltv_matches:
        print(m)
        if m['url'] not in database_match_urls_list:
            print("ADDED")
        else:
            print("NOT ADDED")
    '''


updateNotionDatabase()

#print(e['properties']['Name']['title'][0]['text']['content'])