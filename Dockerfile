FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
#--no-cache-dir keeps the container small by not saving installation junk
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/ ./scripts/

CMD ["/bin/bash"]