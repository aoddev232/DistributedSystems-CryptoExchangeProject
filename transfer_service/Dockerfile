# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY transfer_service/requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy necessary files
COPY transfer_service /usr/src/app/transfer_service
COPY core /usr/src/app/core

ENV PYTHONPATH /usr/src/app/core

# Make port 12345 available to the world outside this container
EXPOSE 8084

# Run the application when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:8084", "transfer_service.transfer_controller:app"]