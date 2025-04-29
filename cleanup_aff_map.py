import os
import sys
import json
import copy
from datetime import timedelta
from typing import Optional
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import ietfdata
import ietfdata.tools.affiliations as af
import ietfdata.tools.affiliation_mapping_dictionary as afmap
if __name__ == '__main__':
    aff = af.Affiliations()
    output_path = None
    input_path = None
    if len(sys.argv) == 2:
        output_path = Path(sys.argv[1])
    if output_path is None:
        output_path = "./affiliation_map.py"
    keys = list(afmap.affiliation_list_map.keys())
    new_map = dict()
    for key in keys:
        tmp_key = key
        tmp_key = aff._cleanup_affiliation_academic(tmp_key)
        tmp_key = aff._cleanup_affiliation_strip_chars(tmp_key)
        tmp_key = aff._cleanup_affiliation_suffix(tmp_key)
        if key in new_map:
            continue
        key_lower_found = False
        for new_key in new_map:
            if tmp_key.lower() == new_key.lower():
                key_lower_found = True
                break
        if key_lower_found:
            assert(new_key.lower()==tmp_key.lower())
            print(f"key.lower() found: {new_key} vs {tmp_key}")
            continue
        else:
            tmp_val = afmap.affiliation_list_map.get(key)
            if tmp_val is None:
                continue
            tmp_list = list()
            for tmp_item in tmp_val:
                tmp_item = aff._cleanup_affiliation_strip_chars(tmp_item) # remove white spaces
                tmp_item = aff._cleanup_affiliation_suffix(tmp_item) # remove suffixes
                if tmp_item == "":
                    continue
                if tmp_item != tmp_key: # purge A->A mapping
                    tmp_list.append(tmp_item)
            if len(tmp_list) > 0:
                new_map[tmp_key] = tmp_list 
        
    
    with open(output_path,'w') as f:
        print("affiliation_list_map = {",file=f)
        for aff in new_map:
            print(f'    "{aff.replace('"','\\"')}":\n        [',end='',file=f)
            list_str = ""
            for val in new_map[aff]:
                list_str+=(f'"{val.replace('"','\\"')}",')
            list_str = list_str.rstrip(',')
            print(f"{list_str}],",file=f)
        print("}",file=f)