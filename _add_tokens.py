#!/usr/bin/env python
import sys


def add_tokens(src_model, dest_model):
    from transformers import GPT2Tokenizer, GPT2LMHeadModel

    print("Loading model ", src_model)
    model = GPT2LMHeadModel.from_pretrained(src_model)
    print("Loading tokenizer ", src_model)
    tokenizer = GPT2Tokenizer.from_pretrained(src_model)
    
    print("Adding new tokens")
    tokenizer.add_special_tokens(
    	{'additional_special_tokens': ['<char>']}
    )
    model.resize_token_embeddings(len(tokenizer))

    print("Save tokenizer ", dest_model)
    tokenizer.save_pretrained(dest_model)
    print("Save model ", dest_model)
    model.save_pretrained(dest_model)

if __name__=='__main__':
    if (len(sys.argv) < 3):
        exit('Usage: add_tokens.py src_model_path desc_model_path')
    add_tokens(sys.argv[1], sys.argv[2])
