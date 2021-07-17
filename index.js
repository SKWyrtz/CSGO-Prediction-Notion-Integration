import { Client } from '@notionhq/client';

const notion = new Client({ auth: process.env.NOTION_KEY });

const databaseId = process.env.NOTION_DATABASE_ID;

async function addItem (text) {
  try {
    await notion.request({
      path: 'pages',
      method: 'POST',
      body: {
        parent: { database_id: databaseId },
        properties: {
            Name: {
                title: [
                    {
                        "text": {
                            "content": "Review"
                        }
                    }
                ]
            },
            TEAMS: {
                multi_select: [
                    {
                        "name"
                    }
                ]
            },
            HLTV Link: {
                url: "https://www.hltv.org/matches"
            },
            Tournament: {
                select: {
                    name: "IEM Cologne 2021"
                }
            }
        }
    }
    });
    console.log('Success! Entry added.');
  } catch (error) {
    console.error(error.body);
  }
}