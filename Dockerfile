FROM --platform=linux/amd64 python:3.9
  
# Set environment variables  
ENV PYTHONDONTWRITEBYTECODE=1  
ENV PYTHONUNBUFFERED=1  
  
# Set working directory  
WORKDIR /app  
  
# Install dependencies  

COPY requirements.txt/app/
 
RUN pip install --upgrade pip  
RUN pip install -r requirements.txt  
  
# Copy project  
COPY . .  
  
# Expose port (change if your app uses a different port)  
EXPOSE 5000 
  
# Command to run the application  
CMD ["python", "hrapp.py"]
