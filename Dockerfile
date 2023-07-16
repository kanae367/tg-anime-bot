FROM python:3.9
WORKDIR /usr/src/app/
COPY . /usr/src/app/
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]