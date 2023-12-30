# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /flask_app

ENV ENV=STAGING

# Copy the current directory contents into the container at /app
COPY ./requirements.txt /flask_app/requirements.txt
COPY ./.env /flask_app/.env
COPY ./static/css/* /flask_app/static/css/
COPY ./templates/* /flask_app/templates/
COPY ./api.py  /flask_app/
COPY ./interface.py /flask_app/interface.py
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /flask_app/requirements.txt

# Run app.py when the container launches
CMD ["flask","--app","interface.py", "run", "--host", "0.0.0.0", "--port", "5000", "--reload"]
