# -*- coding:UTF-8 -*-
# @Author: Xuezhi Fang
# @Date: 2021-06-08
# @Email: jasonfang3900@gmail.com

from PIL import Image
from multiprocessing import Manager, Pool, cpu_count
import os
import re
from pdf2image import convert_from_path
from tqdm import tqdm
from argparse import ArgumentParser
import numpy as np
import shutil

def get_files(root_dir):
    assert os.path.exists(root_dir)
    paths = [path for path in os.listdir(root_dir) if re.search("PDF|pdf", path)]
    return paths

def binarize(img, thre):
    bi_table = [0 if i < thre else 1 for i in range(256)]
    bi_img = img.point(bi_table, "1")
    return bi_img

def process_img(img, idx, bi_thre, queue):
    img = img.convert("L")
    bi_img = binarize(img, bi_thre)
    queue.put((idx, bi_img))

def assert_gray(img):
    if img.ndim == 2:
        return True
    if (img[0] - img[1]).var() ==(img[1] - img[2]).var() == (img[0] - img[2]).var() == 0:
        return True
    else:
        return False

def img_order_map(queue, imgs_total):
    processed = [None for _ in range(imgs_total)]
    while not queue.empty():
        idx, bi_img = queue.get()
        processed[idx] = bi_img
    return processed

def main(args):
    pdf_dir = args.pdf_dir
    out_dir = args.out_dir
    bi_thre = args.bi_thre
    dpi = args.dpi
    threads = args.threads
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    for filename in tqdm(get_files(pdf_dir)):
        pool = Pool(threads)
        queue = Manager().Queue()
        src_path = os.path.join(pdf_dir, filename)
        out_path = os.path.join(out_dir, filename)
        first_page = convert_from_path(src_path, dpi=50, single_file=True)
        if first_page:
            first_img = np.array(first_page[0])
            if assert_gray(first_img):
                shutil.copy(src_path, out_path)
                print(f'"\n{filename}" is already grayscale, thus we copy it to the target dir instead of processing.\n')
                continue
        imgs = convert_from_path(src_path, dpi=dpi, thread_count=threads)
        imgs_total = len(imgs)
        for idx, img in enumerate(imgs):
            pool.apply_async(process_img, args=(img, idx, bi_thre, queue))
        pool.close()
        pool.join()
        bi_imgs = img_order_map(queue, imgs_total)

        bi_imgs[0].save(out_path, "PDF", save_all=True, append_images=bi_imgs[1:])


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--pdf_dir", type=str, required=True, help="dir contains pdf files")
    parser.add_argument("--out_dir", type=str, required=True, help="output dir")
    parser.add_argument("--dpi", type=int, default=200, help="imgs' dpi")
    parser.add_argument("--bi_thre", type=int, default=170, help="binarization threshold")
    parser.add_argument("--threads", type=int, default=cpu_count(), help="set num of threads to parallelize")
    args = parser.parse_args()
    main(args)
