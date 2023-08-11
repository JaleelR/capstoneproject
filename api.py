from secret import gnewsapi, youtubeapi
import requests
from models import  db,  Api, Post





yturl = f"https://www.googleapis.com/youtube/v3/search"
gnewsurl = f"https://gnews.io/api/v4/search"



def fetchapidata():
    
        ''' 
        If api object is not in db then get api(youtube api and gnews api) info and put in database
        '''

        if not Api.query.first():
            try:
                '''  Gets youtube api info by url and params essential for code '''
                res = requests.get(yturl, params = {
                "part": "snippet",
                "maxResults" : 4, 
                "videoEmbeddable": True, 
                "q": "Self improvement",
                "type": "video",
                "key": youtubeapi
                    }
                    )
                data = res.json()
                
                ''' for each video we recieved out of the 25 (recieved from param{maxresults}), the title, channeltitle and videoid
                is extracted and saved to apis table'''

                for items in data['items']:
                    api1 = Api(title = items["snippet"]["title"], channeltitle = items["snippet"]["channelTitle"], content = "", videoid = items["id"]["videoId"] )
                    db.session.add(api1)  
                    db.session.commit()  

                ''' Gets youtube api info by url and params essential for code '''

                res = requests.get(gnewsurl, params = { 
                "q": "Self improvement OR growth AND NOT stocks",
                "apikey": gnewsapi,
                "lang": "en"
                    }
                    )
                data = res.json()

                ''' for each article we recieved, the title, content, image and url
                is extracted and saved to apis table'''

                for articles in data['articles']: 
                    api2 = Api(title = articles["title"],  content = articles["content"], img = ["Image"], url = articles["url"]) 
                    db.session.add(api2)    
                    db.session.commit()
                ''' If error getting, adding and/ or commiting, display error  '''
            except Exception as e:
                print(f"An error has ocurred: {e}")
        

def convert_apidb_to_postdb():

    """ 
    Converting api to Posts
    - checkes if api instance has a videoid associated with it
    - if so, add the youtuber attribute values to posts instance that will be videos(to distiguish between articles api and videos api)
    - if not the post will get information from the artilces api
     """

    if not Post.query.first():
        apis= Api.query.all() 
        for api in apis:
            if api.videoid:
                vidposts = Post(title = api.title, text = api.videoid, youtuber = api.channeltitle,  api_id = api.id)
                db.session.add(vidposts)
                db.session.commit()
            else:
                artposts = Post( title =  api.title, text = api.content, api_id = api.id)
                db.session.add(artposts)
                db.session.commit()

