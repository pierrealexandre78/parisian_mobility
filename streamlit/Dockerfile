FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file from the project root
COPY requirements.in requirements.in

# Install dependencies
RUN pip install -r requirements.in

# Copy the app
COPY streamlit/ .

# Expose the port Streamlit runs on
EXPOSE 8501

# Run the streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
