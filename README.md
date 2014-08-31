Bilor
=====

Experimental exception/logging server.

Summary
=======

The idea behind Bilor is using the full power of ElasticSearch to make logging
more accessible and searchable.

Features
========

Client
------

* Log arbitrary messages with optional extra data (such as request headers, user login, etc)
* Log exceptions from the except clause with optional extra data, as well as with the traceback information
* Be fault-tolerant: if central logger is busy or unavailable, don't raise another exception, but die silently or (optionally) fall back to another way of logging the error.


Server
------

* Collect error and log messages and display them from the web-interfaces. Having some time-based graphs.
* Keep it as simple as possible!
* Survive "error bursts"
* Grouping of messages


Why Bilor when there is Sentry and Logstash?
============================================

Bilor is very similar in many ways to Sentry and Raven when it comes to it's general idea but
tries to experiment with totally different ways of storing the data and with that keeping
it's core small, simple, extensible and reliable. Also, Bilor does not care about teams and groups and
specific user permissions yet.

Scaling ElasticSearch reliably is a known thing and there are many resources in that regard. Specifically
in a virtualized environment such as Amazon AWS.

Logstash would have worked too but it's a huge burden and lots of dependencies for simple
experiments. It'll pay out as a long-term-project eventually though and is always a great idea.

Though Logstash makes more sense once you're trying to centralize logging for all applications e.g
also nginx, PostgreSQL and other apps you're using to provide your service.

Generally, if you have a huge infrastructure consider those alternatives:

* Logstash, ElasticSearch, Kibana with message routing via RabbitMQ (Good tutorial: https://www.digitalocean.com/community/tutorials/how-to-use-logstash-and-kibana-to-centralize-and-visualize-logs-on-ubuntu-14-04)
* Sentry and Raven. They are quite simple, they work and have good active development.

Resources / Ideas
=================

* http://www.elasticsearch.org/blog/curator-tending-your-time-series-indices/
* http://www.elasticsearch.org/guide/en/elasticsearch/guide/current/retiring-data.html
