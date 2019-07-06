import argparse
import logging

from services.processor import Processor

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", "-r", action="store_true")
    parser.add_argument("--ignore", "-ig", action="store_true")
    parser.add_argument("--recognize", "-rc", action="store_true")
    parser.add_argument("--input", "-i", nargs='+', type=str)
    parser.add_argument("--file", "-f", type=str)
    parser.add_argument("--output", "-o", type=str)
    parser.add_argument("--accounts", "-a", type=str)
    logging.basicConfig(filename="logs.log", level=logging.INFO)
    params = parser.parse_args()
    processor = Processor(params.accounts)
    if params.accounts is not None:
        processor.run_with_params_parallel(params)
    else:
        processor.run_with_params(params)
