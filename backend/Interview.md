## what is encapsulation inheritance polymorhism Dependency Inversion

“I separated abstractions, vendor adapters, and orchestration so that adding a new device type or brand never impacts the API or existing logic.”

### In Device why not add functionality methods ? because this is to see how i want to show stuff to the front end , not all devices share the same functionality

## Used a Dictionary in device.py

## Problem: Dynamic Device Availability

In a home IoT system, devices can go offline or be added at any time:

- A bulb may be unplugged or powered off → backend thinks it’s still available
- New devices may be added after startup → backend doesn’t know about them
- Commands sent to offline devices may fail (KasaException)

---

## Solutions Considered

### 1. Per-command online check (`is_online()`)

- Before sending any command, ping the device  
  **Pros:** Accurate, prevents sending commands to offline devices  
  **Cons:** Adds network overhead for every command

### 2. Periodic background discovery

- Backend scans network at intervals to refresh device list  
  **Pros:** Automatically keeps list up-to-date  
  **Cons:** Adds complexity, still can fail between scans

### 3. Manual refresh endpoint

- Frontend or user triggers `/devices/refresh` to update device list  
  **Pros:** Simple, low overhead, works well in home setups  
  **Cons:** Relies on user to refresh after changes

### 4. Safe command wrapper / try-catch

- Wrap all hardware commands in `try/except` to catch offline errors  
  **Pros:** Backend never crashes, provides meaningful HTTP errors  
  **Cons:** Doesn’t proactively know offline devices

What is Uvicorn : python packages for asynchronous hhtp requests used for firing connection calls, n ASGI server — it runs your FastAPI app and handles incoming HTTP/WebSocket connections.

Regarding Github action pipeline

Github actions are like something you can configure on pull or push requests for example to run some checks

flake & ruff for linting python libraries that check unused variables etc

pipreqs generates the dependencies of a project and generates the requirmenets file that holds all dependencies
requirements-dev.txt is used for the pipleine?

.github/worklflow is a hidden directory that runs the github action that you configured via the yaml file

So the Dockerfile just contains instructions like:

Start from this base Python environment
Copy my code in
Install my dependencies
Run this command to start the app

Dockerfile containes the recipe and instructions for building that space

Docker Image : the blueprint of docker containers that is build from the dockerfile

Docker Container: container instances from that docker image

p in the workdir were the starting point of the application is, cm then runs the comands on a specificport and network ?
Almost exactly right. Small corrections:

FROM — picks the base image (not just the language). python:3.11-slim is a pre-built Linux OS + Python 3.11 already installed. slim just means a stripped-down smaller version.

WORKDIR — correct, creates and sets the working directory inside the container. Any commands after it run from that path.

COPY . . — correct. First . is your local machine (the repo), second . is the current WORKDIR inside the container.

RUN pip install -r requirements.txt — correct. RUN executes commands at build time (when you docker build), so the dependencies are baked into the image.

Second WORKDIR — correct, it just shifts the working directory so Python resolves imports from the right place.

CMD — slight correction: CMD runs at container start time (when you docker run), not build time. It's the entry point command. The --host 0.0.0.0 part is important — without it uvicorn only listens inside the container and you can't reach it from your machine. --port 8000 sets the port inside the container, and -p 8000:8000 in your docker run maps it to your machine.

GitHub Actions

Lives in .github/workflows/ — GitHub automatically detects it
Triggered by events like push and pull_request
Runs on a fresh GitHub cloud machine every time, not your local machine or Raspberry Pi
Each job has steps executed in order
uses = pre-built action, run = shell command you write
actions/checkout@v3 pulls your code onto the runner machine
Without it the runner has no idea what your project looks like

Linting

Ruff reads your code without running it and flags problems
Goes in requirements-dev.txt not requirements.txt — it's a dev tool, not a runtime dependency
ruff check . checks everything in the current directory
A failing lint step returns exit code 1 which fails the pipeline

Branch Protection

Without it, CI is a warning not a gate
With it, a red pipeline physically blocks merging to main
Real teams never push directly to main — they use feature branches and PRs

Docker

Dockerfile = recipe
docker build = follows the recipe and produces an image
docker run = starts a container from that image
-p host:container maps ports so the outside world can reach the app
COPY . . — first dot is your machine, second dot is the WORKDIR inside container
RUN executes during build, CMD executes when container starts
Adding Docker build to CI catches deployability problems ruff can't

❓ Self-Test Questions
Try answering these out loud as if you're in the interview:

What is a CI pipeline and why does a team need one?

a CI pipeline automates checks on every push/PR so broken code is caught before it merges, not after. "Doesn't break" is vague — say "catches broken tests, lint errors, or failed builds automatically.

What's the difference between requirements.txt and requirements-dev.txt?

requirements= what project needs to run in productionm
requirements-dev = tools only needed in development/CI

GitHub spins up a fresh machine for every pipeline run — what's the very first thing it needs to do and why?

- checkout the code (actions/checkout@v3)

What's the difference between uses and run in a GitHub Actions step?

uses in Github ised used for a build in action ,run is in order to run specific commands

Your pipeline is green but a teammate can still merge broken code to main. Why, and how do you fix it?

branch protection isnt enabled.

What does -p 8000:8000 mean and what happens if you forget it? it connects the port of your laptop to the port of the docker container , if you dont put it then there is no way to access the container
Your app works locally but the Docker build fails on CI. What are two possible reasons?
(1) requirements file path is wrong, (2) a file referenced in the Dockerfile doesn't exist in the repo
the requirements file is missing or in a wrong place

Why is adding a Docker build step to CI valuable beyond just linting?
Because you make sure nothing breaks during deployment and that universally on all mashines this wont affect it
