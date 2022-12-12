import re

def extract_units(product):
    pattern = r'([\s|^]\d*[\.|\,]?\d*)\s?(g|gr|k|kg|ml|l|lt|lts|cm|m|dz|duzia|kilo|kilos|litro|litros+)(?!\S)'

    match = re.findall(pattern, product, re.I|re.M)
    
    better_match = None
    for m in match:
        if(m[0] != " "):
            better_match = m
            break
    
    if(better_match == None):
        if(len(match) > 0):
            better_match = match[0]
        else:
            return (None, None)

    quantidade = better_match[0].strip()
    unidade = better_match[1].strip()
    return unidade, quantidade