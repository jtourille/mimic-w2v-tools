import argparse
import logging
import os
import sys
import time

from mimic.ctakes import ctakes_corpus, ctakes_to_txt
from mimic.extract import extract_mimic_documents
from mimic.tools import ensure_dir
from mimic.transform import regroup_patient_documents, replace_placeholders, clean_mimic_corpus

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title="Sub-commands", description="Valid sub-commands",
                                       help="Valid sub-commands", dest="subparser_name")

    # MIMIC document extraction from database
    parser_extract = subparsers.add_parser('EXTRACT', help="Extract MIMIC documents from database")
    parser_extract.add_argument("--url", help="Database URL", dest="url", type=str, required=True)
    parser_extract.add_argument("--output-dir", help="Output directory", dest="output_dir", type=str, required=True)

    # MIMIC placeholders replacement
    parser_replace = subparsers.add_parser('REPLACE', help="Perform pseudonymization of the documents")
    parser_replace.add_argument("--input_dir", help="Input directory", dest="input_dir", type=str, required=True)
    parser_replace.add_argument("--output_dir", help="Output directory", dest="output_dir", type=str, required=True)
    parser_replace.add_argument("--list_dir", help="List directory", dest="list_dir", type=str, required=True)

    # MIMIC clean files
    parser_clean = subparsers.add_parser('CLEAN', help="Clean MIMIC documents")
    parser_clean.add_argument("--input_dir", help="Input directory", dest="input_dir", type=str, required=True)
    parser_clean.add_argument("--output_dir", help="Output directory", dest="output_dir", type=str, required=True)
    parser_clean.add_argument("-n", "--n_jobs", help="Number of processes", dest="n_jobs", type=int, default=1,
                              required=True)

    # MIMIC document ctakes processing
    parser_ctakes = subparsers.add_parser('CTAKES', help="Process MIMIC documents with cTAKES")
    parser_ctakes.add_argument("--input_dir", help="Input directory", dest="input_dir", type=str, required=True)
    parser_ctakes.add_argument("--output_dir", help="Output directory", dest="output_dir", type=str, required=True)
    parser_ctakes.add_argument("--ctakes_dir", help="cTAKES directory", dest="ctakes_dir", type=str, required=True)
    parser_ctakes.add_argument("--java_dir", help="Java bin directory", dest="java_dir", type=str, required=True)
    parser_ctakes.add_argument("--resources_dir", help="Resource directory", dest="resources_dir", type=str,
                               required=True)

    # Sentence and token extraction from cTAKES files
    parser_txt = subparsers.add_parser('CTAKES-TO-TXT', help="Sentence and token extraction from cTAKES files")
    parser_txt.add_argument("--xml_dir", help="Input json directory", dest="xml_input_dir", type=str, required=True)
    parser_txt.add_argument("--txt_dir", help="Input txt directory", dest="txt_input_dir", type=str, required=True)
    parser_txt.add_argument("--output_dir", help="Output directory", dest="output_dir", type=str, required=True)
    parser_txt.add_argument("-n", "--n_jobs", help="Number of processes", dest="n_jobs", type=int, default=1,
                            required=True)

    args = parser.parse_args()

    if args.subparser_name == "EXTRACT":

        target_dir = os.path.join(os.path.abspath(args.output_dir))

        if os.path.isdir(target_dir):
            raise IsADirectoryError("The output path you specified already exists")

        ensure_dir(target_dir)

        logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(message)s')

        logging.info("Starting document extraction from mimic-iii database")

        extract_mimic_documents(args.url, target_dir)

    elif args.subparser_name == "REPLACE":

        timestamp = time.strftime("%Y%m%d-%H%M%S")

        target_dir = os.path.join(os.path.abspath(args.output_dir))

        if os.path.isdir(target_dir):
            raise IsADirectoryError("The output path you specified already exists")

        ensure_dir(target_dir)

        log_file_path = os.path.join(target_dir, "replace-{}.log".format(timestamp))
        logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s %(message)s')

        logging.info("Starting placeholder replacing")

        replace_placeholders(args.input_dir, args.output_dir, args.list_dir)

    elif args.subparser_name == "CLEAN":

        timestamp = time.strftime("%Y%m%d-%H%M%S")

        target_dir = os.path.join(os.path.abspath(args.output_dir))

        if os.path.isdir(target_dir):
            raise IsADirectoryError("The output path you specified already exists")

        ensure_dir(target_dir)

        log_file_path = os.path.join(target_dir, "clean-{}.log".format(timestamp))
        logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s %(message)s')

        logging.info("Starting corpus cleaning")

        clean_mimic_corpus(args.input_dir, args.output_dir, n_jobs=args.n_jobs)

    elif args.subparser_name == "CTAKES":

        timestamp = time.strftime("%Y%m%d-%H%M%S")

        target_dir = os.path.join(os.path.abspath(args.output_dir))

        if os.path.isdir(target_dir):
            raise IsADirectoryError("The output path you specified already exists")

        ensure_dir(os.path.abspath(args.output_dir))

        log_file_path = os.path.join(os.path.abspath(target_dir), "ctakes-{}.log".format(timestamp))
        logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s %(message)s')

        logging.info("Processing files with cTAKES")
        logging.info("============================")
        logging.info("* Input directory: {}".format(os.path.abspath(args.input_dir)))
        logging.info("* Output directory: {}".format(os.path.abspath(args.output_dir)))

        ctakes_corpus(args.input_dir, args.output_dir, args.ctakes_dir, args.java_dir, args.resources_dir)

    elif args.subparser_name == "CTAKES-TO-TXT":

        timestamp = time.strftime("%Y%m%d-%H%M%S")

        target_dir = os.path.join(os.path.abspath(args.output_dir))

        if os.path.isdir(target_dir):
            raise IsADirectoryError("The output path you specified already exists")

        ensure_dir(os.path.abspath(args.output_dir))

        log_file_path = os.path.join(os.path.abspath(target_dir), "ctakesTXT-{}.log".format(timestamp))
        logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s %(message)s')

        logging.info("Starting sentence and token extraction from cTAKES files")

        ctakes_to_txt(args.xml_input_dir, args.txt_input_dir, args.output_dir, args.n_jobs)
