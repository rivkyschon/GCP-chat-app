# Use a base Python image
FROM python:latest-slim AS base

RUN update-ca-certificates && pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt --no-cache-dir

#VOLUME [ "/users.csv" ]

# Monitoring the health check
HEALTHCHECK --interval=10s --timeout=3s CMD curl --fail http://localhost:5000/health || exit 1

# Set the working directory in the container
WORKDIR /app

# Expose the port on which the Flask app will run
EXPOSE 5000

FROM python:latest-slim AS env

# Set the environment variable for room files path
ENV ROOM_FILES_PATH "rooms/"
ENV USERS_PATH "users.csv"
ENV FLASK_ENV development

# copy all the directory into the container (except of the .dockerignor files)
COPY . . 

FROM python:latest-slim AS final

# Run the Flask app
CMD ["python", "./chatApp.py"]
