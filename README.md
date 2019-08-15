This project assumes that the user has the appropriate 'news' database.
Requiremnts besides the database is pyscopg2.

The tables of the news.db are articles, authors, and log.

Running "python logs_analysis.py" in the terminal will yield the output per
the three questions:
  1) What are the most popular three articles of all time?
  2) Who are the most popular article authors of all time?
  3) On which days did more than 1% of requests lead to errors?
