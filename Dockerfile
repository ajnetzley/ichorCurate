# Using the Python 3.11.5 image as the base
FROM python:3.11.5-slim

# Set the working directory to /app
WORKDIR /app



# Copy the current directory contents into the container
COPY . /app

# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Create a user to run the Streamlit app - uid will match
# service user svc_ichor_curate.

RUN groupadd -g 4323 g_svc_ichor_curate

RUN useradd -M -u 4323 -g 4323 svc_ichor_curate

# switch to the new user
USER svc_ichor_curate


# Expose the port that Streamlit will run on
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]