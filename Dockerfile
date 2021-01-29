FROM python:latest

# Add scripts to the path of the running container
# Then can acces to scripts
ENV PATH="/scripts:${PATH}"

# Install depencies 
RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir /app

# Copy escape_game inside docker container
COPY ./app /app
WORKDIR /app


# STATIC files inside docker image 
# -p create subdirectories 
RUN mkdir -p /vol/static


