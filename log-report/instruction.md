# Access Log Summary Report

There is an Apache-style access log at `/app/access.log` in your working directory
(`/app`). Analyze the traffic it records and write a small JSON summary report.

Each log line looks like:

```
192.168.0.1 - - [16/Jun/2026:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 1024
```

The client IP is the first whitespace-separated field, and the requested path is the
second token inside the quoted request (`"GET /index.html HTTP/1.1"` → `/index.html`).

## Success criteria

1. Write your report to the file `/app/report.json`.
2. The file must contain a single JSON object with exactly these three keys:
   - `total_requests` (integer): the total number of non-empty log lines.
   - `unique_ips` (integer): the count of distinct client IP addresses.
   - `top_path` (string): the requested path that appears most often. If there is a
     tie, any one of the most frequent paths is acceptable.
3. The values must be computed from the contents of `/app/access.log` and must be
   correct for that log.
4. The JSON must be valid and parseable (e.g. loadable with `json.load`).

For example, a valid report has the shape:

```json
{"total_requests": 42, "unique_ips": 7, "top_path": "/index.html"}
```
