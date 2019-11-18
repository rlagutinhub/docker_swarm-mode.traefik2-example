FROM python:3
WORKDIR /app
COPY . /app
RUN pip3 install -U pip Flask psutil
EXPOSE 8000
CMD ["python3", "app.py", "8000"]
