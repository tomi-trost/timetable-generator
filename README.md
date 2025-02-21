# Running 
## Building the docker image
´´´
docker build -f dev.dockerfile -t timetable-generator .
´´´
## Running the docker image
´´´
docker run -d --name timetable-generator -p 8081:80 timetable-generator
´´´