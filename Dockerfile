# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt


CMD python3 py_docs_bot.py
