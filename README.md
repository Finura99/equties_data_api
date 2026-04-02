
##
01/04/2026
- have been using request and cached data loaded once by the app in top mvoers and/bulk endpoints.
- single-symbol lookup uses SQLite.

##
- ENDPOINTS
1. /prices -> uses cached csv bulk read
2. /prices/{symbol} -> SQL single-symbol lookup
3. /top-movers -> SQL analytics query

Intentially using a transitional architecture to udnerstand the different types of system thinking.