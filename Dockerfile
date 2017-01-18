#Create python3 image from python image on dockerhub
FROM python:3-onbuild

# Create a directory where our app will be placed
RUN mkdir -p /dock/service

# Change directory so that our commands run inside this new directory
WORKDIR /dock/service

# Copy dependency definitions
COPY requirements.txt /dock/service

# Install dependecies
RUN pip3 install -r requirements.txt

# Get all the code needed to run the app
COPY . /dock/service

# WORKDIR /airbnbscrape/airbnbscrape

# Expose the port the app runs in
EXPOSE 5000



CMD ["python3", "start.py"]



# # Export the flask server
# CMD ["export", "FLASK_APP=airbnbscrape/airbnbscrape/start.py"]

# # Run flask server
# CMD ["flask", "run"]