#Simple HTTP Server

This implements HTTP protocol over TCP sockets and is written in Python3

It can parse URL's and request body(JSON only).

Currently it serves only JSON responses, however it can be configured to serve files and other things too.

A demo is available on ```http://13.233.132.214:8000```

Use the following postman collection to explore the sample requests ```https://www.getpostman.com/collections/3caf307cc94cdee54293```

## Setting Up

- Clone the repo ```https://bitbucket.org/vozille/simplehttpserver``` or unzip the zip file provided
- cd into the ```simplehttpserver``` folder
- Run ```docker-compose up --build```
- The application will be live on ```http://localhost:8000```

## Running Tests
The tests are located in ```\HTTPServerTests\WebServerTests.py```

To run the tests, run ```python -m WebServerTests.py```

## Further Improvements
- The server only serves JSON responses. This can be expanded
- The maximum number of concurrent connections is 5, for demonstration purposes. This number is much higher in actual Web Servers.
