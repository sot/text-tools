# Python Application which provides live (search as you type) MSID results
import csv
import os, os.path
from whoosh import index
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, NGRAM, NGRAMWORDS
from whoosh.qparser import QueryParser
from whoosh.analysis import RegexTokenizer
from whoosh.analysis import LowercaseFilter
from whoosh.analysis import StopFilter
from whoosh.analysis import NgramWordAnalyzer
from whoosh import writing

import argparse

def get_parser():
    """
    Creates a new argument parser.
    """
    parser = argparse.ArgumentParser('WhooshIndexer')
    parser.add_argument('--outfolder', default='WhooshIdx', help='Specify the folder where the index will be created.  Specifying an existing index will overwite it. Default value is \'WhooshIdx\'')
    parser.add_argument('-s', default=[],action='append', help='Specify the searchable fields.  May be specified multiple times')
    parser.add_argument('--nMin', default=3,type=int,help='Specify min nGram size, default is 3')
    parser.add_argument('--nMax', default=8,type=int,help='Specify max nGram size, default is 8')
    parser.add_argument('WhooshIdx',  nargs='+', help='Specify a set of .csv  files to add to the index.')
 
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    NgramMin = args.nMin
    NgramMax = args.nMax
    if NgramMax < NgramMin:
        NgramMax = NgramMin
        print('nMax cannot be less than nMin. Setting nMax to nMin')
    MSID_index_dir  = args.outfolder
    Searchable = args.s
    MSID_CSV_fnames = args.infiles
        
                                                   #   TBD: add cmdline flag to set/use a particular index
    if not os.path.exists(MSID_index_dir):
         print("Doesn't exist, creating directory %s" % MSID_index_dir )
         os.mkdir(MSID_index_dir)
      
    ## Indicate which fields to NGRAM-ize
    ## Create Empty Schema 
    schema = Schema()
    ix = index.create_in(MSID_index_dir, schema)
    writer = ix.writer() 
    writer.commit(mergetype=writing.CLEAR,optimize=True)                      # Erase the index to start from scratch
    writer = ix.writer() 
    for cur_file in MSID_CSV_fnames:
        with open(cur_file, newline='',encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames 
            for field in fieldnames:
                if not field in ix.schema.names():
                    if field in Searchable:                                 # NGRAM-ize the field
                        writer.add_field(field, TEXT(stored=True, analyzer=NgramWordAnalyzer(NgramMin, maxsize=NgramMax, tokenizer=RegexTokenizer()), phrase =False))                               # May need to adjust size to allow for description            
                    else:                                                   # Just store raw text
                        writer.add_field(field, TEXT(stored=True))
        writer.commit(optimize=True)
        writer = ix.writer() 
    idx_cnt = 0
    for cur_file in MSID_CSV_fnames:
        print('Indexing %s' % cur_file)
        with open(cur_file, newline='',encoding='utf-8') as csvfile:    
            reader = csv.DictReader(csvfile)   
            for row in reader:  
                idx_cnt += 1            
                writer.add_document(**row)       
                last_row = row
                if idx_cnt % 1000 == 0:
                    print(idx_cnt)
    print('Indexing Done, committing changes to disk')
    writer.commit()
 
if __name__ == "__main__":
    main()
 
## Now Ready to  Search