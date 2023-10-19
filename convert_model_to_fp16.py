#!/usr/bin/env python
import sys
import torch


def convert_model(src_model, dest_model):
    from transformers import AutoTokenizer, AutoModel

    print("Loading model ", src_model)
    model = AutoModel.from_pretrained(src_model)
    print("Loading tokenizer ", src_model)
    tokenizer = AutoTokenizer.from_pretrained(src_model)
    
    print("Convert to fp16")
    model = model.half()

    print("Save tokenizer ", dest_model)
    tokenizer.save_pretrained(dest_model)
    print("Save model ", dest_model)
    model.save_pretrained(dest_model, safe_serialization=True)


if __name__=='__main__':
    if (len(sys.argv) < 3):
        exit('Usage: convert_model_to_fp16.py src_model_path desc_model_path')
    convert_model(sys.argv[1], sys.argv[2])

