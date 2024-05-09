# -*- coding: utf-8 -*-

def dict_search(dictn, match):
    """

    Parameters
    ----------
    dictn : dict
        Contains keys and values with elements to be searched
    match : str
        Value to be matched or found in the input dictionary

    Returns
    -------
    res : str or list
        Key in the input dictionary that contains the matched value. Match is defined as containment in a list, str or pandas series.
        Returns str if only one key is found or a list of strs if multiple keys are found

    """
    # Find the key(s) that contains the value we want to match
    res = [m for m in dictn.keys() if match in dictn[m]]
    if len(res) == 1:
        return res[0]
    else:
        return res

