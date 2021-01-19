#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 14:41:50 2020

@author: bbauer
"""

import pandas as pd
import re

# =============================================================================
#  the csv.file needs to contain the following columns: 
#  ID, Text_Unit_ID, Morph, Analysis, Part_Of_Speech, Lemma, Textual_Unit
#  open the csv-file as pandas dataframe
#  always check that the file is in utf-8
#   
# =============================================================================
# =============================================================================
# select MORPHOLOGY.ID, MORPHOLOGY.Text_Unit_ID, MORPHOLOGY.Morph, MORPHOLOGY.Analysis, LEMMATA.Part_Of_Speech, LEMMATA.Lemma, SENTENCES.Textual_Unit, substring(MORPHOLOGY.Text_Unit_ID from 7) as Ord
# from MORPHOLOGY
# inner join LEMMATA on MORPHOLOGY.Lemma = LEMMATA.Lemma
# inner join SENTENCES on MORPHOLOGY.Text_Unit_ID = SENTENCES.Text_Unit_ID
# where MORPHOLOGY.Text_ID = "0006"
# order by Ord + 0, MORPHOLOGY.Sort_ID 
# =============================================================================

inputfile = "/Users/bbauer/Dropbox/Programming/Corphusator/CorphExports/9.csv"
outputname = inputfile[-6:-4] + "_Corphusated.txt"
df = pd.read_csv(inputfile, encoding="utf-8", na_filter=False)


# =============================================================================
# Checks for empty analyses
# =============================================================================y





# a list of all the TUs in the file
ID = list(df.Text_Unit_ID.unique())

# =============================================================================
#  Deletes all the preverbs from the dataframe, but the dummy-particle is kept
# =============================================================================
dummy = df.loc[df["Morph"] == "no"] + df.loc[df["Morph"] == "nu"] + df.loc[df["Morph"] == "no·"] + df.loc[df["Morph"] == "nu·"]
leavelist = list(dummy.index)
delete = df.loc[df["Part_Of_Speech"] == "particle_preverb"]
dellist = list(delete.index)

for l in leavelist:
    if l in dellist:
        dellist.remove(l)

df = df[~df.index.isin(dellist)]



# =============================================================================
# Changes the POS for the copula
# =============================================================================

df["Part_Of_Speech"][df["Lemma"] == "is 1"] = "copula"


# =============================================================================
# Gets a list of ma and cia
# =============================================================================

ma = (df.loc[df["Lemma"] == "ma"]).index
cia1 = (df.loc[df["Lemma"] == "cía 1"]).index
cia2 = (df.loc[df["Lemma"] == "cía 2"]).index

conjlist = list(list(ma) + list(cia2) + list(cia1))
conlist = []

for c in conjlist:
    con = df.ID[c]
    conlist.append(con)
    

# =============================================================================
# Lists of combinations and the empty lists needed
# =============================================================================
doublelist = ["adjective+particle_anaphoric", "adjective+particle_demonstrative_distal",
              "adjective+particle_demonstrative_proximate",
              "complementiser+verb", "complementiser+copula",
              "conjunction+copula", "conjunction+verb", 
              "copula+particle_relative",
              "particle_augment+verb", "particle_augment+copula",
              "particle_interrogative+verb", "particle_interrogative+copula",
              "particle_negative_main+verb", "particle_negative_main+copula",
              "particle_negative_subordinate+verb", "particle_negative_subordinate+copula",
              "particle_preverb+verb", "particle_preverb+copula", 
              "particle_relative+verb", "particle_relative+copula"
              "preposition+verb", "preposition+particle_pronominal",
              "pronoun_infixed+verb","pronoun_interrogative+verb","pronoun_relative+verb",
              "pronoun_interrogative+copula",
              "pronoun_independent+particle_anaphoric",
              "verb+particle_pronominal", "copula+particle_pronominal",                      
              "noun+particle_anaphoric", "noun+particle_pronominal",
              "noun+particle_demonstrative_distal", "noun+particle_demonstrative_proximate",
              "particle_prefix+noun", "particle_prefix+adjective", "particle_prefix+verbal_noun",
              "preposition+definite_article", "preposition+particle_pronominal", 
              "preposition+pronoun_possessive", "preposition+verb",
              "pronoun_independent+particle_pronominal",
              "verbal_noun+particle_anaphoric", "verbal_noun+particle_pronominal",
              "verbal_noun+particle_demonstrative_distal",
              "verb+particle_relative", "verb+particle_anaphoric", 
              "verbal_participle+particle_anaphoric"]
triplelist = ["complementiser+particle_augment+verb", "complementiser+particle_augment+copula", 
              "complementiser+particle_negative_main+verb", "complementiser+particle_negative_main+copula",
              "complementiser+particle_negative_subordinate+verb", "complementiser+particle_negative_subordinate+copula",
              "complementiser+pronoun_infixed+verb", "complementiser+pronoun_infixed+copula",
              "definite_article+verb+particle_pronominal",
              "particle_augment+pronoun_relative+verb", "particle_augment+pronoun_relative+copula",
              "particle_augment+pronoun_infixed+verb", "particle_augment+pronoun_infixed+copula",
              "particle_augment+particle_relative+verb", "particle_augment+particle_relative+copula",
              "particle_augment+particle_augment+verb", "particle_augment+particle_augment+copula",
              "particle_augment+verb+particle_anaphoric", "particle_augment+copula+particle_anaphoric",
              "particle_augment+verb+particle_pronominal",
              "particle_preverb+pronoun_infixed+verb", "particle_preverb+pronoun_infixed+copula",
              "particle_preverb+particle_relative+verb", "particle_preverb+particle_relative+copula",
              "particle_relative+verb+particle_pronominal",
              "particle_prefix+preposition+adverb", "particle_prefix+verbal_noun+particle_anaphoric"
              "particle_interrogative+verb+particle_pronominal",
              "particle_negative_main+verb+particle_pronominal", "particle_negative_main+copula+particle_pronominal",
              "particle_negative_main+particle_augment+verb", "particle_negative_main+particle_augment+copula",
              "particle_negative_main+pronoun_infixed+verb", "particle_negative_main+pronoun_infixed+copula",
              "particle_negative_subordinate+particle_augment+verb", "particle_negative_subordinate+particle_augment+copula",
              "particle_negative_subordinate+pronoun_infixed+verb",  "particle_negative_subordinate+pronoun_infixed+copula",
              "particle_negative_subordinate+pronoun_relative+verb", "particle_negative_subordinate+pronoun_relative+copula",
              "particle_negative_subordinate+particle_relative+verb", "particle_negative_subordinate+particle_relative+copula",
              "particle_relative+particle_augment+verb", "particle_relative+particle_augment+copula",
              "particle_relative+verb+particle_anaphoric",
              "preposition+pronoun_relative+verb", "preposition+pronoun_relative+copula",
              "preposition+particle_augment+verb", "preposition+particle_augment+copula",
              "preposition+pronoun_infixed+verb", "preposition+pronoun_infixed+copula",
              "pronoun_infixed+particle_augment+verb","pronoun_infixed+particle_augment+copula",
              "pronoun_infixed+particle_relative+verb",
              "pronoun_infixed+verb+particle_pronominal"]
quartlist = ["complementiser+particle_negative_subordinate+particle_augment+verb",
             "complementiser+particle_negative_subordinate+particle_augment+copula",
             "conjunction+particle_relative+verb+particle_comparative",
             "conjunction+particle_negative_main+pronoun_infixed+verb",
             "particle_augment+particle_relative+pronoun_infixed+verb",
             "particle_augment+particle_relative+pronoun_infixed+copula",
             "particle_augment+pronoun_infixed+verb+particle_pronominal",
             "particle_interrogative+particle_negative_subordinate+particle_relative+verb",
             "particle_interrogative+particle_augment+verb+particle_pronominal",
             "particle_negative_main+pronoun_infixed+verb+particle_pronominal",
             "particle_negative_subordinate+particle_relative+particle_augment+verb",
             "particle_negative_subordinate+particle_relative+particle_augment+copula",
             "particle_negative_subordinate+particle_relative+pronoun_infixed+verb",
             "particle_negative_subordinate+particle_relative+verb+particle_pronominal",
             "particle_preverb+conjunction+verb+particle_pronominal",
             "particle_preverb+pronoun_infixed+verb+particle_pronominal",
             "particle_relative+pronoun_infixed+particle_augment+verb",
             "particle_relative+pronoun_infixed+particle_augment+copula",
             "particle_relative+particle_augment+verb+particle_pronominal",
             "particle_relative+pronoun_infixed+verb+particle_pronominal",
             "preposition+pronoun_relative+particle_augment+verb",
             "preposition+pronoun_relative+particle_augment+copula",
             "preposition+pronoun_relative+pronoun_infixed+verb",
             "preposition+pronoun_relative+pronoun_infixed+copula",
             "preposition+pronoun_relative+particle_negative_subordinate+copula",
             "pronoun_infixed+particle_relative+particle_augment+verb"]
quintlist = ["particle_negative_main+pronoun_infixed+particle_augment+verb+particle_pronominal",
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
# Defines the function(s)
# =============================================================================

def update_combined(combined):
    
    doubles = combined.count('·')
    

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
    
    elif doubles > 1 and '∅' not in combined:
        newc = combined.partition('·')[2]
        combined = newc
    

    return combined
    
# =============================================================================
# The fun starts here
# =============================================================================

tuornot = input("Do you want to display the TUs? (y/n) ")

for I in ID:
    

    pos = ID[p] # check this!
    subframe = df[df.Text_Unit_ID == ID[p]]   
    index = subframe["ID"]
    pos = subframe["Part_Of_Speech"]
    morph = subframe["Morph"]
    an = subframe["Analysis"]
    
    # Further lists and variables
    adding = morph + "/" + pos + "Ö" + an
    poslist = adding.tolist()
    posis = len(poslist)
    n = 0
    newpos = []
   
        
    for morph in poslist:

        # Breaks the loop if n is the length of the poslist
        if n >= posis:
            break      
        
        
# =============================================================================
#         Definitions
# =============================================================================
        
        # Defines the items, nexts, etc.
                    
        item = subframe["Morph"].iloc[n] + "/" + subframe["Part_Of_Speech"].iloc[n] + "Ö" + subframe["Analysis"].iloc[n]
        itemID = subframe["ID"].iloc[n]

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
                combined = (se + "/compound_" + nepos + "|" + sean)
                combined = update_combined(combined)
                newpos.append(combined)
                n += 3
            else:
                combined = (it + ne + "/compound_" + nepos + "|" + sean)
                combined = update_combined(combined)
                newpos.append(combined)
                n += 2
            continue
        
        # Combines ci with the copula
        # ("ci" == it or "ce"== it or "cid" == it)
        # maci = ["cid", "ce", "ci", "ma", "mad"]
        
        # if (it in maci) and nepos == "copula":
        #     print(it)
        #     combined = (it + ne + "/" + itpos + "+" + nepos + "|" + nean)
        #     combined = update_combined(combined)
        #     newpos.append(combined)
        #     n += 2
        #     continue

        
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

# =============================================================================
#         # Combination of five
# =============================================================================
        try:
            itemnextsecthifou
        except NameError:
            pass
        else:
            if itemnextsecthifou in quintlist:

                if itpos == "conjunction" and fopos == "particle_pronominal":
                    combined = (it + ne + se + th + "-" + fo + "/" + itpos + "+" + nepos + "+" + thpos + "+" + sepos + "+" + fopos + "|" + than)
                
                else:
                    combined = (it + ne + se + th + fo + "/" + itpos + "+" + thpos + "+" + nepos + "+" + sepos + "+" + fopos + "|" + than)
                combined = update_combined(combined)
                newpos.append(combined)
                n += 4
                item = 0
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
                    elif nepos == "pronoun_infixed" and thpos == "particle_pronominal":
                        combined = (se + "-" + th + "/" + sepos + "+" + nepos + "+" + itpos + "+" + thpos + "|" + sean + "+" + than)
                
                elif itpos == "particle_preverb" and nepos == "conjunction" and sepos == "verb":
                    combined = (se + "-" + th + "/" + nepos + "+" + sepos + "+" + thpos + "|" + sean + "+" + than)
                                    
                elif "negative" in itpos:
                    if nepos == "particle_relative" and sepos == "pronoun_infixed":
                        combined = (it + se + th + "/" + itpos + "+" + thpos + "+" + nepos + "+" + sepos + "|" + than + "+" + sean)
                    elif itpos == "particle_negative_subordinate" and thpos == "particle_pronominal":
                        combined = (it + se + "-" + th + "/" + itpos + "+" + sepos + "+" + nepos + "+" + thpos + "|" + sean + "+" + than)
                    elif nepos == "pronoun_infixed" and thpos == "particle_pronominal":
                        combined = (it + ne + se + "-" + th + "/" + itpos + "+" + sepos + "+" + nepos + "+" + thpos + "|" + sean + "+" + nean + "+" + than)
                
                elif itpos == "particle_augment" and nepos == "pronoun_infixed" and thpos == "particle_pronominal":
                    combined = (it + ne + se + "-" + th + "/" + sepos + "+" + itpos + "+" + nepos + "+" + thpos + "|" + sean + "+" + nean + "+" + than)
                
                elif itpos == "pronoun_infixed" and nepos == "particle_relative" and sepos == "particle_augment":
                    combined = (th + "/" + thpos + "+" + sepos + "+" + nepos + "+" + itpos + "|" + than + "+" + itan)
                
                elif thpos == "particle_comparative":
                    combined = (th + "/" + thpos + "|" + than)
                    
                elif itpos == "particle_preverb" and nepos == "pronoun_infixed" and thpos == "particle_pronominal":
                    combined = (se + "-" + th + "/" + sepos + "+" + nepos + "+" + thpos + "|" + sean + "+" + nean + "+" + than)
                
                elif ne[:1] or se[:1] in th[:1]: 
                    if ne[:1] in th[:1]:
                        combined = (it + se + th + "/" + thpos + "+" + itpos + "+" + nepos + "+" + sepos + "|" + than)
                    else:
                        combined = (it + ne + th + "/" + thpos + "+" + itpos + "+" + nepos + "+" + sepos + "|" + than)
                
                else:
                    combined = (it + ne + se + th + "/" + thpos + "+" + itpos + "+" + nepos + "+" + sepos + "|" + than)
                combined = update_combined(combined)
                newpos.append(combined)
                n += 3
                item = 0
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

                if sepos == "particle_pronominal" and "negative" not in itpos:
                    if itpos == "particle_interrogative":
                        combined = (it + ne + "-" + se + "/" + itpos + "+" + nepos + "+" + sepos + "|" + nean + "+" + sean)            
                    else:
                        combined = (it + ne + "-" + se + "/" + nepos + "+" + itpos + "+" + sepos + "|" + nean + "+" + sean)

                elif (se == "suas" or se == "súas"):
                    combined = (se + "/" + sepos + "|" + sean)
                    
                elif "negative" in itpos:
                    if "relative" in nepos:
                        combined = (it + ne + se + "/" + itpos + "+" + sepos + "+" + nepos + "|" + sean)
                    elif sepos == "particle_pronominal":
                        combined = (it + ne + "-" + se + "/" + itpos + "+" + nepos + "+" + sepos + "|" + nean + "+" + sean)            
                    elif "pronoun" in nepos:
                        combined = (it + ne + se + "/" + itpos + "+" + sepos + "+" + nepos + "|" + sean + "+" + nean)
                    elif "·" in it and "·" in se:
                        combined = (it + se + "/" + itpos + "+" + nepos + "+" + sepos + "|" + sean)                  
                    else:
                        combined = (it + ne + se + "/" + itpos + "+" + nepos + "+" + sepos + "|" + sean)
                
                elif (it[:1] or ne[:1]) == se[:1]: 
                    if ne[:1] == se[:1]:
                        combined = (it + ne + se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean)
                    elif it[:1] == se[:1]:
                        combined = (se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean)
                    else:
                        combined = (it + se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean)
                
                elif itpos == "particle_preverb":
                    if nepos == "pronoun_infixed":
                        combined = (it + ne + se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean)
                    elif nepos == "particle_relative":
                        combined = (it + ne + se)
                
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
                
                elif itpos == "particle_augment":
                    if nepos == "pronoun_relative":
                        combined = (it + ne + se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean)
                    elif nepos == "pronoun_infixed":
                        combined = (it + ne + se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean + "+" + nean)
                    elif nepos == "particle_augment":
                        combined = (it + ne + se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean)
                    
                elif itpos == "pronoun_infixed" and nepos == "particle_augment":
                    combined = (se + "/" + sepos + "+" + nepos + "+" + itpos + "|" + sean + "+" + itan)
                
                elif itpos == "complementiser":
                    if nepos == "pronoun_infixed" and sepos == "verb":
                        combined = (it + ne + se + "/" + itpos + "+" + sepos + "+" + nepos + "|" + sean + "+" + nean)
                    elif nepos == "particle_augment" and sepos == "verb":
                        if len(ne) == 1:
                            combined = (it + se + "/" + itpos + "+" + sepos + "+" + nepos + "|" + sean)
                        else:
                            combined = (it + ne + se + "/" + itpos + "+" + sepos + "+" + nepos + "|" + sean)
                    elif (nepos == "particle_negative_main" or nepos == "particle_negative_subordinate") and (sepos == "verb" or sepos == "copula"):
                        combined = (it + ne + se + "/" + itpos + "+" + nepos + "+" + sepos + "|" + sean)
                    
                elif sepos == "particle_pronominal":
                    combined = (it + ne + "-" + se + "/" + itpos + "+" + nepos + "+" + sepos + "|" + nean + "+" + sean)
                
                else:
                    combined = (se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean)
                n += 2
                
                combined = update_combined(combined)
                dotcount = combined.count("·")
                if dotcount > 1:
                    if '··' in combined:
                        combined = combined.replace('··', '·')
                    else:
                        print("We have a dot-problem: " + combined.partition("/")[0])
                        combinedanalysis = combined.partition("/")[2]
                        newcombi = input("What should we have? ")
                        combined = newcombi + "/" + combinedanalysis
                    
                    
                newpos.append(combined)
                item = 0
                
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
                if nepos == "particle_pronominal" or nepos == "particle_anaphoric":
                    if "-" in ne:
                        ne = ne.replace('-', '')
                    combined = (it + "-" + ne + "/" + itpos + "+" + nepos + "|" + itan + "+" + nean)
                    
                # elif "conjunction" in itpos and ne == "is":
                #     newpos.append(item)
                #     n += 1
                #     continue
                
                elif it == "7":
                    newpos.append(item)
                    n += 1
                    continue
                    
                elif "complementiser" in itpos or "particle_interrogative" in itpos or "negative" in itpos:
                    combined = (it + ne + "/" + itpos + "+" + nepos + "|" + nean)
                
                elif itpos == "particle_augment":
                    if it in ne:
                        combined = (ne + "/" + nepos + "+" + itpos + "|" + nean)
                    else:
                        combined = (it + ne + "/" + nepos + "+" + itpos + "|" + nean)
                        
                elif itpos == "conjunction":
                    if itemID in conlist:
                        combined = (it + ne + "/" + itpos + "+" + nepos + "|" + nean)
                        n += 1
                    else:
                        combined = (it + "/" + itpos + "|" + itan)
                        n -= 1
    
                elif itpos == "particle_preverb":
                    combined = (it + ne + "/" + nepos + "|" + nean)
                
                elif (nepos == "particle_augment" or nepos == "pronoun_infixed") and wild != None:
                    combined = (ne + "/" + nepos + "+" + itpos + "|" + nean)
    
                elif (itpos == "preposition" and nepos == "definite_article"):
                    if it in ("cenmithá", "dochum"):
                        combined = (it + "/" + itpos + "|" + itan)
                        n -= 1
                    else:
                        combined = (it + ne + "/" + itpos + "+" + nepos + "|" + itan + "+" + nean)
                        
                elif (itpos == "preposition" and nepos == "verb"):
                    if "·" in it:
                        combined = (it + ne + "/" + nepos + "+" + itpos + "|" + nean + "+" + itan)
                    else:
                        pass
                
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
                
                else:
                    combined = (it + ne + "/" + itpos + "+" + nepos + "|" + nean)
                    
                n += 1

                dotcount = combined.count("·")
                if dotcount > 1:
                    if '··' in combined:
                        combined = combined.replace('··', '·')
                    else:
                        print("We have a dot-problem: " + combined.partition("/")[0])
                        combinedanalysis = combined.partition("/")[2]
                        newcombi = input("What should we have? ")
                        combined = newcombi + "/" + combinedanalysis
                combined = update_combined(combined)
                newpos.append(combined)
                item = 0
            
                
        
        # No Combination

        if item == 0:
            pass
        else:
            newpos.append(item)
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
    output = (output.replace("None+", ""))
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
    for out in allout:
        one = str(out)
        split = one.split( )
        for token in split:
            token = (token.partition("|")[0] + token.partition("$")[2])
            finaloutput.append(token)

    
    finaloutput = str(finaloutput)
    finaloutput = finaloutput.replace("'", "")
    finaloutput = finaloutput.replace(",", "")
    finaloutput = finaloutput.replace("$", "")
    finaloutput = finaloutput.replace("öäü", " \n")
    finaloutput = finaloutput.replace("üäö", " \n\n")
    outputname = outputname.replace(".txt", "_POS.txt")


elif whichone == "2":
    for out in allout:
        one = str(out)
        split = one.split( )
        for token in split:
            token = (token.partition("/")[0] + "/" + token.partition("|")[2])
            finaloutput.append(token)
    
    finaloutput = str(finaloutput)
    finaloutput = finaloutput.replace("'", "")
    finaloutput = finaloutput.replace(",", "")
    finaloutput = finaloutput.replace("$", "")
    finaloutput = finaloutput.replace("öäü", " \n")
    finaloutput = finaloutput.replace("üäö", " \n\n")
    outputname = outputname.replace(".txt", "_MOR.txt")

else:
    finaloutput = str(allout)
    finaloutput = finaloutput.replace("'", "")
    finaloutput = finaloutput.replace(",", "")
    finaloutput = finaloutput.replace("$", "")
    finaloutput = finaloutput.replace("öäü", " \n")
    finaloutput = finaloutput.replace("üäö", " \n\n")
            
        
finaloutput = finaloutput.replace("[", "")
finaloutput = finaloutput.replace("]", "")

if tuornot == "y":
    outputname = outputname.replace(".txt", "_TU.txt")

# =============================================================================
# Writes the output into a .txt-file
# =============================================================================

with open(("/Users/bbauer/Dropbox/Programming/Corphusator/Corphusated/" + outputname), "w") as output:
    output.write(str(finaloutput))

