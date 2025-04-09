# Server Dockerfile
FROM python:3.12.3-slim

# Do everything as user
RUN useradd user
USER user

ENV HOME=/home/user\
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME

# Copy GET-Food/server contents to working dir and install requirements
COPY --chown=user ./server $HOME/server
RUN pip install --no-cache-dir --upgrade -r server/requirements.txt

# Copy example_data into container and populate the db
COPY --chown=user ./example_data $HOME/example_data
RUN python ./server/populate_db.py ./example_data/example_data.csv

#Expose port where flask app is running
EXPOSE 5000

# Launch the server on container start
CMD ["python", "server/app.py"]