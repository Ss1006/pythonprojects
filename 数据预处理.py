# -*- coding: utf-8 -*-
"""
Created on Thu May 27 10:32:09 2021

@author: 105385
"""

import pandas as pd
import numpy as np
import json
import time
import datetime


'''
点赞表
'''
jsondata=[]
with open(r'D:\work\推荐系统\like.json','r',encoding='utf8') as fp:
    for line in fp.readlines():
        jsondata.append(json.loads(line))

user_id_list=[]
target_id_list=[]
like_time_list=[]        
for i in range(0,len(jsondata)):
    user_id=jsondata[i]['user_id']['$numberLong']
    target_id=jsondata[i]['target_id']
    like_time=jsondata[i]['like_time']
    if like_time.get('$date'):
        y=datetime.datetime.fromtimestamp(like_time['$date']/1000).strftime("%Y-%m-%d")
        like_time_list.append(y)
    else:
        like_time_list.append(0)   
    user_id_list.append(user_id)
    target_id_list.append(target_id)
    
like_df=pd.DataFrame({'user_id':user_id_list,'target_id':target_id_list,'like_time':like_time_list})
like_df['like_rate']=3
user_item_like_df=like_df.groupby('user_id')['target_id'].apply(list).reset_index(name="ModelIDList")
# user_item_df = test.groupby("UserID")["MovieID"].apply(list).reset_index(name="MovieIDList")
# like_df.to_excel(r'D:\work\推荐系统\like_df.xlsx')

'''
评论表
'''
comment_jsondata=[]
with open(r'D:\work\推荐系统\comment.json','r',encoding='utf8') as fp:
    for line in fp.readlines():
        comment_jsondata.append(json.loads(line))

user_id_list=[]
target_id_list=[]
comment_time_list=[]   
for i in range(0,len(comment_jsondata)):
    user_id=comment_jsondata[i]['user_id']['$numberLong']
    target_id=comment_jsondata[i]['target_id']
    comment_time=comment_jsondata[i]['create_time']['$date']
    comment_time=datetime.datetime.fromtimestamp(comment_time/1000).strftime("%Y-%m-%d")
    
    user_id_list.append(user_id)
    target_id_list.append(target_id)
    comment_time_list.append(comment_time)
    
comment_df=pd.DataFrame({'user_id':user_id_list,'target_id':target_id_list,'comment_time':comment_time_list})    
comment_df['comment_rate']=5 
'''
打印表
'''
print_jsondata=[]
with open(r'D:\work\推荐系统\print.json','r',encoding='utf8') as fp:
    for line in fp.readlines():
        print_jsondata.append(json.loads(line))

user_id_list=[]
target_id_list=[]
print_time_list=[]   
for i in range(0,len(print_jsondata)):
    user_id=print_jsondata[i]['user_id']['$numberLong']
    target_id=print_jsondata[i]['model_id']
    print_time=print_jsondata[i]['create_time']['$date']
    print_time=datetime.datetime.fromtimestamp(print_time/1000).strftime("%Y-%m-%d")
    
    user_id_list.append(user_id)
    target_id_list.append(target_id)
    print_time_list.append(print_time)
    
print_df=pd.DataFrame({'user_id':user_id_list,'target_id':target_id_list,'print_time':print_time_list})   
print_df['print_rate']=10
'''
收藏表
'''  

collection_df=pd.read_excel(r'D:\work\推荐系统\collection.xlsx')
collection_df=collection_df.rename(columns={'model_id':'target_id'})
collection_df['collect_rate']=8
collection_df['user_id']=collection_df['user_id'].astype(object)
collection_df['target_id']=collection_df['target_id'].astype(object)

#合并数据
all_data_df=like_df.merge(comment_df,how='outer',on=['user_id','target_id'])
all_data_df=all_data_df.merge(print_df,how='outer',on=['user_id','target_id'])
all_data_df=all_data_df.merge(collection_df,how='outer',on=['user_id','target_id'])

all_data_df.to_excel(r'D:\work\推荐系统\all_data_df.xlsx')




































