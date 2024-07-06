# Use the official MageAI image as base
FROM mageai/mageai:latest

# Install Node.js
RUN apt-get update && apt-get install -y nodejs npm

# Set the working directory in the container
ARG USER_CODE_PATH=/home/src/${PROJECT_NAME}
WORKDIR ${USER_CODE_PATH}

# Copy Python requirements.txt from the host to the container
COPY requirements.txt ${USER_CODE_PATH}/requirements.txt

# Install Python dependencies
RUN pip3 install -r ${USER_CODE_PATH}/requirements.txt

# Set up environment variables and expose ports if needed

# Command to run the application (if needed)
# CMD ["mage", "start", "${PROJECT_NAME}"]