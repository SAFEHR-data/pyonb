# OCR performance evaluation metrics

The `analysis` directory contains code for evaluating the performance of OCR tools. The metrics include:

- Character Error Rate (CER)
- Word Error Rate (WER)
- Normalised Edit Distance (NED)

For all of these metrics 0 = perfect score and 1 = maximum dissimilarity.

## Usage

1. **Ground Truth File:** Let's say you have a document in PDF format. Transcribe the PDF (e.g. copy-paste or something more sophisticated) into a .txt file and save (e.g. `ground-truth.txt`).

2. **OCR Processed File:** Process your PDF file with an OCR tool. Either save the output as a .txt file, or in the case of pyonb, save it as a .json file (e.g. `ocr-output.json`). Note, the JSON response from pyonb is a dictionary structure which contains a key-value pair `"ocr-result": "example output text"`

3. Run OCR performance metrics (code below uses files in [tests/](../tests/data/ocr_eval/) directory):

```shell
cd pyonb/
python -m analysis.eval_ocr -gt tests/data/ocr_eval/copy_paste_ms-note-one-page.txt -ocr tests/data/ocr_eval/marker_ocr_ms-note-one-page.json
```

The command will return CER, WER and NED, e.g.:

```shell
{'cer': 0.055, 'wer': 0.272, 'ned': 0.053}
```
