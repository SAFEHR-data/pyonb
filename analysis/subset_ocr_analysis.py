"""Script to evaluate OCR tool performance in subset of 20 clinical documents."""
import os
import sys
from pathlib import Path
import pandas as pd
import json

# Add analysis/ dir to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from analysis.eval_ocr import main as run_eval_ocr


"""
Preprocessing
"""
WORKING_DIR = Path("/home/trobert4/pyonb_ocr_analysis/_test_subset")
os.chdir(WORKING_DIR)

COPY_PASTE_TXT_PATH = WORKING_DIR / "_pdf_copy_paste_to_txt"

DOCLING_JSON_OUTPUT_PATH = WORKING_DIR / Path("_docling_json")
MARKER_JSON_OUTPUT_PATH = WORKING_DIR / Path("_marker_json")
PADDLEOCR_JSON_OUTPUT_PATH = WORKING_DIR / Path("_paddleocr_json")

Path.mkdir(DOCLING_JSON_OUTPUT_PATH, exist_ok=True)
Path.mkdir(MARKER_JSON_OUTPUT_PATH, exist_ok=True)
Path.mkdir(PADDLEOCR_JSON_OUTPUT_PATH, exist_ok=True)


"""
Extract JSON from .csv to individual .json files

Note:
- eval_ocr.py expects .txt and .json files (not .csv)

JSON responses:
- docling / marker = markdown
- paddleocr = array of strings? TODO(Tom): may need to amend
"""
AIRFLOW_OCR_DIR = WORKING_DIR / Path("_airflow_ocr")
csv_files = ["docling-results.csv", "marker-results.csv", "paddleocr-results.csv"]
json_output_dirs = [DOCLING_JSON_OUTPUT_PATH, MARKER_JSON_OUTPUT_PATH, PADDLEOCR_JSON_OUTPUT_PATH]

for csv_file, json_output_dir in zip(csv_files, json_output_dirs):
    df = pd.read_csv(AIRFLOW_OCR_DIR / Path(csv_file))
    # print(df.columns)
    for doc_filename, doc_json_response in zip(df["name"], df["result"]):
        print(f"Document filename: {doc_filename} \n {doc_json_response} \n")
        with open(json_output_dir / f"{doc_filename}.json", "w") as f:
            json.dump(doc_json_response, f)


"""
Run OCR evaluation metrics
"""

gt_txt_filenames = sorted([p for p in Path(COPY_PASTE_TXT_PATH).iterdir()])
ocr_json_filenames_nested_array = [
    sorted([p for p in Path(DOCLING_JSON_OUTPUT_PATH).iterdir()]),
    sorted([p for p in Path(MARKER_JSON_OUTPUT_PATH).iterdir()]),
    sorted([p for p in Path(PADDLEOCR_JSON_OUTPUT_PATH).iterdir()])
]
# print(gt_txt_filenames, ocr_json_filenames)

ocr_tools = ["docling", "marker", "paddleocr"]

print("OCR Evaluation results:")

for ocr_json_filenames in ocr_json_filenames_nested_array:
    
    ocr_eval_results = []
    current_ocr_tool = [tool for tool in ocr_tools if tool in str(ocr_json_filenames[0].parent)]
    print("\nEvaluating OCR tool: {current_ocr_tool} \n")
    
    for gt_txt_file, ocr_json_file in zip(gt_txt_filenames, ocr_json_filenames):
        try:
            ocr_metrics = run_eval_ocr(gt_txt_file, ocr_json_file)
            print(f"gt_txt: {gt_txt_file.name} / ocr_json: {ocr_json_file.name} - {ocr_metrics}")

            ocr_metrics['gt_txt_filename'], ocr_metrics['ocr_json_filename'] = gt_txt_file.name, ocr_json_file.name
            ocr_eval_results.append(ocr_metrics)

        except Exception as e:
            print(f"Error processing {gt_txt_file.name} or {ocr_json_file.name}: {e}")
            continue  # skip to the next pair

    df_results = pd.DataFrame(ocr_eval_results)
    df_results = df_results[["gt_txt_filename", "ocr_json_filename", "cer", "wer", "ned"]] # reorder
    
    print(df_results)
    
    output_filename = WORKING_DIR / Path(f"ocr_eval_results_{str(current_ocr_tool[0])}.csv")
    df_results.to_csv(output_filename, index=False)