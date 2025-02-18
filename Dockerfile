FROM python:3.11-slim AS base

# Set environment variables  
ENV PYTHONDONTWRITEBYTECODE=1  
ENV PYTHONUNBUFFERED=1  
  
# Set working directory  
WORKDIR /app  


# Copy project  

COPY . /app

# Install dependencies  

 
RUN pip install --upgrade pip  
RUN pip install -r requirements.txt  
  
  
# Expose port (change if your app uses a different port)  
EXPOSE 5000 
 
# Command to run the application  
CMD ["python", "hrapp.py"]
