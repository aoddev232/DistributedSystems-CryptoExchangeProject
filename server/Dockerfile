# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY server/requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy necessary files
COPY server /usr/src/app/server
COPY core /usr/src/app/core

ENV PYTHONPATH /usr/src/app/core

# Make port 12345 available to the world outside this container
EXPOSE 12345

# Run the application when the container launches
CMD ["python", "-u", "-m", "server.server"]