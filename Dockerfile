FROM rasa/rasa:latest-full

RUN cd / && pip install --no-cache-dir tensorflow-text

CMD [ "echo", "Rasa is running" ]