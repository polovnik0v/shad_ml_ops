FROM python:3.11

# Choose what directory should be a working directory
# If the directory does not exist then Docker will create it
WORKDIR /prediction_app

# Copy project files into working directory
COPY . .

# Copy our local file with requirements into Docker Image
COPY requirements.txt ./

# Install all the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Open port for Docker
EXPOSE 3000

# Run django
CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]
