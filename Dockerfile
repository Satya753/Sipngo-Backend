FROM python:3.9

WORKDIR /app

COPY . /app

ENV $(cat .env | xargs)
RUN pip install --no-cache-dir -r req.txt
RUN pip install mysql-connector


EXPOSE 5000
EXPOSE 3306

CMD ["python" , "apptest.py"]
