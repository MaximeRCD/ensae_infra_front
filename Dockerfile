# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /flask_app

ENV ENV=STAGING

# Copy the current directory contents into the container at /app
COPY ./requirements.txt /flask_app/requirements.txt
COPY ./.env /flask_app/.env
COPY ./static/* /flask_app/routers/
COPY ./templates/* /flask_app/models/
COPY ./api.py  /flask_app/
COPY ./interface_yn.py /flask_app/
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /flask_app/requirements.txt

# Run app.py when the container launches
CMD ["flask","--app","interface_yn.py", "run", "--host", "0.0.0.0", "--port", "5000", "--reload"]
