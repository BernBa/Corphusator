# Corphusator
Corphusator turns .csv-files of the lexical database CorPH (http://chronhib.maynoothuniversity.ie) into tagged .txt-files.

The input file needs to contain the following columns: ID_unique_number, Textual_Unit_ID (the identifier for every textual unit, e.g., a single sentence of a text or a gloss), Morph, Analysis, Part_Of_Speech, Lemma. Similar to the Mutator, the .csv-file is turned into to a Pandas dataframe. The next step is the deletion of every token which has “particle_preverb” as its part of speech (except the empty particle “no·”) to avoid the mentioned redundancies. Furthermore, a set of rules for editorial practices are applied.
