FROM python:3.8.6-alpine
RUN apk add --no-cache gcc libc-dev git
RUN apk add --no-cache jpeg-dev zlib-dev freetype-dev
RUN MULTIDICT_NO_EXTENSIONS=1 YARL_NO_EXTENSIONS=1 pip install --no-cache-dir runescape-text Pillow
WORKDIR /runescape/
CMD python -u /runescape/main.py
ADD *.py /runescape/