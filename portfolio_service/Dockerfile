# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY portfolio_service/requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy necessary files
COPY portfolio_service /usr/src/app/portfolio_service
COPY core /usr/src/app/core

ENV PYTHONPATH /usr/src/app/core

# Make port 8081 available to the world outside this container
EXPOSE 8081

# Run the application when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:8081", "portfolio_service.portfolio_controller:app"]