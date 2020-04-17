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
