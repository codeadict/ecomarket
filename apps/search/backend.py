from haystack.backends.solr_backend import SolrEngine, SolrSearchBackend, SolrSearchQuery
from haystack.backends import BaseEngine, BaseSearchBackend, BaseSearchQuery, log_query, EmptyResults

class CustomSolrSearchBackend(SolrSearchBackend):
    @log_query
    def search(self, query_string, **kwargs):
        # We encapsulate the main query, then add the secondary query and 'score'
        # modifier on the end in a way that the main query completely controls
        # the contents of the search results, and the additional ones just
        # adjust the scoring.

        # The 'boost' parameter is used to add additional weight to specific
        # fields, e.g. ships_from:US and ships_to:US should appear higher up
        # the search results, the OR operator is used with '*:*' to make it
        # entirely optional

        # The _val_ defines custom parameters to be added into the 'score' to
        # further boost the position of products with specific attributes 
        # in an algorithmic fashion. This is a little bit of 'black magic' and
        # relies on careful checking of the results sets and isn't perfect, yet.

        boost = getattr(self, 'boost', None)
        query_string = '(' + query_string + ')'
        if boost:
            query_string += ' AND _query_:"' + ' OR '.join(boost) + ' OR *:*"'
        query_string += ' _val_:"sum(scale(ord(number_of_recent_sales),0,20), scale(ord(number_of_sales),0,2))"'
        return super(CustomSolrSearchBackend, self).search(query_string, **kwargs)        

    """
    def build_search_kwargs(self, *la, **kwa):
        args = super(CustomSolrSearchBackend, self).build_search_kwargs(*la, **kwa)
        args['debugQuery'] = 'on'
        return args    
    """

class CustomSolrEngine(SolrEngine):
    backend = CustomSolrSearchBackend