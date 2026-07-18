# Access Log Summary Report

There is an Apache-style access log at `/app/access.log` in your working directory
(`/app`). Analyze the traffic it records and write a small JSON summary report.

Each log line looks like:

```
192.168.0.1 - - [16/Jun/2026:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 1024
```

The client IP is the first whitespace-separated field, and the requested path is the
second token inside the quoted request line (`"GET /index.html HTTP/1.1"` →
`/index.html`).

## Success criteria

1. Write a report to `/app/report.json` that is a single valid JSON object (parseable
   with `json.load`) containing the keys `total_requests`, `unique_ips`, and
   `top_path`.
2. `total_requests` is an integer equal to the number of non-empty lines in
   `/app/access.log`.
3. `unique_ips` is an integer equal to the number of distinct client IP addresses in
   the log.
4. `top_path` is a string equal to the requested path that appears most often in the
   log. If several paths tie for the most requests, any one of them is acceptable.

For example, a valid report has the shape:

```json
{"total_requests": 42, "unique_ips": 7, "top_path": "/index.html"}
```
