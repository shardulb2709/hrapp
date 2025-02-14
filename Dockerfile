FROM --platform=linux/amd64 python:3.9
  
# Set environment variables  
ENV PYTHONDONTWRITEBYTECODE=1  
ENV PYTHONUNBUFFERED=1  
  
# Set working directory  
WORKDIR C:\Users\sborhade\hrapp  
  
# Install dependencies  
 
RUN pip install --upgrade pip  
RUN pip install -r requirements.txt  
  
# Copy project  
COPY . .  
  
# Expose port (change if your app uses a different port)  
EXPOSE 8000  
  
# Command to run the application  
CMD ["python", "hrapp.py"]
