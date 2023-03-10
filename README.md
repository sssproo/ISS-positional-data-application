# ISS positional data application

This project aims at providing an web application for accessing ISS  positional and velocity data from [ISS Trajectory Data | NASA](https://spotthestation.nasa.gov/trajectory_data.cfm).


# Files description

|file|usage  |
|--|--|
| Dockerfile|Build docker  |
|iss_tracker.py|Main application code of Flask app|
|docker-compose.yaml|docker-compose|
|requirements.txt|dependencies for installing this app|


# Pull existing image and use from DockerHub

Command:

    docker image pull ssspro/iss_tracker:hw05
 
 Run Flask from docker:
 

    docker run ssspro/iss_tracker:hw05

# Build a new image from Dockerfile
Command:

    docker build -t ssspro/iss_tracker:hw05 .

# Give example API query commands and expected outputs

Example:
We query from url:
127.0.0.1:5000/epochs/?limit=2&offset=0

Return list data:
["2023-048T12:00:00.000Z","2023-048T12:04:00.000Z"]
