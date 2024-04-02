# The Conduct Application


## STEPS:

clone the repo:

    git clone https://github.com/naveen-ravi2810/Conduct_Backend.git

Add .env just copy it from .env.example <br/>
Need to configure some details from .env file

    cp .env.example .env

Build the image

    docker build  -t conduct .

Run the Image

    docker run -p8000:8000 <image-id (or) conduct>

You can see it in localhost:8000

and read the docs at

<a href='http://localhost:8000/docs'>http://localhost:8000/docs</a>


User Complete



### Errors and Learnings
`errors that i rectified`

1. Writing pytest
    1. Use case of scope
    2. How to yield client

