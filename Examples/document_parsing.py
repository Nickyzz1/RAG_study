import time
import argparse
import asyncio
import sys
from pathlib import Path
from raganything import RAGAnything, RAGAnythingConfig
import os


def parsing_document(path: str):

    print(f"Parsing files from {path}")
    print(os.listdir(path))
    for list in os.listdir(path):
        file = Path(list)
        print(list)
    #     if not file.exists():
    #         print("File doesn't exists")
    #         return False
    #         # start_time = time.perf_counter()
    #     print(file)

parsing_document("C://Users//SPI1CT//Documents//Estudo XPertify//RAG-Anything//repo//RAG_study//Data//PDF")