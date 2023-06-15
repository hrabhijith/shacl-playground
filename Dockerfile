from python:3.8.10

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . . 

ENV OPENAI_API_KEY=<YOUR_API_KEY>

WORKDIR /

CMD ["python", "chat.py"]