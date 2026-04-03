# EduTracker Solutions - Reflection

This document contains theoretical approaches and architectural answers to some core backend challenges at EduTracker.

## 1. Real-Time Notifications (e.g., Enrollment events)

### Approach
To add real-time notifications when a student enrolls in a course, the standard Request-Response cycle of HTTP is insufficient. I would introduce **WebSockets** using **Django Channels**.

### Implementation Steps
1. **Django Channels & Redis**: Install `channels` and setup a message broker (like Redis via `channels_redis`) to handle communication between decoupled worker processes.
2. **Consumers**: Create a WebSocket `Consumer` (like a DRF View but for websockets) that clients (mobile app) can connect to upon login. This essentially subscribes them to a "personal notification group".
3. **Triggering the Event**: Override the `perform_create` or `save` method in the `StudentViewSet` (or the underlying Enrollment model if it was explicit). When a course is successfully added, send a message to the Redis channel group assigned to that student or the course instructor.
4. **Client-side**: The mobile app listens on the open WebSocket connection and instantly displays a toast or in-app notification when the event payload is received.

---

## 2. Large Video Course Uploads with File Size Limits

### Approach
Handling large video files directly through synchronous Django views blocks workers and consumes immense memory. We need to offload the heavy lifting and enforce constraints at multiple levels.

### Implementation Steps
1. **Web Server Limits**: Enforce the absolute maximum upload size at the reverse proxy layer (e.g., `client_max_body_size 500M;` in NGINX) to reject massive payloads before they ever hit the Python application.
2. **Django Level Validators**: Use DRF `FileField` or `validators` on the model to strictly check the file size (e.g., raise `ValidationError` if `file.size > LIMIT`). Also, adjust `FILE_UPLOAD_MAX_MEMORY_SIZE` so Django streams large files to disk rather than keeping them in memory.
3. **Cloud Storage (Best Practice)**: Instead of storing videos on the local server block, use **AWS S3** or **Google Cloud Storage** via `django-storages`.
4. **Direct / Pre-signed Uploads (Optimal)**: For massive videos, generate an S3 pre-signed URL from a backend endpoint. The mobile app uploads the video *directly* to S3 using this URL, completely bypassing the Django server, thus saving bandwidth and compute. Once uploaded, a webhook/callback updates the Django database with the video's URL.

---

## 3. Handling Rate-Limiting for High Traffic

### Approach
When dealing with heavy traffic from diverse mobile clients, the API must be protected from accidental DDoS attacks (e.g., retry-loops in client code) or malicious scraping.

### Implementation Steps
1. **DRF Throttling**: Utilize Django REST Framework's built-in throttling mechanics.
   - Configure `AnonRateThrottle` for unauthenticated endpoints (restricting by IP).
   - Configure `UserRateThrottle` for authenticated endpoints (restricting by Token/User ID).
   - Set limits like `"user": "100/min"` and `"anon": "20/min"` in `settings.py`.
2. **Caching Backend**: For the DRF throttles to operate efficiently across multiple scalable server instances, back Django's cache with **Redis** (or Memcached). This provides atomic and high-speed token bucket counting.
3. **Infrastructure Level Limiting**: For absolute protection, configure rate-limiting at the Edge/API Gateway or Reverse Proxy level. Services like **Cloudflare Rate Limiting**, **AWS API Gateway**, or **NGINX `limit_req`** can drop excessive requests before they ever consume backend resources.
