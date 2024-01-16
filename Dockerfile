FROM python:3.11.7

COPY . /ItsMichaAIBot

WORKDIR /ItsMichaAIBot

RUN python3 -m pip install -r requirements.txt

# specify the port number the container should expose
EXPOSE 3000

# rn the application
CMD ["python", "main.py"] 
