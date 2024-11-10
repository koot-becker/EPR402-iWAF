# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /waf

# Copy the current directory contents into the container at /app
COPY . /waf

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Define environment variable
ENV NAME=WebAppFirewall

# Define entrypoint
ENTRYPOINT [ "python3", "web_app_firewall_interface.py" ]

# Run app.py when the container launches
CMD [ ]