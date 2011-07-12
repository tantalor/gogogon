Gogogon
=======

**Gogogon** is system for consuming the [1.USA.Gov click feed](http://bitly.measuredvoice.com/usa.gov) 
and generating daily rankings of 1.USA.Gov URLs.

The origin of *gogogon* is a todder's pronunciation of "octagon".

Output
======

Gogogon produces daily JSON and CSV files aggregated by the global hash.

The JSON file is an array of objects, one object for each short link. The structure of the objects is,

 * **u**: URL
 * **title**: page title
 * **global_clicks**: daily click count
 * **agency**: *e.g.*, nasa.gov
 * **global_hash**: bit.ly global hash

[JSON sample output](https://gist.github.com/1068435)

The CSV file has the same content in comma-separated values. The structure is, 

> Long URL,Page Title,Clicks,Agency Domain,Global hash

[CSV sample output](https://gist.github.com/1068436)

Processes
=========

 * `consumer.py` continuously reads the feed and writes daily logs of all clicks
 * `ranks.py` daily reads the previous day's log file and generates the output files

Licence
=======

(The MIT License)

Copyright © 2011 Captura Group

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the ‘Software’), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED ‘AS IS’, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
