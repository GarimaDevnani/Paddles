import sqlite3


def getNoOfBikesRentedBetween(start_date, end_date):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()

    # Note that the date is in YYYY-MM-DD format
    query = f'''
        SELECT count(*) AS bikes, strftime('%Y-%m-%d', datestart) AS date 
        FROM journeylog WHERE datestart BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY strftime('%Y-%m-%d', datestart)
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return result


def getNoOfBikesRentedBetweenWith(start_date, end_date, location):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()

    # Note that the date is in YYYY-MM-DD format
    query = f'''
        SELECT count(*) AS bikes, strftime('%Y-%m-%d', datestart) AS date 
        FROM journeylog WHERE rentfrom = '{location}' AND datestart BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY strftime('%Y-%m-%d', datestart)
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return result


def getNoOfBikesReportedBetween(start_date, end_date):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()

    # Note that the date is in YYYY-MM-DD format
    query = f'''
        SELECT count(*) AS bikes, strftime('%Y-%m-%d', reporteddate) AS date 
        FROM repairlog WHERE reporteddate BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY strftime('%Y-%m-%d', reporteddate)
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return result


def getNoOfBikesReportedBetweenWith(start_date, end_date, location):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()

    # Note that the date is in YYYY-MM-DD format
    query = f'''
        SELECT count(*) AS bikes, strftime('%Y-%m-%d', reporteddate) AS date 
        FROM repairlog WHERE reportlocation = '{location}' AND reporteddate BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY strftime('%Y-%m-%d', reporteddate)
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return result


def getNoOfBikesFixedBetween(start_date, end_date):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()

    # Note that the date is in YYYY-MM-DD format
    query = f'''
        SELECT count(*) AS bikes, strftime('%Y-%m-%d', fixdate) AS date 
        FROM repairlog WHERE fixdate BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY strftime('%Y-%m-%d', fixdate)
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return result


def getNoOfBikesFixedBetweenWith(start_date, end_date, location):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()

    # Note that the date is in YYYY-MM-DD format
    query = f'''
        SELECT count(*) AS bikes, strftime('%Y-%m-%d', fixdate) AS date 
        FROM repairlog WHERE reportlocation = '{location}' AND fixdate BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY strftime('%Y-%m-%d', fixdate)
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return result


def getMostToLeastUsedLocation(start_date, end_date):
    with sqlite3.connect('Database/company.db') as db:
        cursor = db.cursor()

    query = f'''
        SELECT count(*) AS bikes, rentfrom AS location 
        FROM journeylog WHERE datestart BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY rentfrom ORDER BY count(*) DESC
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return result
