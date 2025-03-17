## Instructions

### Python

NB: below requires absolute paths so far
```shell
cd pyonb/ocr/marker
python main.py ../tests/ms-note-one-page.pdf output-data/output.txt
```

### Docker Compose

NB: requires file in input-data/ms-note-one-page.pdf
```shell
cd pyonb/ocr/marker
docker compose run marker input-data/ms-note-one-page.pdf output-data/output.txt
```

