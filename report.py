#! /usr/bin/env python3

import psycopg2

# database name
DB_NAME = "news"


# function to run the query, and fetch the results
def runQueryFromDB(db_name, query):

    try:
        # connect to the database
        db = psycopg2.connect(database=db_name)
        # cursor to run the query
        cur = db.cursor()
        cur.execute(query)
        # fetch results
        results = cur.fetchall()
        # return query results
        return results
    except:
        print("Unable to run the query!")
    finally:
        if db:
            # close db
            db.close()


# function to generate the report for the most popular articles
def mostPopularArticles():

    # query for report 1: what are the most popular three articles?
    query = ("select articles.title, count(log.id) as TimesViewed "
             "from log, articles "
             "where substring(log.path, 10) = articles.slug "
             "group by articles.title "
             "order by TimesViewed desc "
             "limit 3;")

    results = runQueryFromDB(DB_NAME, query)

    if(results is not None):
        print("The top three viewed articles are: \n")
        for result in results:
            print("\"" + result[0] + "\"" + " -- " + str(result[1]) + " Views"
                  )

    print("\n")


# function to generate the report for the most popular authors
def mostPopularAuthors():

    # query for report 2: who are the most popular authors of all time?
    query = ("select authors.name, count(log.id) as TimesViewed "
             "from log, authors, articles "
             "where substring(log.path, 10) = articles.slug "
             "and authors.id = articles.author "
             "group by authors.name "
             "order by TimesViewed desc "
             "limit 4;")

    results = runQueryFromDB(DB_NAME, query)

    if(results is not None):
        print("The most popular authors of all times are: \n")
        for result in results:
            print(result[0] + " -- " + str(result[1]) + " Views")

    print("\n")


# function to generate the error report
def errorReport():

    # query for report 3: On which days did more than 1% of requests lead to
    # errors?
    query = ("select errors.what_day, cast(errors.error_count as decimal) / "
             "totals.total_count as error_percent "
             "from (select count(log.id) as error_count, "
             "log.time::date as what_day "
             "from log "
             "where log.status != '200 OK' "
             "group by log.time::date) errors, "
             "(select count(log.id) as total_count, "
             "log.time::date as what_day "
             "from log "
             "group by log.time::date) totals "
             "where errors.what_day = totals.what_day "
             "and cast(errors.error_count as decimal) / "
             "totals.total_count > 0.01; ")

    results = runQueryFromDB(DB_NAME, query)

    if(results is not None):
        print("The days with more than 1% of requests lead to errors: \n")
        for result in results:
            print(str(result[0]) + " -- " + "{0:.2f}%".format(result[1] * 100))

    print("\n")


# run the queries and generate the reports
if __name__ == "__main__":
    mostPopularArticles()
    mostPopularAuthors()
    errorReport()
