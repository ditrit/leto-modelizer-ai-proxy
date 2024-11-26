FROM python:3.12.3-slim-bookworm

# Set up working directory
WORKDIR /code

# Copy Pipfile and source code into the container
COPY ./Pipfile /code
COPY ./Pipfile.lock /code
COPY ./src /code/src

# Install required system dependencies and pip
RUN apt update && \
    apt upgrade -y && \
    pip install pipenv && \
    pipenv install --deploy

# Expose the required port
EXPOSE 8585

# Set the PATH
ENV PATH="/root/.local/bin:${PATH}"

# Set the DECRYPTION_KEY environment variable (defaulted to dev key)
# CHANGE THIS IN PRODUCTION
ENV DECRYPTION_KEY="123456789"

# Run the application with Hypercorn
CMD ["pipenv", "run", "hypercorn", "src.main:app", "--reload", "--bind", "0.0.0.0:8585"]
