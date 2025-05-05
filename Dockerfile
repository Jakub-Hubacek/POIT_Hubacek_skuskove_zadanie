FROM python:3.12

# 
WORKDIR /app

# 
COPY server/requirements.txt ./requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 
COPY server/app ./app

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]