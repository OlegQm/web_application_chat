FROM python:3.8.8
WORKDIR /webapp
COPY . .
ARG OPENAI_API_KEY="default"
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "-m", "streamlit", "run", "gpt_3/application.py"]