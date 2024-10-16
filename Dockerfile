FROM python:3.11-slim
# Oficial image base on python, with its variant slim
WORKDIR /globant_coding_challenge
# Work directory inside the container
COPY requirements.txt .
# Copy from my machine to the work directory
RUN apt-get update && apt-get install -y curl && pip install --no-cache-dir -r requirements.txt
# Install the dependencies from requirements.txt
COPY . .
# Copy all the content from my local directory to the work directory

EXPOSE 8080
# Expose the 8080 port from the container

CMD ["python3", "scripts/main.py"]
# Define the default command that will be execute once the container start
