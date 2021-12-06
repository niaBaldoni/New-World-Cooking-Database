FROM python:latest

WORKDIR /app
COPY . .

ENV DATABASE_URL="mysql://eugenia:nwdb@127.0.0.1/food_db"

RUN pip install regex
RUN pip install SQLAlchemy
RUN pip install mysqlclient
RUN pip install AdvancedHTMLParser
RUN pip install requests
RUN pip install numpy

CMD ["python3", "./main.py"]