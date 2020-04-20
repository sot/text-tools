# text-tools
Tools for indexing, searching and analyzing textual info

## Whoosh Indexing
* Dependencies - whoosh
  * Available by "pip install whoosh"
* python3+

### WhooshIndexer.py
Creates an index from .csv files for use with search-as-you-type clients
See cmd line help below

    python WhooshIndexer.py -h
    usage: WhooshIndexer [-h] [--outfolder OUTFOLDER] [-s S] [--nMin NMIN] [--nMax NMAX] infiles [infiles ...]

    positional arguments:
      infiles               Specify a set of .csv files to add to the index.

    optional arguments:
      -h, --help            show this help message and exit
      --outfolder OUTFOLDER
                        Specify the folder where the index will be created. Specifying an existing index will overwite it. Default value     is 'WhooshIdx'
      -s S                  Specify the searchable fields. May be specified multiple times
      --nMin NMIN           Specify min nGram size, default is 3
      --nMax NMAX           Specify max nGram size, default is 8



### SearcherGUI_NGRAM.py
   ** Client Example using low-level Whoosh API (soon to be deprecated)  **

### SearcherGUI_NGRAMWrap.py
** Client Example using Whoosh Wrapper API   **
Just run from the command line

    python SearcherGUI_NGRAMWrap.py

### SearcherGUI_NGRAM_MAUDE.py
   ** Demo of Searchable MAUDE client (based on low-level Whoosh API) **
   
### WhooshWrap.py
** Whoosh Wrapper class that hides low-level API for search clients.  
Requires an existing index
Methods:

    def __init__(self,MSID_index_dir, Searchable):
        ''' Initializes the wrapper object with ijdex reference and preferences
            parameter MSID_index_dir        = (string) Existing Whoosh Index directory
            parameter Searchable            = (string) List of fieldnames of the index to search    
        '''
    def doSearch(self,qstring,MaxResults,Timeout,ReturnFields):
        ''' Performs a search on the index with the provided query and returns a Dict of results
            parameter qstring       = (string) Search key
            parameter MaxResults    = (int) Maximum # of results to return
            parameter Timeout       = (numeric) Maximum # of seconds to wait before ending search
            parameter ReturnFields  = (list of strings) List of fieldnames to include in return results.  NOTE, may be different than Searchable, but fields must exist in index
            returnval result_fields = dict of result strings : lists per field, i.e. 
                                    = result_dict = {'Return Fields 1' : [ list of result strings ], 'Return Fields 2' : [ list of result strings ]....}
        '''
    
   
