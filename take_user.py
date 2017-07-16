#!/usr/bin/python
#-*- coding:utf-8 -*-
############################
#File Name: take_user.py
#Author: yuxuan
#Created Time: 2017-03-10 10:32:57
############################
from draw_data import draw_data
import logging
import numpy as np
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

classify_dict = np.load("classify.dict.npz")['arr_0'][()]

def user_pro():
    userlike = np.load("userlike.dict.npz")['arr_0'][()]
    db = draw_data()
    for titleid in classify_dict.keys():
        k += 1
        comment = db.title_comment_time(titleid, )
        comment = db.title_comment_aggregate(titleid)
        tempc = 0
        user_num = 0
        for ci in comment:
            tempc += 1
            if ci["_id"] in userLike:
                user_num += 1

def user_like(num):
    userLike = dict()
    db = draw_data()
    user = db.return_user(num)
    titleUserNum = dict() 
    for ti in user:
        userLike[ti["_id"]] = [0 for i in range(15)]
        titleUserNum[ti["_id"]] = dict()
        titleUserNum[ti["_id"]]["count"] = 0
    print len(userLike)
    topic_set = dict()
    user_all_num = 2551366
    titlenum = len(classify_dict)
    k=0
    for titleid in classify_dict.keys():
        k += 1
        printUserNum = 0
        comment = db.title_comment_aggregate(titleid)
        tempc = 0
        for ci in comment:
            tempc += 1
            if ci["_id"] in userLike:
                printUserNum += 1
                titleUserNum[ci["_id"]][titleid] = ci["count"]
                titleUserNum[ci["_id"]]["count"] += ci["count"]
        topic_num = np.argmax(classify_dict[titleid])
        topic_set[titleid] = [topic_num, tempc]
        logging.info("process "+str(k)+"/"+str(titlenum)+":"+titleid+" "+str(topic_num)+" "+str(printUserNum)+"/"+str(tempc))
    np.savez("topic_set.dict", topic_set)
    np.savez("titleUserNum.dict", titleUserNum)
    
    topic_set = np.load("topic_set.dict.npz")['arr_0'][()]
    titleUserNum = np.load("titleUserNum.dict.npz")['arr_0'][()]
    for uid in userLike:
        for titleid in classify_dict.keys():
            if titleid in titleUserNum[uid]:
                tf = 1.0*titleUserNum[uid][titleid]/titleUserNum[uid]["count"]
                idf = np.log2(1.0*user_all_num/topic_set[titleid][1])
                userLike[uid][topic_set[titleid][0]] += tf*idf
        npsum = np.sum(userLike[uid])
        for i in range(15):
            userLike[uid][i] /= npsum
    np.savez("userlike.dict", userLike)
    return userLike

def calid_user():
    titleUserNum = np.load("titleUserNum.dict.npz")['arr_0'][()]
    titleContianUser = dict()
    for uid in titleUserNum.keys():
        for tid in titleUserNum[uid].keys():
            if tid in titleContianUser:
                titleContianUser[tid].append(uid)
            else:
                titleContianUser[tid] = [uid]
    np.savez("titleContianUser.dict", titleContianUser)

def test():
    userlike = np.load("userlike.dict.npz")['arr_0'][()]
    for uid in userlike.keys():
        userlike[uid] = np.array(userlike[uid]).reshape(1, 15)
    np.savez("userlike.dict", userlike)

if __name__ == "__main__":
   #user_like(300)
   #test()
   calid_user()
