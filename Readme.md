# Webcron
Webcron is a simple Python script that makes web requests at regular intervals.


## Config file (jobs.json)
The configuration file is a json formated list of jobs. A job is defined by its name, the url to be requested and the request interval in seconds.

Example:
```
[
    {
        "name": "Google",
        "url": "http://google.com",
        "interval": 5
    },
    {
        "name": "Google",
        "url": "https://google.com",
        "interval": 10
    }
]
```

## Volumes
* Config path: The path to configuration folder

```
-v /path/to/local/storage:/usr/src/app/config
```

## Start container
```
docker run -d --name=webcron -v -v /path/to/local/storage:/usr/src/app/config:r topdockercat/webcron:latest
```
