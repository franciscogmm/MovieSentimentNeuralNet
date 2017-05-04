from apiclient.discovery import build
import json
import pprint
import sys
import csv
import pandas as pd
from time import time, sleep
import numpy as np
import nltk
import string
#from datetime import date, time, datetime

APINAME = 'youtube'
APIVERSION = 'v3'
APIKEY = 'AIzaSyBlUA4kCLwn9PwH1P1D9UP8U2-zodjYEm0'

#volumes source ('public'), search query ('androide')

service = build(APINAME, APIVERSION, developerKey = APIKEY)

def get_videos(query,max):
    searchrequest = service.search().list(
        q = query, 
        type = 'video',
        part ='id, snippet',
        maxResults = 50).execute()
    
    #initialize
    video_detail_vector = []
    total_video_list = []
    comment_reply_vector = []
    comment_thread_list = []
    numbersearch = 0
    try:
    
        for search_result in searchrequest.get('items', []):
            #get details
            vid_id = search_result['id']['videoId']
            vid_title = search_result['snippet']['title'].encode('UTF-8')
            vid_description = search_result['snippet']['description'].encode('UTF-8')
            vid_published_datetime = search_result['snippet']['publishedAt'].encode('UTF-8')
            numbersearch += 1
            print numbersearch
            #load elements
            contentDetails = service.videos().list(
            id = vid_id,
            part ='contentDetails').execute()
            
            stats = service.videos().list(
            id = vid_id,
            part ='statistics').execute()
            
            #create row
        
            video_detail_vector.append(vid_id) #[0]
            video_detail_vector.append(vid_title) #[1]
            video_detail_vector.append(vid_description) #[2]
            video_detail_vector.append(vid_published_datetime)#[3]
            
                
            #contentDetails
            for details in contentDetails.get("items",[]):
                duration = details['contentDetails']['duration'].encode('utf-8')
                dimension = details['contentDetails']['dimension'].encode('utf-8')
                definition = details['contentDetails']['definition'].encode('utf-8')
                caption = details['contentDetails']['caption'].encode('utf-8')
                
                video_detail_vector.append(duration) #P#DT#H#M#S [4]
                video_detail_vector.append(dimension) #[5]
                video_detail_vector.append(definition) #[6]
                video_detail_vector.append(caption) #[7]
            
            #get statistics
            for vidstats in stats.get("items",[]):
                comments = vidstats['statistics']['commentCount']
                views = vidstats['statistics']['viewCount']
                favorites = vidstats['statistics']['favoriteCount']
                dislikes = vidstats['statistics']['dislikeCount']
                likes = vidstats['statistics']['likeCount']
                
                comments = comments.encode('utf-8')
                views = views.encode('utf-8')
                favorites = favorites.encode('utf-8')
                dislikes = dislikes.encode('utf-8')
                likes = likes.encode('utf-8')
                
                video_detail_vector.append(comments) #[8]
                video_detail_vector.append(views) #[9]
                video_detail_vector.append(favorites) #[10]
                video_detail_vector.append(likes) #[11]
                video_detail_vector.append(dislikes) #[12]
             
            #get comments
            
            comment_threads_results = service.commentThreads().list(
                part = 'id, snippet, replies',
                videoId = vid_id,
                maxResults = 100,
                textFormat = "plainText"
                ).execute()
            countingcommentsThreads = 0
            countingcommentsReplies = 0
            
            for item in comment_threads_results['items']:
                comment = item['snippet']['topLevelComment']
                text = comment['snippet']['textDisplay']
                date = comment['snippet']['publishedAt']
                text = text.encode('utf-8','ignore')
                #text = text.decode('unicode_escape').encode('utf-8','ignore')
                num_replies = item['snippet']['totalReplyCount']
                p_id = item['id']

                countingcommentsThreads += 1

                print str(countingcommentsThreads) + ' - ' + str(query) + ' - ' + vid_title
                #print countingcommentsThreads
                comment_thread_list.append(text)
                comment_thread_list.append(date)
            
                if 'replies' in item.keys():
                    for reply in item['replies']['comments']:
                        r_text = reply['snippet']['textDisplay']
                        r_date = reply['snippet']['publishedAt']
                        r_text = r_text.encode('utf-8','ignore')

                        
                        comment_reply_vector.append(r_text)
                        comment_reply_vector.append(r_date)

                while ("nextPageToken" in comment_threads_results):
                    comment_threads_results = service.commentThreads().list(
                    part = 'id, snippet, replies',
                    videoId = vid_id,
                    pageToken=comment_threads_results["nextPageToken"],
                    textFormat="plainText",
                    ).execute()

                    
                    for item in comment_threads_results['items']:
                        comment = item['snippet']['topLevelComment']
                        text = comment['snippet']['textDisplay']
                        date = comment['snippet']['publishedAt']
                        text = text.encode('utf-8','ignore')
                        #text = text.decode('unicode_escape').encode('utf-8','ignore')
                        num_replies = item['snippet']['totalReplyCount']
                        p_id = item['id']

                        countingcommentsThreads += 1
                        print str(countingcommentsThreads) + ' - ' + str(query) + ' - ' + vid_title

                        comment_thread_list.append(text)
                        comment_thread_list.append(date)
                    
                        if 'replies' in item.keys():
                            for reply in item['replies']['comments']:
                                r_text = reply['snippet']['textDisplay']
                                r_date = reply['snippet']['publishedAt']
                                r_text = r_text.encode('utf-8','ignore')
                                
                                comment_reply_vector.append(r_text)
                                comment_reply_vector.append(r_date)

                        if countingcommentsThreads == max:
                            break
                    if countingcommentsThreads == max:
                        break
                if countingcommentsThreads == max:
                        break            
                
                
            
                comment_thread_list.append(comment_reply_vector)
                comment_reply_vector = []
            
            countingcommentsThreads = 0
            video_detail_vector.append(comment_thread_list) #[13]
            
            #encode as UTF-8
            video_detail_vector[0] = video_detail_vector[0].decode('utf-8').strip() 
            video_detail_vector[1] = video_detail_vector[1].decode('utf-8').strip() 
            video_detail_vector[2] = video_detail_vector[2].decode('utf-8').strip() 
            video_detail_vector[3] = video_detail_vector[3].decode('utf-8').strip() 
            video_detail_vector[0] = video_detail_vector[0].encode('utf-8')
            video_detail_vector[1] = video_detail_vector[1].encode('utf-8')
            video_detail_vector[2] = video_detail_vector[2].encode('utf-8')
            video_detail_vector[3] = video_detail_vector[3].encode('utf-8')
            
            #print video_detail_vector
            #append to total list
            #print video_detail_vector
            total_video_list.append(video_detail_vector)
            
            #refresh row
            video_detail_vector = []
            comment_thread_list = []
        
            print "------------------------------------------------------------------------------"  
            
    except KeyError:
        sleep(60)
    
    return total_video_list
    
movielistz =[]
with open('movie list_2013.csv', 'rb') as csv_in:
    myreader2 = csv.reader(csv_in, delimiter = ',')
    next(myreader2) #skips column headers    

    for row in myreader2:
        moviequery = row[2]
        #print moviequery
        movielistz.append(moviequery)
    print movielistz
counting = 0
for i in movielistz:
    dataz = get_videos(i,5000)
    #totallist.append(dataz)
    counting += 1
    print counting
    filenamez = str(i) + '.csv'
    print dataz
    labels = ['Video ID','Video Title','Video Description','Video Published on', 'Duration','Dimension', 'Definition','Caption','countComments','countViews','countFavorites','countLikes','countDislikes','Comments']
    df = pd.DataFrame.from_records(dataz, columns = labels)
    df.to_csv(filenamez, index = False)
    del df
    
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++"

# dataz = get_videos('Logan movie trailer')
# df = pd.DataFrame.from_records(dataz,columns = labels)
#df = pd.DataFrame.from_records(totallist,columns = labels)
#df.to_csv('output_all.csv', index = False)
