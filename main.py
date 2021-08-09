import requests, json
import webscrape
import datetime

token = 'secret_eZO4nNr15zzanm6cOn6eJi30EAsMODJLtudYxAJ5FBL'

databaseId = "ea3f6564af444aa5a1055d1afece4e08"

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}
def createPage(data):
    ISO8601_converted_str = convert_date_string_to_ISO8601(data["date"])

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
            }, 
            "Date": {
                "date": {
                    "start": ISO8601_converted_str
                }
            }
        }
    }
    data = json.dumps(newPageData, default=str)
    # print(str(uploadData))
    res = requests.request("POST", createUrl, headers=headers, data=data)
    print(res.status_code)
    print(res.text)

def convert_date_string_to_ISO8601(string):
    print(string)
    split_string = string.split("-")
    split_string.pop(0)
    final_str = []
    for str in split_string:
        if str.replace(" ", ""):
            final_str.append(int(str))
    print(final_str)
    return datetime.datetime(final_str[0], final_str[1], final_str[2], final_str[3], final_str[4], tzinfo=datetime.timezone(datetime.timedelta(hours=2)))

def readNotionDatabase():
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)
    # print(res.text)
    return data
    #with open('./db.json', 'w', encoding='utf8') as f:
    #    json.dump(data, f, ensure_ascii=False)


def updateNotionDatabase():
    database_matches = readNotionDatabase()

    database_match_urls_list = []
    for e in database_matches['results']:
        database_match_url = e['properties']['HLTV Link']['url']
        database_match_urls_list.append(database_match_url)
    
    hltv_matches = webscrape.find_all_stared_matches()

    matches = list(hltv_matches.items())
    matches.pop()
    for match in matches:
        if match[1]["url"] not in database_match_urls_list:
                createPage(match[1])
        else:
            print ("not added")


updateNotionDatabase()

#print(e['properties']['Name']['title'][0]['text']['content'])