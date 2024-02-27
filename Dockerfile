FROM python:3.11.7-alpine

COPY . .

RUN python3 -m pip install -r requirements.txt

# specify the port number the container should expose
EXPOSE 3000

# run the application
CMD ["python", "main.py"] 
