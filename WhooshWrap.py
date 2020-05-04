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
    def __init__(self,MSID_index_dir, Searchable,MaxResults=10,Timeout = 0.5):
        ''' Initializes the wrapper object with ijdex reference and preferences
            parameter MSID_index_dir        = (string) Existing Whoosh Index directory
            parameter Searchable            = (string) List of fieldnames of the index to search
            parameter MaxResults       = (numeric) Maximum # of results to return
            parameter Timeout       = (numeric) Maximum # of seconds to wait before ending search
        
        '''
        self.ix = index.open_dir(MSID_index_dir)                         #  
        self.qp = MultifieldParser(Searchable, schema=self.ix.schema)    # Search all the specified fields
        #self.qp =  QueryParser(Searchable[0], schema=self.ix.schema)    # Search ONLY the first field
        #self.s = self.ix.searcher(weighting = scoring.Frequency)        # Simple Scorer
        self.s = self.ix.searcher(weighting = scoring.BM25F)         # Fancy Scorer
        c = self.s.collector(limit=MaxResults)                # The "collector" allows setting the timeout for a search. In this case it's 0.5 seconds which is a little long...
        self.c = TimeLimitCollector(c,Timeout)               
        self.Searchable = Searchable
        self.LastResults = None
        
    def doSearch(self,qstring,ReturnFields):
        ''' Performs a search on the index with the provided query and returns a Dict of results
            parameter qstring       = (string) Search key
            parameter ReturnFields  = (list of strings) List of fieldnames to include in return results.  NOTE, may be different than Searchable, but fields must exist in index
            returnval result_fields = dict of result strings : lists per field, i.e. 
                                    = result_dict = {'Return Fields 1' : [ list of result strings ], 'Return Fields 2' : [ list of result strings ]....}
        '''
        q = self.qp.parse(qstring)          # build query with event-provided search key        
        try:
            self.s.search_with_collector(q,self.c)
        except:
            print("TIMEOUT!")                       # DEBUG out put to console if we're timing out a lot  
        results = self.c.results()                       # If we do get a timeout, still return whatever we've got, i.e. partial results    
        self.LastResults = results                  #
        ResultsDict ={}
        for field in ReturnFields:
            ResultsDict[field] = []
            for res in results:
                ResultsDict[field].append(res[field]) # should check that field is in results
        return ResultsDict
            