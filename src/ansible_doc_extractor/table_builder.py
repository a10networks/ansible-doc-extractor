#    Copyright 2021, A10 Networks
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# MAX_COL_PARAM = 25
# MAX_COL_DEFAULT = 15
# MAX_COL_COMMENT = 100

import math

max_col_param = 0
max_col_default = 0
max_col_comment = 0
def _set_table_lengths(data_value):
    # TODO: THIS IS TERRRIBLE. RE-WRITE IT
    global max_col_param
    global max_col_default
    global max_col_comment
    for k, v in data_value.items():
        if k.lower() == "description" and len(v[0]) >  max_col_comment:
            # Description element is wrapped in a list block though it is just a single entry
             max_col_comment = len(v[0])
        elif k == "suboptions":
            for option in v.keys():
                _set_table_lengths(v[option])
        elif k not in ('required', 'choices') and len(k) >  max_col_param:
            max_col_param = len(k)

def row_builder(col1, col2, col3):
    global max_col_param
    global max_col_default
    global max_col_comment


    cell_padding = lambda x, y: y + " " * x
    col1_str = cell_padding(col1, math.abs(col1 - max_col_param))
    col2_str = cell_padding(col2, math.abs(col2 - max_col_default))
    col3_str = cell_padding(col3, math.abs(col3 - max_col_comment))
    row_str = "| {} | {} | {} |".format(col1_str, col2_str, col3_str)
    return row_str
    

def build_table(data):        
    # TODO: Iterate over objects and find the max char length for each column O(n)
    # column_break = ""
    # for curr_item in column_items:
    #    spaces = (max_column(len(items)) - len(curr_item)) / 2
    #    column_break += "+" + "-" * spaces*2 + "+"
    #    row = "|" + " " * spaces + curr_item + " " * spaces + "|"
    global max_col_param
    for k, v in data.items():
        if len(k) > max_col_param:
            max_col_param = len(k)
        _set_table_lengths(v)

    fill = lambda x, y: x*y

    h1_fill = fill("=", max_col_param + 2)
    h2_fill = fill("=", max_col_default + 2)
    h3_fill = fill("=", max_col_comment + 2)
    header_spacer = "+{}+{}+{}+\n".format(h1_fill, h2_fill, h3_fill)
    
    col1_fill = fill("-", max_col_param + 2)
    col2_fill = fill("-", max_col_default + 2)
    col3_fill = fill("-", max_col_comment + 2)
    row_spacer = "+{}+{}+{}+\n".format(col1_fill, col2_fill, col3_fill)

    table = row_spacer + row_builder("Parameters", "Choices/Defaults", "Comments") + header_spacer

    for k, v in data_value.items():
        choice_default = v.get("choices", " ")
        description = v['description']
        table += row_builder(k, choice_default, description)