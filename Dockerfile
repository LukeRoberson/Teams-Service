# Use the custom base image
FROM lukerobertson19/base-os:latest

# OCI labels for the image
LABEL org.opencontainers.image.title="AI Assistant Teams Service"
LABEL org.opencontainers.image.description="Interaction with Microsoft's Graph API to send messages to Teams users and groups."
LABEL org.opencontainers.image.base.name="lukerobertson19/base-os:latest"
LABEL org.opencontainers.image.source="https://github.com/LukeRoberson/Teams-Service"
LABEL org.opencontainers.image.version="1.0.0"

# The health check URL for the service
LABEL net.networkdirection.healthz="http://localhost:5100/api/health"

# The name of the service, as it should appear in the compose file
LABEL net.networkdirection.service.name="teams"

# Copy the rest of the application code
COPY . .
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Start the application using uWSGI
CMD ["uwsgi", "--ini", "uwsgi.ini"]
