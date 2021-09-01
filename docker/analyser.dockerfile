# Gets image with easyocr/pytorch already
FROM challisa/easyocr
RUN mkdir /app
WORKDIR /app
# Copies requirements.txt early to install dependencies on lower images.
COPY /analyser/requirements.txt .
RUN pip install -r requirements.txt
# Now copies all analyser files
COPY analyser ./analyser
WORKDIR /app/analyser
# Starts server/listener
CMD ["python", "listener.py"]