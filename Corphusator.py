#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 11:10:21 2021

@author: bernhardbauer
"""

import pandas as pd
import re
from pathlib import Path
from tqdm import tqdm

# =============================================================================
#  the csv.file needs to be in the folder "CorphExports"
#  and has to contain the following columns: 
#  ID, Text_Unit_ID, Morph, Analysis, Part_Of_Speech, Lemma, Textual_Unit, Lang
#  open the csv-file as pandas dataframe
#  always check that the file is in utf-8
#
#  For the output file please create a folder "Corphusated"
#   
# =============================================================================
# select MORPHOLOGY.ID, MORPHOLOGY.Text_Unit_ID, MORPHOLOGY.Morph, MORPHOLOGY.Analysis, LEMMATA.Part_Of_Speech, LEMMATA.Lemma, SENTENCES.Textual_Unit, LEMMATA.Lang, substring(MORPHOLOGY.Text_Unit_ID from 7) as Ord
# from MORPHOLOGY
# inner join LEMMATA on MORPHOLOGY.Lemma = LEMMATA.Lemma
# inner join SENTENCES on MORPHOLOGY.Text_Unit_ID = SENTENCES.Text_Unit_ID
# where MORPHOLOGY.Text_ID = "0006"
# order by Ord + 0, MORPHOLOGY.Sort_ID 

filename = input("Please input the name of the input file (without .csv): ")
inputfile = Path("CorphExports/" + filename + ".csv")
input_name = str(inputfile)
outputname = str(input_name[-6:-4]) + "_Corphusated.txt"
df = pd.read_csv(inputfile, encoding="utf-8", na_filter=False)

# =============================================================================
# Checks for empty analyses
# =============================================================================y

# a list of all the TUs in the file
ID = list(df.Text_Unit_ID.unique())

# =============================================================================
#  Deletes all the preverbs from the dataframe, but the dummy-particle is kept
#  also deletes ' in the Morphs to avoid issues
# =============================================================================

dummy = df.loc[df["Morph"] == "no"] + df.loc[df["Morph"] == "nu"] + df.loc[df["Morph"] == "no·"] + df.loc[df["Morph"] == "nu·"]
leavelist = list(dummy.index)
delete = df.loc[df["Part_Of_Speech"] == "particle_preverb"]
dellist = list(delete.index)

for l in leavelist:
    if l in dellist:
        dellist.remove(l)

df = df[~df.index.isin(dellist)]
df["Morph"] = df["Morph"].str.replace("'", "")

# =============================================================================
# Changes the POS for the copula
# =============================================================================

df.loc[(df.Lemma == "is 1"), "Part_Of_Speech"] = "copula"

# =============================================================================
# Gets a list of ma and cia
# =============================================================================

ma = (df.loc[df["Lemma"] == "ma"]).index
cia1 = (df.loc[df["Lemma"] == "cía 1"]).index
cia2 = (df.loc[df["Lemma"] == "cía 2"]).index
cenm = (df.loc[df["Lemma"] == "cenmothá 2"]).index
amal = (df.loc[df["Lemma"] == "amail 2"]).index
ar = (df.loc[df["Lemma"] == "ar 2"]).index
conjlist = list(list(ma) + list(cia2) + list(cia1) + list(cenm) + list(amal) + list(ar))
conlist = []
for c in conjlist:
    con = df.ID[c]
    conlist.append(con)

co3 = (df.loc[df["Lemma"] == "co 3"]).index
colist = list(co3)
co3list = []
for co in colist:
    c3 = df.ID[co]
    co3list.append(c3)    
    


# =============================================================================
# Lists of combinations and defined lists
# =============================================================================
doublelist = ["adjective+particle_anaphoric", "adjective+particle_demonstrative_distal",
              "adjective+particle_demonstrative_proximate", "adjective+particle_pronominal",
              "complementiser+verb", "complementiser+copula",
              "conjunction+copula", "conjunction+verb", 
              "copula+particle_relative",
              "compound_noun+particle_demonstrative_proximate", "compound_verbal_noun+particle_demonstrative_proximate",
              "compound_noun+particle_demonstrative_distal", "compound_verbal_noun+particle_demonstrative_distal",
              "compound_adjective+particle_demonstrative_proximate", "compound_adjective+particle_demonstrative_distal", 
              "particle_augment+verb", "particle_augment+copula",
              "particle_interrogative+verb", "particle_interrogative+copula",
              "particle_negative_main+verb", "particle_negative_main+copula",
              "particle_negative_subordinate+verb", "particle_negative_subordinate+copula",
              "particle_preverb+verb", "particle_preverb+copula", 
              "particle_relative+verb", "particle_relative+copula",
              "pronoun_infixed+verb","pronoun_interrogative+verb","pronoun_relative+verb",
              "pronoun_interrogative+copula",
              "pronoun_independent+particle_anaphoric",
              "verb+particle_pronominal", "copula+particle_pronominal",
              "verb+particle_anaphoric", "copula+particle_anaphoric",
              "noun+particle_anaphoric", "noun+particle_pronominal",
              "noun+particle_demonstrative_distal", "noun+particle_demonstrative_proximate",
              "particle_prefix+noun", "particle_prefix+adjective", "particle_prefix+verbal_noun",
              "preposition+definite_article", "preposition+particle_pronominal", 
              "preposition+pronoun_possessive", "preposition+verb",
              "preposition+verb", "preposition+particle_pronominal",
              "pronoun_independent+particle_pronominal",
              "verbal_noun+particle_anaphoric", "verbal_noun+particle_pronominal",
              "verbal_noun+particle_demonstrative_distal", "verbal_noun+particle_demonstrative_proximate",
              # "verb+particle_relative", 
              "verb+particle_anaphoric", 
              "verbal_participle+particle_anaphoric"]
triplelist = ["complementiser+particle_augment+verb", "complementiser+particle_augment+copula", 
              "complementiser+particle_negative_main+verb", "complementiser+particle_negative_main+copula",
              "complementiser+particle_negative_subordinate+verb", "complementiser+particle_negative_subordinate+copula",
              "complementiser+pronoun_infixed+verb", "complementiser+pronoun_infixed+copula",
              "complementiser+verb+particle_pronominal", "complementiser+copula+particle_pronominal",
              "definite_article+verb+particle_pronominal",
              "particle_augment+pronoun_relative+verb", "particle_augment+pronoun_relative+copula",
              "particle_augment+pronoun_infixed+verb", "particle_augment+pronoun_infixed+copula",
              "particle_augment+particle_relative+verb", "particle_augment+particle_relative+copula",
              "particle_augment+particle_augment+verb", "particle_augment+particle_augment+copula",
              "particle_augment+verb+particle_anaphoric", "particle_augment+copula+particle_anaphoric",
              "particle_augment+verb+particle_pronominal",
              "particle_preverb+pronoun_infixed+verb", "particle_preverb+pronoun_infixed+copula",
              "particle_preverb+particle_relative+verb", "particle_preverb+particle_relative+copula",
              "particle_preverb+verb+particle_anaphoric", "particle_preverb+copula+particle_anaphoric",
              "particle_relative+verb+particle_pronominal",
              "particle_prefix+preposition+adverb", "particle_prefix+verbal_noun+particle_anaphoric",
              "particle_interrogative+verb+particle_pronominal",
              "particle_negative_main+verb+particle_pronominal", "particle_negative_main+copula+particle_pronominal",
              "particle_negative_main+verb+particle_anaphoric",
              "particle_negative_main+particle_augment+verb", "particle_negative_main+particle_augment+copula",
              "particle_negative_main+pronoun_infixed+verb", "particle_negative_main+pronoun_infixed+copula",
              "particle_negative_subordinate+particle_augment+verb", "particle_negative_subordinate+particle_augment+copula",
              "particle_negative_subordinate+pronoun_infixed+verb",  "particle_negative_subordinate+pronoun_infixed+copula",
              "particle_negative_subordinate+pronoun_relative+verb", "particle_negative_subordinate+pronoun_relative+copula",
              "particle_negative_subordinate+particle_relative+verb", "particle_negative_subordinate+particle_relative+copula",
              "particle_negative_subordinate+verb+particle_pronominal",
              "particle_relative+particle_augment+verb", "particle_relative+particle_augment+copula",
              "particle_relative+verb+particle_anaphoric",
              "preposition+pronoun_relative+verb", "preposition+pronoun_relative+copula",
              "preposition+particle_augment+verb", "preposition+particle_augment+copula",
              "preposition+pronoun_infixed+verb", "preposition+pronoun_infixed+copula",
              "pronoun_infixed+particle_augment+verb","pronoun_infixed+particle_augment+copula",
              "pronoun_infixed+particle_relative+verb", "pronoun_infixed+particle_preverb+verb",
              "pronoun_infixed+verb+particle_pronominal",
              "pronoun_interrogative+verb",
              "pronoun_relative+verb+particle_pronominal"]
quartlist = ["complementiser+particle_negative_subordinate+particle_augment+verb",
             "complementiser+particle_negative_subordinate+particle_augment+copula",
            "conjunction+particle_relative+verb+particle_comparative",
            "conjunction+particle_negative_main+pronoun_infixed+verb",
            "particle_augment+particle_relative+pronoun_infixed+verb",
            "particle_augment+particle_relative+pronoun_infixed+copula",
            "particle_augment+pronoun_infixed+verb+particle_pronominal",
            "particle_interrogative+particle_negative_subordinate+particle_relative+verb",
            "particle_interrogative+particle_augment+verb+particle_pronominal",
            "particle_interrogative+particle_augment+verb+particle_anaphoric",
            "particle_negative_main+pronoun_infixed+verb+particle_pronominal",
            "particle_negative_main+particle_augment+verb+particle_pronominal",
            "particle_negative_main+pronoun_infixed+particle_augment+verb",
            "particle_negative_main+pronoun_infixed+verb+particle_anaphoric",
            "particle_negative_subordinate+particle_relative+particle_augment+verb",
            "particle_negative_subordinate+particle_relative+particle_augment+copula",
            "particle_negative_subordinate+particle_relative+pronoun_infixed+verb",
            "particle_negative_subordinate+particle_relative+verb+particle_pronominal",
            "particle_negative_subordinate+particle_augment+verb+particle_pronominal",
            "particle_preverb+conjunction+verb+particle_pronominal",
            "particle_preverb+pronoun_infixed+verb+particle_pronominal",
            "particle_preverb+pronoun_infixed+particle_relative+verb",
            "particle_relative+pronoun_infixed+particle_augment+verb",
            "particle_relative+pronoun_infixed+particle_augment+copula",
            "particle_relative+particle_augment+verb+particle_pronominal",
            "particle_relative+pronoun_infixed+verb+particle_pronominal",
            "preposition+pronoun_relative+particle_augment+verb",
            "preposition+pronoun_relative+particle_augment+copula",
            "preposition+pronoun_relative+pronoun_infixed+verb",
            "preposition+pronoun_relative+pronoun_infixed+copula",
            "preposition+pronoun_relative+particle_negative_subordinate+copula",
            "pronoun_infixed+particle_relative+particle_augment+verb",
            "pronoun_infixed+particle_augment+verb+particle_pronominal",
            "pronoun_infixed+particle_augment+verb+particle_anaphoric",
            "pronoun_relative+pronoun_infixed+particle_augment+verb"]
quintlist = ["complementiser+pronoun_infixed+verb+particle_pronominal+particle_anaphoric",
             "particle_augment+pronoun_infixed+particle_relative+verb+particle_pronominal",
             "particle_negative_main+pronoun_infixed+particle_augment+verb+particle_pronominal",
             "particle_negative_main+pronoun_infixed+particle_augment+copula+particle_pronominal"]

poslist = []
allout = []
finaloutput = []
p = 0

# =============================================================================
# Representation of verbal complexes
# =============================================================================

# conjunction/interrogative/complementiser
# negative
# verb
# augment
# relative
# preposition
# infixes
# notae augentes

# =============================================================================
# Defines the functions
# =============================================================================

def update_combined(combined):
    if '∅N' in combined:
        combined = combined.replace('∅N', '')
    if '∅L' in combined:
        combined = combined.replace('∅L', '')
    if '∅' in combined:
        combined = combined.replace('∅', '')
    if 'particle_preverb' in combined:
        combined = combined.replace('+particle_preverb', '')
    if '··' in combined:
        combined = combined.replace('··', '·')
    return combined

def update_finaloutput(finaloutput):
    finaloutput = str(finaloutput)
    finaloutput = finaloutput.replace("'", "")
    finaloutput = finaloutput.replace(",", "")
    finaloutput = finaloutput.replace("$", "")
    finaloutput = finaloutput.replace("öäü", " \n")
    finaloutput = finaloutput.replace("üäö", " \n\n")
    finaloutput = finaloutput.replace("[", "")
    finaloutput = finaloutput.replace("]", "")
    finaloutput = finaloutput.replace("∅", "")
    finaloutput = finaloutput.replace("++", "+")
    finaloutput = finaloutput.replace("+ ", " ")
    finaloutput = finaloutput.replace("|+", "|")
    finaloutput = finaloutput.replace("··", "·")
    finaloutput = finaloutput.replace("@Latin", "")
    return finaloutput

def update_dots(combined):
    dotcount = combined.count("·")

    if dotcount > 1:
        # print(combined)
        lenuntildot = len(combined.partition("·")[0])
        lenbtwdots = len(combined.split("·")[1])
        lentosedot = lenuntildot + lenbtwdots + 2
        btwdots = combined.split("·")[1]
        beforedot = combined[:lenuntildot]
    
        if combined.startswith('·') is True:
            deletemorph = len(it)
            newcombi = (combined.partition("/")[0])[deletemorph:]
        elif lenbtwdots == 1:
            combi = (combined[:lenuntildot] + combined[(lentosedot-1):])
            newcombi = combi.partition("/")[0]
        elif combined[:lenuntildot] == combined.split("·")[1] or beforedot == combined[lentosedot:(lentosedot+lenuntildot)] or beforedot == combined[((lentosedot-lenuntildot)-1):lentosedot-1]:
            combi = combined.partition("·")[2]
            newcombi = combi.partition("/")[0]
        elif btwdots == ((combined.split("·")[2])[:len(btwdots)]):
            combi = combined.partition("·")[0] + "·" + ((combined.partition("·")[2])[len(btwdots):])
            newcombi = combi.partition("/")[0]
        elif combined[:lenuntildot] == combined[((lentosedot+1)-lenuntildot):(lentosedot+1)]:
            combi = combined[(lenuntildot+1):]
            newcombi = combi.partition("/")[0]
        elif btwdots == combined[(lenuntildot-len(btwdots)):lenuntildot]:
            combi = (combined[:((lenuntildot-len(btwdots)))] + combined[(lentosedot-1):])
            newcombi = combi.partition("/")[0]
        else:
            print("\n" + "We have a dot-problem: " + combined.partition("/")[0])
            newcombi = input("What should we have? ")
        combinedanalysis = combined.partition("/")[2]
        combined = newcombi + "/" + combinedanalysis  
    return combined

def update_allout(allout, whichone):
    for out in allout:
        one = str(out)
        split = one.split( )
        for token in split:
            if whichone == "1":
                token = (token.partition("|")[0] + token.partition("$")[2])
            else:
                token = (token.partition("/")[0] + "/" + token.partition("|")[2])
            finaloutput.append(token) 
    return allout
   

# =============================================================================
# The fun starts here
# =============================================================================

tuornot = input("Do you want to display the TUs in the outputfile? (y/n) ")

for I in tqdm(ID):

    pos = ID[p] # check this!
    subframe = df[df.Text_Unit_ID == ID[p]]   
    index = subframe["ID"]
    pos = subframe["Part_Of_Speech"]
    morph = subframe["Morph"]
    an = subframe["Analysis"]
    Lang = subframe["Lang"]
    
    # Further lists and variables
    adding = morph + "/" + pos + "Ö" + an + "@" + Lang
    poslist = adding.tolist()
    posis = len(poslist)
    n = 0
    newpos = [] 
    for morph in poslist:
        
        
        # print(n, morph)
        # Breaks the loop if n is the length of the poslist
        if n >= posis:
            break      
        # print(poslist[n])
        # if "@Latin" in morph:
        #     item = morph
        
# =============================================================================
#         Definitions
# =============================================================================
        
        # Defines the items, nexts, etc.

        item = subframe["Morph"].iloc[n] + "/" + subframe["Part_Of_Speech"].iloc[n] + "Ö" + subframe["Analysis"].iloc[n]
        itemID = subframe["ID"].iloc[n]
        
        if "@Latin" in poslist[n]:
            item = poslist[n]
        
        # print(morph, item)

        if n+1 < posis:
            nxt = subframe["Morph"].iloc[n+1] + "/" + subframe["Part_Of_Speech"].iloc[n+1] + "Ö" + subframe["Analysis"].iloc[n+1]
        else:
            nxt = None

        if n+2 < posis:
            secnxt = subframe["Morph"].iloc[n+2] + "/" + subframe["Part_Of_Speech"].iloc[n+2] + "Ö" + subframe["Analysis"].iloc[n+2]
        else:
            secnxt = None
        if n+3 < posis:
            thinxt = subframe["Morph"].iloc[n+3] + "/" + subframe["Part_Of_Speech"].iloc[n+3] + "Ö" + subframe["Analysis"].iloc[n+3]
        else:
            thinxt = None
        if n+4 < posis:
            founxt = subframe["Morph"].iloc[n+4] + "/" + subframe["Part_Of_Speech"].iloc[n+4] + "Ö" + subframe["Analysis"].iloc[n+4]
        else:
            founxt = None

        # More variables, regular expressions
        delimiters = "/", "Ö"
        regexPattern = "|".join(map(re.escape, delimiters))
                       
        it = item.partition("/")[0]
        itpos = re.split(regexPattern, item)[1]
        itan = re.split(regexPattern, item)[2]

        if nxt is not None:
            ne = nxt.partition("/")[0]
            nepos = re.split(regexPattern, nxt)[1]
            nean = re.split(regexPattern, nxt)[2]
           
        if secnxt is not None:
            se = secnxt.partition("/")[0]
            sepos = re.split(regexPattern, secnxt)[1]
            sean = re.split(regexPattern, secnxt)[2]
            
        if thinxt is not None:
            th = thinxt.partition("/")[0]
            thpos = re.split(regexPattern, thinxt)[1]
            than = re.split(regexPattern, thinxt)[2]

        if founxt is not None:
            fo = founxt.partition("/")[0]
            fopos = re.split(regexPattern, founxt)[1]
            foan = re.split(regexPattern, founxt)[2]
 
        # Defines the combinations
        if nxt is None:
            itemnext = None
            itemnextsec = None
            itemnextsecthi = None
            itemnextsecthifou = None
        # elif "@Latin" in item:
        #     item = item.partition("@")[0]
        #     pass
        else:
            try:
                nepos
            except NameError:
                pass
            else:
                itemnext = itpos + "+" + nepos
                try:
                    sepos
                except NameError:
                    pass
                else:
                    itemnextsec = itpos + "+" + nepos + "+" + sepos
                    try:
                        thpos
                    except NameError:
                        pass
                        pass
                    else:
                        itemnextsecthi = itpos + "+" + nepos + "+" + sepos + "+" + thpos
                        try:
                            fopos
                        except NameError:
                            pass
                        else:
                            itemnextsecthifou = itpos + "+" + nepos + "+" + sepos + "+" + thpos + "+" + fopos

        # Combines those compounds which don't have a combined compound in the database
        if "compos." in item:
            if it + ne == se:
                try:
                    thpos
                except NameError:
                    combined = (se + "/compound_" + nepos + "|" + sean)
                    combined = update_combined(combined)
                    newpos.append(combined)
                    n += 3
                else:
                    if thpos in ("particle_demonstrative_distal", "particle_demonstrative_proximate", "particle_anaphoric"):
                        combined = (se + "-" + th + "/compound_" + nepos + "+" + thpos + "|" + sean + "+" + than)
                        n += 4

            else:
                if it == ne[:len(it)]:
                    it = ""
                if sepos in ("particle_demonstrative_distal", "particle_demonstrative_proximate", "particle_anaphoric"):
                    combined = (it + ne + "-" + se + "/compound_" + nepos + "+" + sepos + "|" + nean + "+" + sean)
                    combined = update_combined(combined)
                    newpos.append(combined)
                    n += 3   
                else:
                    combined = (it + ne + "/compound_" + nepos + "|" + nean)
                    combined = update_combined(combined)
                    newpos.append(combined)
                    n += 2
            
            continue
        
        # Conjugated prepositions get their own tag and a prevented from combining with other elements unless it's particle_pronominal
        if ("3" in item or "2" in item or "1" in item) and itpos == "preposition":
            if nepos == "particle_pronominal":
                if "-" in ne:
                    ne = ne.replace('-', '')
                combined = (it + "-" + ne + "/" + itpos + "_pronoun" + "+" + nepos + "|" + itan)
                n += 1
            else:
                combined = (it + "/" + itpos + "_pronoun" + "|" + itan)
            newpos.append(combined)
            n += 1
            continue
        
        # Con·rici exception
        if "con·rici" in item:
            newpos.append(item)
            n += 1
            continue
        
        # exception for co 3
        if itemID in co3list:
            newpos.append(item)
            n += 1
            continue
        
        # exception for in·daas
        if ("in·" and "definite_article") in item and nepos == "verb":
            if "@Latin" in poslist[n+1]:
                pass
            else:
                combined = ("in" + ne + "/" + itpos + "+" + nepos + "|" + itan + "+" + nean)
                newpos.append(combined)
                n += 2
                continue
        # exception for iarsindi
        if (it == "iar" or "íar") and ne == "sind" and se in ("í", "i"):
            n += 3
            continue
        
        if it == "ar" and ne == "ind" and se in ("í", "i"):
            n += 3
            continue
        
# =============================================================================
# Looks for combinations
# =============================================================================

        # Looks for morphs that start with "·"
        wild = re.search("^·", it)
        try:
            ne
        except NameError:
            pass
        else:
            wildne = re.search("^·", ne)
        
        if "@Latin" in poslist[n]:
            itemnextsecthifou = None
            itemnextsecthi = None
            itemnextsec = None
            itemnext = None

            
            

# =============================================================================
#         # Combination of five
# =============================================================================
        try:
            itemnextsecthifou
        except NameError:
            pass
        else:
            if itemnextsecthifou in quintlist:
                if "@Latin" in poslist[n]:
                    continue

                if itpos == "conjunction" and fopos == "particle_pronominal":
                    combined = (it + ne + se + th + "-" + fo + "/" + itpos + "+" + nepos + "+" + thpos + "+" + sepos + "+" + fopos + "|" + than)
                
                elif itpos == "particle_augment" and fopos == "particle_pronominal":
                    combined = (th + "-" + fo + "/" + thpos + "+" + itpos + "+" + sepos + "+" + nepos + "+" + fopos + "|" + than + "+" + nean + "+" + foan)
                
                elif thpos == "particle_pronominal" and fopos == "particle_anaphoric":
                    combined = (se + "-" + th + "-" + fo + "/" + itpos + "+" + sepos + "+" + nepos + "+" + thpos + "+" + fopos + "|" + sean + "+" + nean + "+" + than)
                
                else:
                    combined = (it + ne + se + th + fo + "/" + itpos + "+" + thpos + "+" + nepos + "+" + sepos + "+" + fopos + "|" + than)
                combined = update_combined(combined)
                newpos.append(combined)
                n += 3
                item = 0
                nxt = 0
                secnxt = 0
                thinxt = 0
                founxt = 0
                
                if itemnextsecthi in quartlist:
                    itemnextsecthi = None
                if itemnextsec in triplelist:
                    itemnextsec = None
                if itemnext in doublelist:
                    itemnext = None

        
        
# =============================================================================
#         # Combination of four
# =============================================================================
        try:
            itemnextsecthi
        except NameError:
            pass
        else:

            if itemnextsecthi in quartlist:
                if "@Latin" in poslist[n]:
                    continue

                if itpos == "preposition":
                    if nepos == "pronoun_relative" and sepos == "pronoun_infixed":
                        combined = (it + ne + se + th + "/" + thpos + "+" + itpos + "+" + nepos + "+" + sepos + "|" + than)
                    elif nepos == "pronoun_relative" and sepos == "particle_negative_subordinate":
                        combined = (it + ne + se +th + "/" + sepos + "+" + thpos + "+" + nepos + "+" + itpos + "|" + than + "+" + itan)
                    elif nepos == "pronoun_relative" and sepos == "particle_augment":
                        combined = (it + ne + th + "/" + thpos + "+" + sepos + "+" + nepos + "+" + itpos + "|" + than + "+" + itan)
                
                
                elif itpos == "conjunction" and nepos == "particle_negative_main" and sepos == "pronoun_infixed":
                    combined = (it + ne + se + th + "/" + itpos + "+" + nepos + "+" + thpos + "+" + sepos + "|" + than + "+" + sean)
                
                elif itpos == "particle_interrogative":
                    if nepos == "particle_negative_subordinate" and sepos == "particle_relative":
                        combined = (it + ne + se + th + "/" + itpos + "+" + nepos + "+" + thpos + "+" + sepos + "|" + than)
                    elif nepos == "particle_augment":
                        if thpos == "particle_pronominal":
                            combined = (it + se + "-" + th + "/" + itpos + "+" + sepos + "+" + nepos + "+" + sepos + "+" + thpos + "|" + sean + "+" + than)             
                
                elif itpos == "particle_relative":
                    if nepos == "particle_augment" and thpos == "particle_pronominal":
                        combined = (it + ne + se + "-" + th + "/" + sepos + "+" + nepos + "+" + itpos + "+" + thpos + "|" + sean + "+" + than)
                    if nepos == "pronoun_infixed" and thpos == "particle_pronominal":
                        combined = (se + "-" + th + "/" + sepos + "+" + nepos + "+" + itpos + "+" + thpos + "|" + sean + "+" + than)
                
                elif itpos == "particle_preverb":
                    if nepos == "pronoun_infixed" and sepos == "particle_relative":
                        combined = (th + "/" + thpos + "+" + sepos + "+" + nepos + "|" + than + "+" + nean)
                    elif nepos == "conjunction" and sepos == "verb":
                        combined = (se + "-" + th + "/" + nepos + "+" + sepos + "+" + thpos + "|" + sean + "+" + than)
                                    
                elif "negative" in itpos:
                    if nepos == "particle_relative":
                        if sepos == "pronoun_infixed":
                            combined = (it + se + th + "/" + itpos + "+" + thpos + "+" + nepos + "+" + sepos + "|" + than + "+" + sean)
                        elif sepos == "particle_augment":
                            combined = (it + se + th + "/" + itpos + "+" + thpos + "+" + sepos + "+" + nepos + "|" + itan + "+" + than)
                        elif thpos == "particle_pronominal":
                            combined = (it + se + "-" + th + "/" + itpos + "+" + sepos + "+" + nepos + "+" + thpos + "|" + sean + "+" + than)
                    elif itpos == "particle_negative_subordinate" and thpos == "particle_pronominal":
                        combined = (it + se + "-" + th + "/" + itpos + "+" + sepos + "+" + nepos + "+" + thpos + "|" + sean + "+" + than)
                    elif sepos == "pronoun_infixed" and (thpos == "particle_pronominal" or thpos == "particle_anaphoric"):
                        combined = (it + ne + se + "-" + th + "/" + itpos + "+" + sepos + "+" + nepos + "+" + thpos + "|" + sean + "+" + nean + "+" + than)
                    elif nepos == "pronoun_infixed":
                        if (thpos == "particle_pronominal" or thpos == "particle_anaphoric"):
                            combined = (it + ne + se + "-" + th + "/" + itpos + "+" + sepos + "+" + nepos + "+" + thpos + "|" + sean + "+" + nean + "+" + than)
                        elif sepos == "particle_augment":
                            combined = (it + ne + se + th + "/" + itpos + "+" + thpos + "+" + sepos + "+" + nepos + "|" + itan + "+" + than + "+" + sean + "+" + nean)
                
                elif itpos == "particle_augment":
                    if nepos == "pronoun_infixed" and thpos == "particle_pronominal":
                        combined = (it + ne + se + "-" + th + "/" + sepos + "+" + itpos + "+" + nepos + "+" + thpos + "|" + sean + "+" + nean + "+" + than)
                    elif nepos == "particle_relative" and sepos == "pronoun_infixed":
                        combined = (th + "/" + thpos + "+" + itpos + "+" + nepos + "+" + sepos + "|" + than + "+" + sean)
                
                elif itpos == "pronoun_infixed":
                    if nepos == "particle_relative" and sepos == "particle_augment":
                        combined = (th + "/" + thpos + "+" + sepos + "+" + nepos + "+" + itpos + "|" + than + "+" + itan)
                    elif nepos == "particle_augment" and thpos in ("particle_pronominal", "particle_anaphoric"):
                        combined = (se + "-" + th + "/" + sepos + "+" + nepos + "+" + itpos + "+" + thpos + "|" + sean + "+" + than + "+" + itan)
                    elif nepos == "particle_augment" and thpos == "particle_pronominal":
                        combined = (se + "-" + th + "/" + sepos + "+" + nepos + "+" + itpos + "+" + thpos + "|" + sean + "+" + itan + "+" + than)
                
                elif thpos == "particle_comparative":
                    combined = (th + "/" + thpos + "|" + than)
                    
                elif itpos == "particle_preverb" and nepos == "pronoun_infixed" and thpos == "particle_pronominal":
                    combined = (se + "-" + th + "/" + sepos + "+" + nepos + "+" + thpos + "|" + sean + "+" + nean + "+" + than)
                
                elif itpos == "pronoun_relative":
                    if nepos == "pronoun_infixed":
                        combined = (it + ne + th + "/" + thpos + "+" + itpos + "+" + nepos + "|" + than + "+" + itan + "+" + nean)
                
                elif ne[:1] or se[:1] in th[:1]: 
                    if ne[:1] in th[:1]:
                        combined = (it + se + th + "/" + thpos + "+" + itpos + "+" + nepos + "+" + sepos + "|" + than)
                    else:
                        combined = (it + ne + th + "/" + thpos + "+" + itpos + "+" + nepos + "+" + sepos + "|" + than)
                
                else:
                    combined = (it + ne + se + th + "/" + thpos + "+" + itpos + "+" + nepos + "+" + sepos + "|" + than)
                
                combined = update_combined(combined)
                combined = update_dots(combined)
                n += 2

                # dotcount = combined.count("·")
                # if dotcount > 1:
                #     if '··' in combined:
                #         combined = combined.replace('··', '·')
                #     else:
                #         lenuntildot = len(combined.partition("·")[0])
                #         lenbtwdots = len(combined.split("·")[1])
                #         lentosedot = (len(combined.partition("·")[0]) + lenbtwdots)
                #         btwdots = (combined[(lentosedot-1):((lentosedot+lenbtwdots)-1)])

                #         if combined.startswith('·') is True:
                #             deletemorph = len(ne)
                #             newcombi = (combined.partition("/")[0])[deletemorph:]
                #         elif combined[:lenuntildot] == combined.split("·")[1]:
                #             combi = combined.partition("·")[2]
                #             newcombi = combi.partition("/")[0]
                #         elif combined.split("·")[1] == btwdots or len(btwdots) == 1:
                #             combi = (combined[:lenuntildot] + combined[(lentosedot+1):])
                #             newcombi = combi.partition("/")[0]
                #         elif combined[:lenuntildot] == combined[((lentosedot+1)-lenuntildot):(lentosedot+1)]:
                #             combi = combined[(lenuntildot+1):]
                #             newcombi = combi.partition("/")[0]
                #         else:
                #             print(combined.split("·")[1])
                #             print("\n" + "We have a dot-problem: " + combined.partition("/")[0])
                #             newcombi = input("What should we have? ")
                #         combinedanalysis = combined.partition("/")[2]
                #         combined = newcombi + "/" + combinedanalysis
                
                newpos.append(combined)
                item = 0
                nxt = 0
                secnxt = 0
                thinxt = 0

                if itemnextsec in triplelist:
                    itemnextsec = None
                if itemnext in doublelist:
                    itemnext = None

                
# =============================================================================
#         # Combination of three
# =============================================================================
        try:
            itemnextsec
        except NameError:
            pass
        else:
            if itemnextsec in triplelist:
                if "@Latin" in poslist[n]:
                    continue
                
                if sepos == "particle_pronominal" and "negative" not in itpos:
                    if itpos == "particle_interrogative":
                        combined = (it + ne + "-" + se + "/" + itpos + "+" + nepos + "+" + sepos + "|" + nean + "+" + sean)            
                    if itpos == "particle_augment" and "·" not in it:
                        combined = (ne + "-" + se + "/" + itpos + "+" + nepos + "+" + sepos + "|" + nean + "+" + sean)
                    else:
                        combined = (it + ne + "-" + se + "/" + nepos + "+" + itpos + "+" + sepos + "|" + nean + "+" + sean)

                elif (se == "suas" or se == "súas"):
                    combined = (se + "/" + sepos + "|" + sean)
                    
                elif "negative" in itpos:
                    if "relative" in nepos:
                        combined = (it + ne + se + "/" + itpos + "+" + sepos + "+" + nepos + "|" + sean)
                    elif sepos in ("particle_pronominal", "particle_anaphoric"):
                        combined = (it + ne + "-" + se + "/" + itpos + "+" + nepos + "+" + sepos + "|" + nean + "+" + sean)            
                    elif "pronoun" in nepos:
                        combined = (it + ne + se + "/" + itpos + "+" + sepos + "+" + nepos + "|" + sean + "+" + nean)
                    elif "·" in it and "·" in se:
                        combined = (it + se + "/" + itpos + "+" + nepos + "+" + sepos + "|" + sean)                  
                    else:
                        combined = (it + ne + se + "/" + itpos + "+" + nepos + "+" + sepos + "|" + sean)
                
                elif itpos == "particle_preverb":
                    if it == "no" and sepos == "copula":
                        combined = (ne + se + "/" + sepos + "+" + nepos + "|" + sean + "|" + nean)
                    elif nepos == "pronoun_infixed":
                        combined = (it + ne + se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean + "+" + nean)
                    elif nepos == "particle_relative":
                        combined = (it + ne + se + "/" + sepos + "|" + sean)
                    elif sepos == "particle_anaphoric":
                        combined = (ne  + "-" + se + "/" + nepos + "+" + sepos + "|" + nean + "+" + sean)
                
                elif itpos == "particle_augment":
                    if nepos == "pronoun_relative":
                        combined = (it + ne + se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean)
                    elif nepos == "pronoun_infixed":
                        combined = (it + ne + se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean + "+" + nean)
                    elif nepos == "particle_augment":
                        combined = (it + ne + se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean)
                    elif sepos == "particle_anaphoric":
                        combined = (it + ne + "-" + se + "/" + nepos + "+" + sepos + "|" + sean)
                
                
                elif (it[:1] or ne[:1]) == se[:1]: 
                    if ne[:1] == se[:1]:
                        combined = (it + ne + se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean)
                    elif it[:1] == se[:1]:
                        combined = (se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean)
                    else:
                        combined = (it + se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean)
                                
                elif nepos == "verb" and sepos == "particle_anaphoric":
                    combined = (ne + "-" + se + "/" + nepos + "+" + itpos + "+" + sepos + "|" + nean)
                    
                elif itpos == "conjunction":
                    combined = (it)
                        
                elif itpos == "preposition":
                    if "infix" in nepos:
                        if wildne != None:
                            combined = (it + se + "/" + itpos + "+" + sepos +  "+" + nepos + "|" + sean)
                        else:    
                            combined = (it + ne + se + "/" + itpos + "+" + sepos +  "+" + nepos + "|" + sean)    
                    elif nepos == "particle_augment":
                        combined = (it + se + "/" + sepos + "+" + nepos + "+" + itpos + "|" + sean)               
                    elif nepos == "pronoun_relative":
                        combined = (it + ne + se + "/" + sepos + "+" + nepos + "+" + itpos + "|" + sean)
                    
                elif itpos == "particle_relative" and nepos == "particle_augment":
                    combined = (it + se + "/" + sepos + "+" + nepos + "+" + itpos + "|" + sean)
                    
                elif itpos == "pronoun_infixed":
                    if nepos == "particle_augment":
                        combined = (se + "/" + sepos + "+" + nepos + "+" + itpos + "|" + sean + "+" + itan)
                    elif nepos == "particle_relative":
                        combined = (se + "/" + sepos + "+" + nepos + "+" + itpos + "|" + sean + "+" + itan)
                
                elif itpos == "complementiser":
                    if nepos == "pronoun_infixed" and sepos == "verb":
                        combined = (it + ne + se + "/" + itpos + "+" + sepos + "+" + nepos + "|" + sean + "+" + nean)
                    elif nepos == "particle_augment" and sepos == "verb":
                        if len(ne) == 1 or ne == se[:3]:
                            combined = (it + se + "/" + itpos + "+" + sepos + "+" + nepos + "|" + sean)
                        else:
                            combined = (it + ne + se + "/" + itpos + "+" + sepos + "+" + nepos + "|" + sean)
                    elif (nepos == "particle_negative_main" or nepos == "particle_negative_subordinate") and (sepos == "verb" or sepos == "copula"):
                        combined = (it + ne + se + "/" + itpos + "+" + nepos + "+" + sepos + "|" + sean)
                    
                elif sepos == "particle_pronominal":
                    combined = (it + ne + "-" + se + "/" + itpos + "+" + nepos + "+" + sepos + "|" + nean + "+" + sean)
                
                else:
                    combined = (se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean)
                n += 1
                
                combined = update_combined(combined)
                combined = update_dots(combined)              
                    
                newpos.append(combined)
                item = 0
                nxt = 0
                secnxt = 0

                if itemnext in doublelist:
                    itemnext = None
            
# =============================================================================
#         # Combination of two  
# =============================================================================
                
        try:
            itemnext
        except NameError:
            pass
        else:
            if itemnext in doublelist:

                if "@Latin" in poslist[n]:
                    continue
                if nepos == "particle_pronominal" or nepos == "particle_anaphoric" or nepos == "particle_demonstrative_proximate":
                    if "-" in ne:
                        ne = ne.replace('-', '')
                    combined = (it + "-" + ne + "/" + itpos + "+" + nepos + "|" + itan + "+" + nean)
                
                elif it == "7":
                    newpos.append(item)
                    n += 1
                    item = 0
                    continue
                    
                elif it == "ol·" and nepos == "verb":
                    combined = (it + ne + "/" + itpos + "+" + nepos + "|" + nean)
                
                elif itpos == "pronoun_interrogative":
                    combined = (it + ne + "/" + itpos + "+" + nepos + "+" + itan + "+" + nean)
                
                elif "complementiser" in itpos or "negative" in itpos:
                    combined = (it + ne + "/" + itpos + "+" + nepos + "|" + nean)
                               
                elif itpos == "particle_augment":
                    if it in ne:
                        combined = (ne + "/" + nepos + "+" + itpos + "|" + nean)
                    else:
                        combined = (it + ne + "/" + nepos + "+" + itpos + "|" + nean)
                        
                elif itpos == "conjunction":
                    if itemID in conlist:
                        combined = (it + "/" + itpos + "|" + itan)
                        n -= 1
                    else:
                        combined = (it + ne + "/" + itpos + "+" + nepos + "|" + nean)
    
                elif itpos == "particle_preverb":
                    combined = (it + ne + "/" + nepos + "|" + nean)
                
                elif (nepos == "particle_augment" or nepos == "pronoun_infixed") and wild != None:
                    combined = (ne + "/" + nepos + "+" + itpos + "|" + nean)
    
                elif itpos == "preposition":
                    if nepos == "definite_article":
                        if it in ("cenmithá", "dochum", "dochumm"):
                            combined = (it + "/" + itpos + "|" + itan)
                            n -= 1
                        else:
                            combined = (it + ne + "/" + itpos + "+" + nepos + "|" + itan + "+" + nean)                
                    elif nepos == "verb":
                        if "·" in it:
                            combined = (it + ne + "/" + nepos + "+" + itpos + "|" + nean + "+" + itan)
                        else:
                            pass
                    elif nepos == "pronoun_possessive":
                        combined =(it + ne + "/" + itpos + "+" + nepos + "|" + itan)
                        
                elif it == "cia" or it == "cía":
                    combined = (it + "/" + itpos + " " + ne + "-" + se + "/" + sepos + "+" + nepos + "|" + nean)
                    n += 1
               
                elif itpos == "noun" or itpos == "verbal_noun" or itpos == "adjective" or itpos == "pronoun_independent":
                    combined = (it + "-" + ne + "/" + itpos + "+" + nepos + "|" + itan)
                
                elif itpos == "pronoun_infixed" and nepos == "verb":
                    if wild != None:
                        combined = (ne + "/" + nepos + "+" + itpos + "|" + nean + "+" + itan)
                    else:
                        combined = (it + ne + "/" + nepos + "+" + itpos + "|" + nean + "+" + itan)
                
                elif itpos == "particle_relative" and nepos == "verb":
                    combined = (it + ne + "/" + nepos + "+" + itpos + "|" + nean)
                    
                elif itpos == "copula" and nepos == "particle_relative":
                    combined = (it + "/" + itpos + "+" + nepos + "|" + itan)
                
                elif itpos == "pronoun_relative":
                    combined = (it + ne + "/" + nepos + "+" + itpos + "|" + nean)
                
                else:
                    combined = (it + ne + "/" + itpos + "+" + nepos + "|" + nean)
                    
                # print(combined)
                combined = update_dots(combined)
                newpos.append(combined)
                item = 0
                nxt = 0

        
        # No Combination
        if item == 0:
            n += 1
            pass
        else:
            newpos.append(item)
            
        combined = "∅"
        # print(n, item)
        n += 1


        
# =============================================================================
# Adds to the output list and the final output "allout"
# =============================================================================  
    
    for idx, po in enumerate(newpos):
        if po is not None:
            if 'Ö' in po:
                po = (po.partition("Ö")[0] + "|" + po.partition("Ö")[2])
                po = po.replace(" ", "_")
                newpos[idx] = po
        else:
            po = 'None'
            newpos[idx] = po
        
    output = ' '.join(newpos)
    output = output.replace("None+", "")
    output = output.replace("copula", "verb")

    if tuornot == "y":
        textual_unit = subframe["Textual_Unit"].iloc[0]
        allout.append(textual_unit + "öäü" + output + "$üäö")
    else:
        allout.append(output + "$öäü")
        
#   Sets the counter for the next ID    
    p += 1

# =============================================================================
# Sets the version POS, Morphology or both
# =============================================================================
    
whichone = input("Do you want (1) POS, (2) Morphological, or (3) POS and Morphological tags? ")

if whichone == "1":
    update_allout(allout, whichone)   
    finaloutput = update_finaloutput(finaloutput)
    outputname = outputname.replace(".txt", "_POS.txt")

elif whichone == "2":
    update_allout(allout, whichone)
    finaloutput = update_finaloutput(finaloutput)
    outputname = outputname.replace(".txt", "_MOR.txt")

else:
    finaloutput = update_finaloutput(allout)
        
if tuornot == "y":
    outputname = outputname.replace(".txt", "_TU.txt")

# =============================================================================
# Writes the output into a .txt-file
# =============================================================================
with open(("Corphusated/" + outputname), "w") as output:
    output.write(str(finaloutput))