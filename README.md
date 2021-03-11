# Corphusator

Due to the detailed lemmatisation down to the level of preverbs and particles, the transformation of the tokens of the lexical database CorPH (http://chronhib.maynoothuniversity.ie)) into continuous text is not straightforward.

Corphusator is a Python3-based programme which enables the users to get fully tagged continuous .txt-files. The following tags are available:

      1) POS
      2) morphological
      3) both

# Requirements:

Make sure that the following Python-packages are installed:

    - pandas
    - pathlib
    - tqdm

# Folder structure:
Please create a folder for the Corphusator including the subfolders "Corphusated" and "CorphExports". The latter needs to host the input file(s) and
the output(s) will be stored in the former.

# The input file:
Export a .csv-file from CorPH (see the documentation on the website) including including the columns below and store it in the folder "CorphExports":

  From MORPHOLOGY:
  
    - ID
    - Text_Unit_ID
    - Morph
    - Analysis
    - Lemma
  From LEMMATA:
  
    - Part_Of_Speech
    - Lang
  From SENTENCES:
  
    - Textual_Unit

# Running the Corphusator:
When initialised the programme asks you to put in the filename of input file (without the extension .csv). It then asks for input whether or not the
Textual Units should be presented in the output file (y or n). After this a bar will show you the progress and spent/estimated time. The morphs are now
treated according to a a list of possible combinations for morphs, which are broken down to either two, three, four or five constituents.
In some cases further user input is necessary, e.g., if there are problems with raised dots in a verbal complex. The programme will guide you through the
necessary steps.

After completion the user is asked to enter

  1) for POS-tags only
  2) for morphological tags only
  3) for both tags

The output files will be named according to your decisions, e.g., "7_Corphusated_POS.txt" for an input file with the name "7" and POS-tags.
If the option including the Textual Units is chosen "TU" is added to the filename, e.g., "7_Corphusated_TU" for a file including the Textual Units and both available tags.

# Representation of the tags:
Where available each morphs is assigned a POS-tag and a morphological tag (the latter is only available for Irish morphs). See the CorPH-website for the tag-sets.
The following separators are used to divide the morphs from the tags and the tags from each other:

  "/" for POS
  "|" for morphological

For instance, the third singular present indicative of the Old Irish copula is therefore
represented as follows: "is/verb|3sg.pres.ind."

The tagged text for every Textual Unit is concluded with a linebreak (\n). If the Textual Units themselves are also represented a second linebreak is
added after the tagged text:

  "Textual Unit 1
  Tagged Textual Unit 1

  Textual Unit 2
  Tagged Textual Unit 2"

