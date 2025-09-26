# 1. Imagem base Python
FROM python:3.11-slim

# 2. Diretório de trabalho dentro do container
WORKDIR /app

# 3. Copia o requirements.txt e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia todo o código para dentro do container
COPY . .

# 5. Expõe a porta desejada
EXPOSE 9000

# 6. Comando para iniciar a API
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "9000"]
