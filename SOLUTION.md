# Lab 6 - REST vs gRPC Performance Results

Average time per operation in milliseconds (ms). Local and same-zone tests used 1,000 requests per method; different-region tests used 100 requests per method. PING values are average round-trip times from 10 packets.

| Method | Local (ms) | Same-Zone (ms) | Different Region (ms) |
|---|---:|---:|---:|
| REST add | 2.6033 | 3.6608 | 321.8400 |
| gRPC add | 0.8758 | 1.2409 | 142.9032 |
| REST rawimg | 5.1251 | 8.2642 | 1304.0305 |
| gRPC rawimg | 12.5590 | 14.5884 | 202.4548 |
| REST dotproduct | 3.0044 | 4.4942 | 321.5585 |
| gRPC dotproduct | 0.8477 | 1.3739 | 143.2090 |
| REST jsonimg | 28.4960 | 32.3666 | 1411.8304 |
| gRPC jsonimg | 19.3988 | 20.6445 | 216.3527 |
| PING | 0.0560 | 0.4540 | 159.8740 |

## Observations

- **gRPC performed better for small operations** like `add` and `dotproduct` across all three environments due to lower communication overhead.
- **REST was faster for `rawimg`** in localhost and same-zone testing, showing that gRPC is not always faster for every operation.
- **`jsonimg` was generally slower than `rawimg`** because Base64 encoding increases data size and adds encoding/decoding overhead.
- **Network latency increased significantly with distance.** Average ping increased from 0.056 ms (localhost) to 0.454 ms (same-zone) and 159.874 ms (different region).
- **TCP connection handling affected performance.** Our REST client creates a new TCP connection for each request, while gRPC reuses a single connection through its channel, reducing connection setup overhead.
- **gRPC performed significantly better across regions**, especially for image transfers, because connection reuse avoids repeated TCP connection setup over long distances.
