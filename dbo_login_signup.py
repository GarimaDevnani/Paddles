import sqlite3
import time


def getUser(email):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()
    sql_select = f'''SELECT username,permission,balance,userstatus,userid FROM users WHERE email = '{email}' '''
    cursor.execute(sql_select)
    result = cursor.fetchall()
    db.close()
    return result


def authenticateUser(email, password):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()
    sql_authenticateUser = f'''SELECT password FROM users Where email='{email}' '''
    try:
        cursor.execute(sql_authenticateUser)
        resultL = cursor.fetchall()
    except:
        result = -1
        db.close()
        return result
    else:
        db.close()
        if len(resultL) == 0:
            result = 0
            return result
        if resultL[0][0] == password:
            result = 1
        else:
            result = 0
        return result


def checkUserStatus(email):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()
    sql_authenticateUser = f'''SELECT userstatus FROM users Where email='{email}' '''
    try:
        cursor.execute(sql_authenticateUser)
        result = cursor.fetchall()
    except:
        result = -1
        db.close()
        return result
    else:
        db.close()
        return result


def insertTousers(username, email, password):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()
    try:
        sql_selectid = f'''SELECT userid FROM users'''
        cursor.execute(sql_selectid)
        listId = cursor.fetchall()
        userid = listId[-1][0] + 1
        sql_insert = f'''INSERT INTO users(userid,username,email,password,permission,balance,userstatus)VALUES({userid},'{username}','{email}','{password}','CUST',0,0)'''
        cursor.execute(sql_insert)
        db.commit()
        result = 1
    except:
        result = 0
        return result
    else:
        db.close()
        return result


def getLocationBikes(location):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()
    sql_select = f'''SELECT bikeid,bikestate FROM bikes WHERE bikelocation = '{location}' '''
    cursor.execute(sql_select)
    result = cursor.fetchall()
    db.close()
    return result


def insertTologs(userid, bikeid, rentfrom):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()
    sql_selectid = f'''SELECT logid FROM journeylog'''
    cursor.execute(sql_selectid)
    listId = cursor.fetchall()
    if listId == []:
        logid = 1
    else:
        logid = listId[-1][0] + 1

    datestart = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    sql_insert = f'''INSERT INTO journeylog(logid,userid,bikeid,rentfrom,datestart)VALUES({logid},{userid},{bikeid},'{rentfrom}','{datestart}')'''
    cursor.execute(sql_insert)
    db.commit()
    db.close()


def insertTologsbyDay(userid, bikeid, rentfrom):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()
    sql_selectid = f'''SELECT logid FROM journeylog'''
    cursor.execute(sql_selectid)
    listId = cursor.fetchall()
    if listId == []:
        logid = 1
    else:
        logid = listId[-1][0] + 1

    datestart = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    sql_insert = f'''INSERT INTO journeylog(logid,userid,bikeid,rentfrom,datestart,price)VALUES({logid},{userid},{bikeid},'{rentfrom}','{datestart}',58)'''
    cursor.execute(sql_insert)
    db.commit()
    db.close()


def getLogid(userid):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()
    sql_select = f'''SELECT logid FROM journeylog WHERE userid = '{userid}' '''
    cursor.execute(sql_select)
    result = cursor.fetchall()
    db.close()
    return result


def updateUserstatus(userid, logid):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()
    sql_update = f'''UPDATE users SET userstatus = {logid} WHERE userid = {userid}'''
    cursor.execute(sql_update)
    db.commit()
    db.close()


def updateBikeLocation(bikeid):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()
    sql_update = f'''UPDATE bikes SET bikelocation = 'TRANSIT' WHERE bikeid = {bikeid}'''
    cursor.execute(sql_update)
    db.commit()
    db.close()


def updateBikestate(bikeid):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()
    sql_update = f'''UPDATE bikes SET bikestate = 'DEFECTIVE' WHERE bikeid = {bikeid}'''
    cursor.execute(sql_update)
    db.commit()
    db.close()


def getLoginfo(logid):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()
    sql_select = f'''SELECT userid,bikeid,datestart,dateend,rentfrom,returnto,price FROM journeylog WHERE logid = {logid} '''
    cursor.execute(sql_select)
    result = cursor.fetchall()
    db.close()
    return result


def updateBikelocation_withbikelocation(bikeid, bikelocation):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()
    sql_update = f'''UPDATE bikes SET bikelocation = '{bikelocation}' WHERE bikeid = {bikeid}'''
    cursor.execute(sql_update)
    db.commit()
    db.close()


def updateLogdateend_returnto(logid, returnto):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()

    dateend = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    sql_update = f'''UPDATE journeylog SET dateend = '{dateend}' WHERE logid = {logid}'''
    cursor.execute(sql_update)
    db.commit()

    sql_update = f'''UPDATE journeylog SET returnto = '{returnto}' WHERE logid = {logid}'''
    cursor.execute(sql_update)
    db.commit()
    db.close()


def emptyUserstatus(userid):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()

    sql_update = f'''UPDATE users SET userstatus = 0 WHERE userid = {userid}'''
    cursor.execute(sql_update)
    db.commit()
    db.close()


def updateUserbalance(userid, balance):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()

    sql_update = f'''UPDATE users SET balance = {balance} WHERE userid = {userid}'''
    cursor.execute(sql_update)
    db.commit()
    db.close()


def getRentHistory(userid):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()
    sql_select = f'''SELECT datestart,dateend,rentfrom,returnto,price FROM journeylog WHERE userid = {userid} '''
    cursor.execute(sql_select)
    result = cursor.fetchall()
    db.close()
    return result


def updateLogprice(logid, price):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()

    sql_update = f'''UPDATE journeylog SET price = {price} WHERE logid = {logid}'''
    cursor.execute(sql_update)
    db.commit()
    db.close()


def reportError(logid, userid, bikeid, location):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()

    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    sql_insert = f'''INSERT INTO repairlog(logid,customerid,bikeid,reporteddate,reportlocation)VALUES({logid},{userid},{bikeid},'{now}','{location}')'''
    cursor.execute(sql_insert)
    db.commit()
    db.close()
