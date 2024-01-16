FROM python:3.11.7

COPY . ./ItsMichaAIBot
RUN python3 -m pip install -r requirements.txt
WORKDIR /ItsMichaAIBot

# specify the port number the container should expose
EXPOSE 3000

# rn the application
CMD ["python", "main.py"] 
