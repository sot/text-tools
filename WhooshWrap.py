from whoosh import index
from whoosh.qparser import MultifieldParser
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, NGRAM, NGRAMWORDS
from whoosh.qparser import QueryParser
from whoosh.qparser import FuzzyTermPlugin
from whoosh import scoring
from whoosh.collectors import TimeLimitCollector
from whoosh.highlight import WholeFragmenter

class WhooshWrap():
    '''
        Wrapper class to make Whoosh API a little simpler
        Initialize by pointing to an existing Whoosh index and specifying searchable fields, Max Results and Timeout
        Query by running self.doSearch, providing query string, and timeout
        Results of the last search are stored in the object as Whoosh results object (requires open index to access) and returned as a traditional python dictionary
    '''
    def __init__(self,MSID_index_dir, Searchable):
        ''' Initializes the wrapper object with ijdex reference and preferences
            parameter MSID_index_dir        = (string) Existing Whoosh Index directory
            parameter Searchable            = (string) List of fieldnames of the index to search
        
        '''
        self.ix = index.open_dir(MSID_index_dir)                         #  
        self.qp = MultifieldParser(Searchable, schema=self.ix.schema)    # Search all the specified fields
        self.Searchable = Searchable
        self.LastResults = None
        
    def doSearch(self,qstring,MaxResults,Timeout,ReturnFields):
        ''' Performs a search on the index with the provided query and returns a Dict of results
            parameter qstring       = (string) Search key
            parameter MaxResults    = (int) Maximum # of results to return
            parameter Timeout       = (numeric) Maximum # of seconds to wait before ending search
            parameter ReturnFields  = (list of strings) List of fieldnames to include in return results.  NOTE, may be different than Searchable, but fields must exist in index
            returnval result_fields = dict of result strings : lists per field, i.e. 
                                    = result_dict = {'Return Fields 1' : [ list of result strings ], 'Return Fields 2' : [ list of result strings ]....}
        '''
        q = self.qp.parse(qstring)          # build query with event-provided search key
        with self.ix.searcher(weighting = scoring.BM25F) as s:    # there are several NLP style scorers for Whoosh
            c = s.collector(limit=MaxResults)                # The "collector" allows setting the timeout for a search. In this case it's 0.5 seconds which is a little long...
            c = TimeLimitCollector(c,Timeout)               
            try:
                s.search_with_collector(q,c)
            except:
                print("TIMEOUT!")                       # DEBUG out put to console if we're timing out a lot  
            results = c.results()                       # If we do get a timeout, still return whatever we've got, i.e. partial results    
            self.LastResults = results                  #
            ResultsDict ={}
            for field in ReturnFields:
                ResultsDict[field] = []
                for res in results:
                    ResultsDict[field].append(res[field]) # should check that field is in results
            return ResultsDict
            