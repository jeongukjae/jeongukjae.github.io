---
layout: post
title: "Tips for Fluet logger"
tags:
    - Operation
---

[Fluent-bit](https://fluentbit.io) is widely-used for logging and monitoring components.
It can gather events or logs from many different input sources, filter them, and convey them to proper output destinations.
At the same time, it is very lightweight and scalable.

To send events programmatically in application codes to fluent bit, I think using fluent logger is a good candidate.
It supports various languages such as Go, Python, and Node.js, and has simple interfaces.
So it is very easy to aggregate application events and store them in blob storage like AWS S3 using Fluent logger and Fluent bit.

But in production usage, some configurations are needed to use it properly.
So in this post, I will show you some situations and solutions.

## Situation #1: Can't load-balance the events

In a cloud environment, we can use multiple fluent bit pods pointed by some DNS address to aggregate events derived from multiple application services with fluent-logger.
Fluent logger uses [Forward protocol](https://github.com/fluent/fluentd/wiki/Forward-Protocol-Specification-v1) to send events.
Each application pod will connect to fluent bit server with TCP socket, and it will last until the application or fluent bit pod is terminated.
So we cannot load-balance logging traffic between fluent bit pods.

### Solution

If you are using [Async mode](https://github.com/fluent/fluent-logger-golang#async) for logger, you need to set [AsyncReconnectInterval](https://github.com/fluent/fluent-logger-golang#asyncreconnectinterval) also.
It will re-establish the connection to fluent bit server after the interval.

## Situation #2: Losing events when resetting connection

Sometimes we have to reconnect to fluent bit for unexpected reasons such as network issues.
In that situation, I experienced events are losed for a while.
Fluent logger didn't retry, and no error logs are printed, so it was hard to confirm.

### Solution

You have to set [RequestACK](https://github.com/fluent/fluent-logger-golang#requestack) option.
Fluent logger doesn't request acknowledgment by default, so it sends events without checking the connection.
If RequestACK is set, it will check the acknowledgment after sending each event.
