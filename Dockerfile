# from python:3.12

# WORKDIR /app
# COPY requirements.txt .
# RUN pip install -r requirements.txt
# COPY . .
# # Install system dependencie
# COPY entrypoint.sh .
# RUN chmod +x entrypoint.sh
# EXPOSE 8000

# CMD [ "./entrypoint.sh" ]

FROM python:3.12-slim

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN  pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
