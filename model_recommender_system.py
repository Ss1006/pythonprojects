# -*- coding: utf-8 -*-
"""
Created on Tue May 25 15:09:19 2021

@author: 105385
"""

import sys
import os
import pandas as pd
from datetime import datetime
import math
import warnings


all_data_df=pd.read_excel(r'D:\work\推荐系统\all_data_df.xlsx')
from sklearn.model_selection import train_test_split
train, test = train_test_split(all_data_df, test_size=0.2, random_state=1)
#print("train", train.columns)

# based on users co-filter

def recall(true, pred):
    """
    recall value = |true == pred|/len(true)
    :param true: dict, {user:[item1, item2]
    :param pred: dict, recommend list for each user. e.g.{user:[(user2, similarity)]}
    :return:
    >>> true = {"u1":["item1", "item2"]}
    >>> pred = {"u1":[("u2", 0.6), ("u3", 0.1)]}
    """
    pred_true = 0
    all_true = 0

    for user, items in pred.items():
        for item in items:
            v, _ = item[0], item[1]
            if v in true[user]:
                pred_true += 1
        all_true += len(true[user])
    if all_true == 0:
        return 0
    return pred_true*1.0 / all_true

def precision(true, pred):
    """
    precision value = |true == pred|/len(pred)
    :param true: dict, {user:[item1, item2]
    :param pred: dict, recommend list for each user. e.g.{user:[(user2, similarity)]}
    >>> true = {"u1":["item1", "item2"]}
    >>> pred = {"u1":[("u2", 0.6), ("u3", 0.1)]}
    :return:
    """
    pred_true = 0
    all_pred = 0
    for user,items in pred.items():
        for item in items:
            v, _ = item[0], item[1]
            if v in true[user]:
                pred_true += 1
            all_pred += 1
    if all_pred == 0:
        return 0
    return pred_true*1.0 / all_pred

def coverage(actual_items, recommend_items):
    """
    coverage = len(set(pred))/len(set(actual_items))
    :param actual_items: set(), all items.
    :param recommend_items: set(), all recommend items
    :return:
    >>> actual_items = set("item1", "item2")
    >>> recommend_items = set("item1")
    """
    if len(set(actual_items)) == 0:
        return 1
    return (len(set(recommend_items))*1.0)/len(set(actual_items))

def popularity(user_cf, train, test, N, K):
    """
    popularity means how many people have watched it. Log transformation is applied for stability.
    :param user_cf: recommend system.
    :param train: dict, the train set.
    :param test: dict, the test set.
    :param N: select top N items to recommend.
    :param K: select the moset K similar users.
    :return:
    >>> train = {"user":["item1", "item2"]}
    >>> test = {"user2":["item2"]}
    """
    item_popularity = dict()
    for user, items in train.items():
        for item in items:
            item_popularity[item] = item_popularity.get(item,0)+1
    ret = 0
    n = 0
    for user in test.keys():
        recommend_list = user_cf.recommend(user, N, K)
        for item,sim in recommend_list:
            ret += math.log(1 + item_popularity[item])
            n += 1
    if n == 0:
        return 0
    ret = ret*1.0/n
    return ret



class UserCF(object):
    """
    用户协同过滤，根据相似用户推荐内容
    """
    def train(self, user_items):
        """
        训练模型
        :return:
        """
        self.user_items = user_items
        # 计算用户的协同矩阵
        self.user_sim_matrix = self.user_similarity(user_items)
        #self.user_sim_matrix = self.improved_user_similarity(user_items)
        return self.user_sim_matrix

    def improved_user_similarity(self, user_items):
        """
        improved the similarity.
        :param user_items: {user1:[model1,model2], user2:[model1]}
        :return:
        """
        # build inverse table for item_users
        item_users = dict()
        for u, items in user_items.items():
            for i in items:
                if i not in item_users:
                    item_users[i] = set()
                item_users[i].add(u)

        # calculate co-rated items between users.
        C = dict()
        N = dict()
        for item, users in item_users.items():
            # each user u and user v both like the same item, similarity add 1/log(1+U(item))
            for u in users:
                N[u] = N.get(u,0) + 1
                if u not in C:
                    C[u] = dict()
                for v in users:
                    if v == u:
                        continue
                    C[u][v] = C[u].get(v,0) + 1/math.log(1+len(users))

        # calculate final similarity matrix W
        W = dict()
        for u, related_users in C.items():
            if u not in W:
                W[u] = dict()
            for v, cuv in related_users.items():
                W[u][v] = cuv / math.sqrt(N[u] * N[v])

        return W



    def user_similarity(self, user_items):
        """
        :param user_items: {user1:[model1,model2], user2:[model1]}
        :return:
        """
        # build inverse table for item_users
        item_users = dict()
        for u, items in user_items.items():
            for i in items:
                if i not in item_users:
                    item_users[i] = set()
                item_users[i].add(u)

        # calculate co-rated items between users.
        C = dict()
        N = dict()
        for item, users in item_users.items():
            for u in users:
                N[u] = N.get(u,0) + 1
                if u not in C:
                    C[u] = dict()
                for v in users:
                    if v == u:
                        continue
                    C[u][v] = C[u].get(v,0) + 1

        # calculate final similarity matrix W
        W = dict()
        for u, related_users in C.items():
            if u not in W:
                W[u] = dict()
            for v, cuv in related_users.items():
                W[u][v] = cuv / math.sqrt(N[u] * N[v])

        return W

    def recommend(self, user, N, K):
        """
        recommend item according to user.
        :param user:
        :param N: the number of recommend items
        :param K: the number of most similar users
        :return:  recommend items dict, {item: similarity}
        """
        already_items = set(self.user_items.get(user, set()))
        recommend_items = dict()
        for v, sim in sorted(self.user_sim_matrix.get(user,dict()).items(), key=lambda x:-x[1])[:K]:
            for item in self.user_items[v]:
                if item in already_items:
                    continue
                recommend_items[item] = recommend_items.get(item,0) + sim
        recommend_item_list = sorted(recommend_items.items(), key=lambda x:-x[1])[:N]
        return recommend_item_list

    def recommend_users(self, users, N, K):
        """

        :param users:
        :param N:
        :param K:
        :return: dict, {user:[model1, model2]}
        """
        recommend_result = dict()
        for user in users:
            recommend_item_list = self.recommend(user, N, K)
            recommend_result[user] = recommend_item_list
        return recommend_result

class ItemCF(object):
    """
    物品协同过滤，根据用户浏览过的物品推荐相似物品
    """
    def train(self, user_items, alpha=0.5, normalization=False):
        """
        训练模型
        :return:
        """
        self.user_items = user_items
        # 计算物品的协同矩阵
        # 基础的ItemCF
        #self.item_sim_matrix = self.item_similarity(user_items, normalization=True)
        # 改进的ItemCF
        #self.item_sim_matrix = self.improved_item_similarity(user_items)
        # 基于哈利波特问题改进的ItemCF 
        self.item_sim_matrix = self.improved_item_similarity2(user_items, alpha=alpha, normalization=normalization)

        return self.item_sim_matrix

    def improved_item_similarity(self, user_items, normalization=False):
        """
        :param user_items: {user1:[model1,model2], user2:[model1]}
        :return: W: {items1: {item2: sim12, item3:sim13}}
        """
        # calculate co-rated users between items.
        C = dict()
        N = dict()
        for user, items in user_items.items():
            for i in items:
                N[i] = N.get(i,0) + 1
                if i not in C:
                    C[i] = dict()
                for j in items:
                    if i == j:
                        continue
                    C[i][j] = C[i].get(j,0) + 1/math.log(1+len(items))

        # calculate final similarity matrix W
        W = dict()
        for i, related_items in C.items():
            if i not in W:
                W[i] = dict()
            for j, cij in related_items.items():
                W[i][j] = cij / math.sqrt(N[i] * N[j])

        if normalization:
            for i, item_list in W.items():
                item_list = [item/max(item_list) for item in item_list]
                W[i] = item_list
        return W

    def improved_item_similarity2(self, user_items, alpha=0.5, normalization=False):
        """
        :param user_items: {user1:[model1,model2], user2:[model1]}
        :return: W: {items1: {item2: sim12, item3:sim13}}
        """
        # calculate co-rated users between items.
        C = dict()
        N = dict()
        for user, items in user_items.items():
            for i in items:
                N[i] = N.get(i,0) + 1
                if i not in C:
                    C[i] = dict()
                for j in items:
                    if i == j:
                        continue
                    C[i][j] = C[i].get(j,0) + 1/math.log(1+len(items))

        # calculate final similarity matrix W
        W = dict()
        for i, related_items in C.items():
            if i not in W:
                W[i] = dict()
            for j, cij in related_items.items():
                # if N[i] < N[j]:
                W[i][j] = cij / (N[i]**(1-alpha) * N[j]**alpha)
                # else:
                #     W[i][j] = cij / (N[j] ** (1 - alpha) * N[i] ** alpha)

        if normalization:
            for i, item_list in W.items():
                item_list = [item/max(item_list) for item in item_list]
                W[i] = item_list
        return W

    def item_similarity(self, user_items, normalization=False):
        """
        :param user_items: {user1:[model1,model2], user2:[model1]}
        :return: W: {items1: {item2: sim12, item3:sim13}}
        """
        # calculate co-rated users between items.
        C = dict()
        N = dict()
        for user, items in user_items.items():
            for i in items:
                N[i] = N.get(i,0) + 1
                if i not in C:
                    C[i] = dict()
                for j in items:
                    if i == j:
                        continue
                    C[i][j] = C[i].get(j,0) + 1

        # calculate final similarity matrix W
        W = dict()
        for i, related_items in C.items():
            if i not in W:
                W[i] = dict()
            for j, cij in related_items.items():
                W[i][j] = cij / math.sqrt(N[i] * N[j])

        if normalization:
            for i, item_sim_dict in W.items():
                max_val = max(item_sim_dict.values())
                #print(max_val)
                for j,sim in item_sim_dict.items():
                    item_sim_dict[j] = sim/max_val


        return W

    def recommend(self, user, N, K):
        """
        recommend item according to the history items of users.
        :param user:
        :param N: the number of recommend items
        :param K: the number of most similar users
        :return:  recommend items dict, {item: similarity}
        """
        already_items = set(self.user_items.get(user, set()))
        recommend_items = dict()

        for i in already_items:
            for j, sim in sorted(self.item_sim_matrix.get(i,dict()).items(), key=lambda x:-x[1])[:K]:
                if j in already_items:
                    continue
                recommend_items[j] = recommend_items.get(j,0) + sim
        recommend_item_list = sorted(recommend_items.items(), key=lambda x:-x[1])[:N]
        return recommend_item_list

    def recommend_users(self, users, N, K):
        """

        :param users:
        :param N:
        :param K:
        :return: dict, {user:[model1, model2]}
        """
        recommend_result = dict()
        for user in users:
            recommend_item_list = self.recommend(user, N, K)
            recommend_result[user] = recommend_item_list
        return recommend_result

def train_user_cf(train_df):
    user_cf = UserCF()
    # user_item_df = train_df.groupby("UserID")["ModelID"].apply(list).reset_index(name="ModelIDList")
    # user_item_dict = dict(zip(user_item_df["UserID"], user_item_df["ModelIDList"]))
    item_user_df = train_df.groupby("ModelID")["UserID"].apply(list).reset_index(name="UserIDList")
    data = dict(zip(item_user_df["ModelID"], item_user_df["UserIDList"]))
    #print("data",user_item_dict)
    W = user_cf.train(data)
    # print("W", W)
    # print(user_cf.recommend(208, 10, 3))
    # print(user_cf.recommend_users([1,2,3,4,5,600], 10, 3))
    return user_cf, data

def train_item_cf(train_df):
    item_cf = ItemCF()
    user_item_df = train_df.groupby("UserID")["ModelID"].apply(list).reset_index(name="ModelIDList")
    user_item_dict = dict(zip(user_item_df["UserID"], user_item_df["ModelIDList"]))
    # item_user_df = train_df.groupby("modelID")["UserID"].apply(list).reset_index(name="UserIDList")
    # data = dict(zip(item_user_df["modelID"], item_user_df["UserIDList"]))
    #print("data",user_item_dict)
    W = item_cf.train(user_item_dict)
    print(item_cf.recommend(7198150169, 10, 3))
    print(item_cf.recommend_users([7198150169,5463815327,6337959232,7808717148,2277198261], 10, 5))
    return item_cf, user_item_dict


def evaluate(user_cf, train_dict, test_dict, N, K):
    """
    evaluate models
    :param N:
    :param K:
    :return:
    """
    recommend_dict = user_cf.recommend_users(test_dict.keys(), N=N, K=K)

    # recall
    recall_val = recall(true=test_dict, pred=recommend_dict)
    precision_val = precision(true=test_dict, pred=recommend_dict)

    actual_items = set()
    for item_list in train_dict.values():
        for item in item_list:
            if item not in actual_items:
                actual_items.add(item)
    print("actual_items", len(actual_items))

    recommend_items = set()
    for item_list in recommend_dict.values():
        for (item,sim) in item_list:
            if item not in recommend_items:
                recommend_items.add(item)
    print("recommend_items", len(recommend_items))
    coverage_val = coverage(actual_items=actual_items, recommend_items=recommend_items)

    # item_popularity = dict()
    # for item_list in train_dict.values():
    #     for item in item_list:
    #         item_popularity[item] = item_popularity.get(item,0)+1

    popularity_val = popularity(user_cf=user_cf, train=train_dict, test=test_dict, N=N, K=K)

    return [recall_val,precision_val,coverage_val,popularity_val]

def evaluate_user_cf(user_cf, train_dict, test_dict, N, K):
    """

    :param user_cf:
    :param train_dict: {user:[item1, item2]}
    :param test_dict: {user: [item3]}
    :param N:the number of recommend items
    :param K:the number of most similar users
    :return:
    """
    print(evaluate(user_cf, train_dict, test_dict, N, K))




def main(train,test):
    user_cf, user_item_dict = train_user_cf(train)
    N = 30
    K = 80
    user_item_df = test.groupby("UserID")["ModelID"].apply(list).reset_index(name="ModelIDList")
    test_user_item_dict = dict(zip(user_item_df["UserID"], user_item_df["ModelIDList"]))

    item_cf, user_item_dict = train_item_cf(train)

    print("user_cf:",K)
    evaluate_user_cf(user_cf, user_item_dict, test_user_item_dict, N, K)

    print("item_cf:",K)
    evaluate_user_cf(item_cf, user_item_dict, test_user_item_dict, N, K)

main(train,test)