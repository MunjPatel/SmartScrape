class GSEExceptions(Exception):
    """

    Scraper exceptions class which inherits properties of the 'Exception' class. Returns a string as output.
    Specifically for scraping list of websites using GSE.

    """
    def __init__(self,_arg_:str)->None:
        self._arg_ = _arg_
        super().__init__(self._arg_)
    def __str__(self) -> str:
        return self._arg_

class GoogleSearchError(GSEExceptions):
    """Custom exception for Google Search errors."""
    pass