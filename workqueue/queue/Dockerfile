# Build upon this image "alpine" is a lightweight distro
FROM python:3.7-alpine

# Copy in requirements.txt first (for caching purposes)
COPY requirements.txt /app/requirements.txt

# Install all the requirements
RUN pip install -r /app/requirements.txt
RUN pip install ffmpeg-python

# Copy everthing from . to /app inside the 'box'
COPY . /app
WORKDIR /app


# How to run it when we start up the box?
#CMD ["gunicorn", "-b 0.0.0.0:5000", "-w 2", "main:app"]


# ENV FLASK_APP=app.main:app
# CMD ["flask", "run", "--host", "0.0.0.0"]
CMD ["export", "FLASK_APP=app.main:app", "&&", "flask", "run", "--reload"]

# # start from base
# FROM python:3.9

# # copy our application code
# ADD . /app
# WORKDIR /app

# COPY /backend/api.py ./
# COPY /benchmarks/pyproject.toml ./

# # Install dependencies
# RUN pip install -r requirements.txt
# RUN poetry install

# # expose port
# EXPOSE 5000

# # start app
# # CMD [ "python", "./backend/api.py" ]
# CMD [ "poetry", "run", "gunicorn", "-w", "1", "--threads", "4", "-b", "0.0.0.0:5000", "api:app" ]