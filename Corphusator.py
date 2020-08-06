#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 08:39:43 2020

@author: bbauer
"""


import pandas as pd
import re

# =============================================================================
#  the csv.file needs to contain the following columns: 
#  ID_unique_number, Textual_Unit_ID, Morph, Analysis, Part_Of_Speech, Lemma
#  open the csv-file as pandas dataframe
#  always check that the file is in utf-8
# =============================================================================

inputfile = "/Users/bbauer/Dropbox/Programming/Corphusator/CorphExports/78.csv"
outputname = inputfile[-6:-4] + "_Corphusated.txt"
df = pd.read_csv(inputfile, encoding="utf-8", na_filter=False)


# =============================================================================
# Checks for empty analyses
# =============================================================================




# a list of all the TUs in the file
ID = list(df.Textual_Unit_ID.unique())

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
    con = df.ID_unique_number[c]
    conlist.append(con)
    

# =============================================================================
# Lists of combinations and the empty lists needed
# =============================================================================
doublelist = ["complementiser+verb",
              "conjunction+copula",
              "particle_augment+verb", "particle_augment+copula",
              "particle_interrogative+verb", "particle_interrogative+copula",
              "particle_negative_main+verb", "particle_negative_main+copula",
              "particle_negative_subordinate+verb", "particle_negative_subordinate+copula"
              "particle_preverb+verb", "particle_preverb+copula", 
              "particle_relative+verb", "particle_relative+copula"
              "preposition+verb", "preposition+particle_pronominal",
              "pronoun_infixed+verb","pronoun_interrogative+verb","pronoun_relative+verb",
              "verb+particle_pronominal",                        
              "noun+particle_anaphoric", "noun+particle_pronominal",
              "noun+particle_demonstrative_distal",
              "particle_prefix+noun", "particle_prefix+adjective", "particle_prefix+verbal_noun",
              "preposition+definite_article", "preposition+particle_pronominal", 
              "preposition+pronoun_possessive",
              "pronoun_independent+particle_pronominal",
              "verbal_noun+particle_anaphoric", "verbal_noun+particle_pronominal",
              "verbal_noun+particle_demonstrative_distal",
              "verb+particle_relative"]
triplelist = ["complementiser+particle_augment+verb", "complementiser+particle_negative_main+verb",
              "complementiser+particle_negative_subordinate+verb", "complementiser+pronoun_infixed+verb",
              "particle_augment+pronoun_relative+verb", "particle_augment+pronoun_infixed+verb",
              "particle_augment+particle_relative+verb",
              "particle_preverb+pronoun_infixed+verb", "particle_preverb+particle_relative+verb",
              "particle_negative_main+particle_augment+verb", "particle_negative_main+pronoun_infixed+verb",
              "particle_negative_subordinate+particle_augment+verb", "particle_negative_subordinate+pronoun_infixed+verb",
              "particle_negative_subordinate+pronoun_relative+verb", "particle_negative_subordinate+particle_relative+verb",
              "particle_relative+particle_augment+verb",
              "preposition+pronoun_relative+verb", "preposition+particle_augment+verb", "preposition+pronoun_infixed+verb",
              "pronoun_infixed+particle_augment+verb", "pronoun_infixed+verb+particle_pronominal"]
quartlist = ["complementiser+particle_negative_subordinate+particle_augment+verb",
             "preposition+pronoun_relative+particle_augment+verb",
             "preposition+pronoun_relative+pronoun_infixed+verb"]
quintlist = ["particle_negative_main+pronoun_infixed+particle_augment+verb+particle_pronominal"]

poslist = []
allout = []
finaloutput = []
p = 0

# =============================================================================
# Representation of verbal complexes
# =============================================================================

# conjunction/interrogative
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

for I in ID:
    

    pos = ID[p]
    subframe = df[df.Textual_Unit_ID == ID[p]]   
    index = subframe["ID_unique_number"]
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
        itemID = subframe["ID_unique_number"].iloc[n]

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

                if itpos == "preposition" and nepos == "pronoun_relative" and sepos == "pronoun_infixed":
                    combined = (it + ne + se + th + "/" + thpos + "+" + itpos + "+" + nepos + "+" + sepos + "|" + than)
                
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
                if sepos == "particle_pronominal":
                    combined = (it + ne + "-" + se + "/" + nepos + "+" + itpos + "+" + sepos + "|" + nean)
                
                # elif itpos == "conjunction":
                #     if it == "7":
                #         newpos.append(item)
                #         n += 1
                #         continue
                #     # else:
                #     #     combined = (it + ne + se + "/" + itpos + "+" + sepos + "+" + nepos + "|" + sean)
                
                elif (it[:1] or ne[:1]) == se[:1]: 
                    if ne[:1] == se[:1]:
                        combined = (it + ne + se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean)
                    elif it[:1] == se[:1]:
                        combined = (se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean)
                    else:
                        combined = (it + se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean)
                
                elif itpos == "particle_preverb" and nepos == "pronoun_infixed":
                    combined = (it + ne + se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean)
                    
                elif itpos == "particle_preverb" and nepos == "particle_relative":
                    combined = (it + ne + se)
                    
                elif itpos == "conjunction":
                    combined = (it)
    
                elif "negative" in itpos:
                    if "·" in it and "·" in se:
                        combined = (it + se + "/" + itpos + "+" + sepos + "+" + nepos + "|" + sean)
                    else:
                        combined = (it + ne + se + "/" + itpos + "+" + sepos + "+" + nepos + "|" + sean)

                        
                elif itpos == "preposition" and "pronoun" in nepos:
                    if wildne != None:
                        combined = (it + se + "/" + itpos + "+" + sepos +  "+" + nepos + "|" + sean)
                    else:    
                        combined = (it + ne + se + "/" + itpos + "+" + sepos +  "+" + nepos + "|" + sean)
                    
                elif itpos == "preposition" and nepos == "particle_augment":
                    combined = (it + se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean)
                
                elif itpos == "particle_augment" and nepos == "pronoun_relative":
                    combined = (it + ne + se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean)
                
                elif itpos == "particle_augment" and nepos == "pronoun_infixed":
                    combined = (it + ne + se + "/" + sepos + "+" + itpos + "+" + nepos + "|" + sean)
                
                elif itpos == "complementiser" and nepos == "particle_augment" and sepos == "verb":
                    if len(ne) == 1:
                        combined = (it + se + "/" + itpos + "+" + sepos + "+" + nepos + "|" + sean)
                    else:
                        combined = (it + ne + se + "/" + itpos + "+" + sepos + "+" + nepos + "|" + sean)
                
                elif itpos == "complementiser" and (nepos == "particle_negative_main" or nepos == "particle_negative_subordinate") and sepos == "verb":
                    combined = (it + ne + se + "/" + itpos + "+" + sepos + "+" + nepos + "|" + sean)
                    
                elif sepos == "particle_pronominal":
                    combined = (it + ne + "-" + se + "/" + itpos + "+" + nepos + "+" + sepos + "|" + nepos + "+" + sepos)
                    
    
                
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
                if nepos == "particle_pronominal":
                    if "-" in ne:
                        ne = ne.replace('-', '')
                    combined = (it + "-" + ne + "/" + itpos + "+" + nepos + "|" + itan)
                    
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
                
                elif it == "cia" or it == "cía":
                    combined = (it + "/" + itpos + " " + ne + "-" + se + "/" + sepos + "+" + nepos + "|" + nean)
                    n += 1
               
                elif itpos == "noun" or itpos == "verbal_noun":
                    combined = (it + "-" + ne + "/" + itpos + "+" + nepos + "|" + itan)
                
                elif itpos == "pronoun_infixed" and nepos == "verb":
                    if wild != None:
                        combined = (ne + "/" + nepos + "+" + itpos + "|" + nean + "+" + itan)
                    else:
                        combined = (it + ne + "/" + nepos + "+" + itpos + "|" + nean + "+" + itan)
                
                elif itpos == "verb" and nepos == "particle_relative":
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
    output = (output.replace("None+", "") + " .")
    output = output.replace("copula", "verb")
    allout.append(output)
        
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
            token = token.partition("|")[0]
            finaloutput.append(token)
    
    finaloutput = str(finaloutput)
    finaloutput = finaloutput.replace("'", "")
    finaloutput = finaloutput.replace(",", "")
    finaloutput = finaloutput.replace(" .", " \n")
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
    finaloutput = finaloutput.replace(" ./", " \n")
    outputname = outputname.replace(".txt", "_MOR.txt")

else:
    finaloutput = str(allout)
    finaloutput = finaloutput.replace("'", "")
    finaloutput = finaloutput.replace(",", "")
    finaloutput = finaloutput.replace(" .", " \n")
            
        
finaloutput = finaloutput.replace("[", "")
finaloutput = finaloutput.replace("]", "")

# =============================================================================
# Writes the output into a .txt-file
# =============================================================================

with open(("/Users/bbauer/Dropbox/Programming/Corphusator/Corphusated/" + outputname), "w") as output:
    output.write(str(finaloutput))

