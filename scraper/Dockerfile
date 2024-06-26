FROM python:3.10

WORKDIR /app

EXPOSE 8001

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Команда для запуска скрапера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]