# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY stake_service/requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy necessary files
COPY stake_service /usr/src/app/stake_service
COPY core /usr/src/app/core

ENV PYTHONPATH /usr/src/app/core

# Make port 8082 available to the world outside this container
EXPOSE 8082

# Run the application when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:8082", "stake_service.stake_controller:app"]