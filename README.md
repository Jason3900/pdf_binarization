# PDF binarization

## Intro
a simple program to convert pdf to binarized version  

## Requirements
```bash
conda install -c conda-forge poppler  
pip install pdf2image pillow tqdm  
```

## Usage
**Usage**:
```python
python bi_pdf.py --pdf_dir PDF_DIR --out_dir OUT_DIR [--dpi DPI] [--bi_thre BI_THRE] [--threads THREADS]  
# args in [] means optional
```

**Arguments**: 
```bash
-h, --help	show this help message and exit  
--pdf_dir	dir contains pdf files, multi files are supported  
--out_dir	OUT_DIR  output dir  
--dpi DPI	imgs' dpi  
--bi_thre	binarization threshold  
--threads	set num of threads to speed up  
```
