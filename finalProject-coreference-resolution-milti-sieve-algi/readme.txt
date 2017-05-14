Coreference resolution is one of the most promising areas of NLP research today. It involves identifying each mention of a noun phrase that refer to the same real world entity, to the same cluster.
For our system architecture, we implement a multi-pass sieve which is made up of 5 passes. Each of the passes are arranged in order of decreasing precision, such that the highest precision sieve is matched first, and lower precision sieves later on. This helps us maintain the precision of the entire as a whole, and not let the lower precision features modify the result.

The 5 sieves implemented are:
* Pass 1 – Exact Match
* Pass 2 – Precise Constructs - Appositives, Acronyms
* Pass 3 – Strict Head Matching
* Pass 4 – Lexical Matching
* Pass 5 – Pronoun Matching

Instructions to Run the Code:

python main <list file of input> <list of female proper nouns> <list of male proper nouns> <sieve_count>
Eg. python main test1.listfile female.txt male.txt 5

To run the scorer individually:
python corefscorer  <list of response files to be evaluated> <location of directory of (golden truth) key files> <-V (optional) for Verbose>

python corefscorer responselist.txt ../dev -V
