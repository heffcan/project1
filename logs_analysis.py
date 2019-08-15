#!/usr/bin/env python3

import psycopg2
from psycopg2 import errors


# 1. most popular articles
def get_top_three_articles(db):
	c = db.cursor()
	c.execute("SELECT title, count(log.path) as views from articles, log\
  			   WHERE split_part(log.path, '/', '3') = articles.slug\
  			   group by title order by views desc limit 3;")
	return c.fetchall()


# 2. Who are the authors of the top viewed
def get_top_authors(db):
	c = db.cursor()
	c.execute("SELECT name, count(log.path) AS views \
			     FROM authors, log, articles \
				 WHERE split_part(log.path, '/', '3') = articles.slug\
				 AND articles.author = authors.id\
				 GROUP BY name\
				 ORDER BY views DESC;")
	return c.fetchall()


# 3. On which days did more than 1% of requests lead to errors
def get_days_of_more_than_1percent_errors(db):
	c = db.cursor()
	b = db.cursor()
	b.execute("select date_part('day', time) as day, \
				count(*) as num_of_requests\
			    from log\
			    group by day\
			    order by day;")
	"""
	I am summing up the total requests of all time, not per day.
	Correct this. I need to aggregate the number of request per 
	the same day and make that my calculations
	"""
	c.execute("select date_part('day', time) as day, \
				count(*) as num_of_errors\
				   from log\
				   where status != '200 OK'\
				   group by day\
			       order by day;;")
	daily_requests = b.fetchall()
	daily_failures = c.fetchall()
	# print(daily_requests)
	# print(daily_failures)
	over_percent_failed_requests = []

	for day0, total__fails in daily_failures:
		for day1, total_requests in daily_requests:
			# print( day1, (float(total__fails)/total_requests)*100)
			error_rate = (total__fails/float(total_requests))*100

			if error_rate > 1:
				# print("Day: {} - fail_rate: {:.2f}%".format(day0, error_rate)
				# 	   )
				over_percent_failed_requests.append((day0, error_rate))
	return sorted(set(over_percent_failed_requests))

if __name__ == '__main__':
	DB_NAME = "news"
	with psycopg2.connect(database=DB_NAME) as db:
		print("Top 3 Articles:")
		for aricles, num_views in get_top_three_articles(db):
			print("\t\"" + aricles + " -- " + str(num_views) + " views")
		print("Top Authors:")
		for author, num_views in get_top_authors(db):
			print("\t" + author + " -- " + str(num_views) + " views")
		print("Error Rates:")
		for day, error_rate in get_days_of_more_than_1percent_errors(db):
			print("Day: {} - fail_rate: {:.2f}%".format(day, error_rate)
					   )
	
