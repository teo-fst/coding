def sort_function(f):
    string=f.split('+')
    dict_string={}

    for code in string:
        key=0
        for bit in enumerate(code):
            if bit[1]=="1":
                key+=2**(2-bit[0])    
        dict_string.update({key:code})

    myKeys = list(dict_string.keys())
    myKeys.sort()
    sorted_dict = {i: dict_string[i] for i in myKeys}

    return list(sorted_dict.values())

print(format(6, f'0{4}b'))
