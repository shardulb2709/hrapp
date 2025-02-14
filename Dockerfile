FROM python:3.9-slim  
  
# Set environment variables  
ENV PYTHONDONTWRITEBYTECODE=1  
ENV PYTHONUNBUFFERED=1  
  
# Set working directory  
WORKDIR /home/sborhade/hrapp  
  
# Install dependencies  
COPY requirements.txt .  
RUN pip install --upgrade pip  
RUN pip install -r requirements.txt  
  
# Copy project  
COPY . .  
  
# Expose port (change if your app uses a different port)  
EXPOSE 8000  
  
# Command to run the application  
CMD ["python", "hrapp.py"]
