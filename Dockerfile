from python:3.8.10

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . . 

ENV OPENAI_API_KEY=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  

WORKDIR /

CMD ["python", "chat.py"]