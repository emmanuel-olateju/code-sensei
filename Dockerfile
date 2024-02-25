FROM python:3.11.1

# Install git
RUN apt-get update && apt-get install -y git

# Create app directory
WORKDIR /app

# Clone repo
RUN git clone https://github.com/emmanuel-olateju/code-sensei /app

# Install any needed packages specified in requirements.txt
RUN pip install openai
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENTRYPOINT [ "streamlit","run","code-sensei.py","--server.port","80" ]