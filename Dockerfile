from python:latest

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

# # TODO remove ??
# RUN chmod +x *
# RUN chmod +x */*


EXPOSE 8001
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "--workers", "3", "karabela.wsgi"]
