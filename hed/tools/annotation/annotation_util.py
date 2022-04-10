""" Utilities to facilitate annotation of events in BIDS. """
from pandas import DataFrame
from hed.errors import HedFileError


def check_df_columns(df, required_cols=('column_name', 'column_value', 'description', 'HED')):
    """ Return a list of the specified columns that are missing from a dataframe.
    Args:
        df (DataFrame):         Spreadsheet to check the columns of.
        required_cols (tuple):  List of column names that must be present

    Returns:
        list:   List of column names that are missing

    """
    missing_cols = []
    column_list = list(df.columns.values)
    for col in required_cols:
        if col not in column_list:
            missing_cols.append(col)
    return missing_cols


def df_to_hed(dataframe, description_tag=True):
    """ Creates a sidecar-like dictionary from a four-column dataframe.

    Args:
        dataframe (DataFrame): A four-column Pandas DataFrame with specific columns.
        description_tag (bool): If True description tag is included

    Returns:
        dict compatible with BIDS JSON events.

    The DataFrame must have the columns with names: column_name, column_value,
        description, and HED.
    """
    missing_cols = check_df_columns(dataframe)
    if missing_cols:
        raise HedFileError("RequiredColumnsMissing", f"Columns {str(missing_cols)} are missing from dataframe", "")
    hed_dict = {}
    for index, row in dataframe.iterrows():
        if row['HED'] == 'n/a' and row['description'] == 'n/a':
            continue
        if row['column_value'] == 'n/a':
            hed_dict[row['column_name']] = _get_value_entry(row['HED'], row['description'],
                                                            description_tag=description_tag)
            continue
        cat_dict = hed_dict.get(row['column_name'], {})
        _update_cat_dict(cat_dict, row['column_value'], row['HED'], row['description'],
                         description_tag=description_tag)
        hed_dict[row['column_name']] = cat_dict
    return hed_dict


def extract_tags(hed_string, search_tag):
    """ Extract all instances of specified tag from a tag_string
        Args:
           hed_string (str):   Tag string from which to extract tag.
           search_tag (str):          HED tag to extract

        Returns: (list, list)
            (remainder, extracted)  Remainder is the tag_string without tag, extracted is a list of extracted tags
    """
    extracted = []
    remainder = ""
    back_piece = hed_string
    while back_piece:
        ind = back_piece.find(search_tag)
        if ind == -1:
            remainder = _update_remainder(remainder, back_piece)
            break
        first_pos = _find_last_pos(back_piece[:ind])
        remainder = _update_remainder(remainder, trim_back(back_piece[:first_pos]))
        next_piece = back_piece[first_pos:]
        last_pos = _find_first_pos(next_piece)
        extracted.append(trim_back(next_piece[:last_pos]))
        back_piece = trim_front(next_piece[last_pos:])
    return remainder, extracted


def generate_sidecar_entry(column_name, column_values=None):
    """  Creates the sidecar column dictionary for a given column name

    Args:
        column_name (str):       Name of the column
        column_values (list):    List of column values

     Returns:
         dict   A dictionary representing a template for a sidecar entry.
    """

    sidecar_entry = {"Description": f"Description for {column_name}", "HED": ""}
    if not column_values:
        sidecar_entry["HED"] = "Label/#"
    else:
        levels = {}
        hed = {}
        for column_value in column_values:
            if column_value == "n/a":
                continue
            levels[column_value] = f"Description for {column_value}"
            hed[column_value] = f"Label/{column_value}"
        sidecar_entry["Levels"] = levels
        sidecar_entry["HED"] = hed
    return sidecar_entry


def hed_to_df(sidecar_dict, col_names=None):
    """ Returns a four-column dataframe version of the HED portions of a JSON sidecar.

    Args:
        sidecar_dict (dict):        A dictionary conforming to BIDS JSON events sidecar format.
        col_names (list, None):     A list of the cols to include in the flattened side car.

    Returns:
        DataFrame:   Four-column spreadsheet representing HED portion of sidecar.

    The returned DataFrame has columns: column_name, column_value, description, and hed.

    """

    if not col_names:
        col_names = sidecar_dict.keys()
    column_name = []
    column_value = []
    column_description = []
    hed_tags = []

    for col_key, col_dict in sidecar_dict.items():
        if col_key not in col_names or not isinstance(col_dict, dict) or 'HED' not in col_dict:
            continue
        elif 'Levels' in col_dict or isinstance(col_dict['HED'], dict):
            keys, values, descriptions, tags = _flatten_cat_col(col_key, col_dict)
        else:
            keys, values, descriptions, tags = _flatten_val_col(col_key, col_dict)
        column_name = column_name + keys
        column_value = column_value + values
        column_description = column_description + descriptions
        hed_tags = hed_tags + tags

    data = {"column_name": column_name, "column_value": column_value,
            "description": column_description, "HED": hed_tags}
    dataframe = DataFrame(data).astype(str)
    return dataframe


def merge_hed_dict(sidecar_dict, hed_dict):
    """Update a JSON sidecar based on the hed_dict values

    Args:
        sidecar_dict (dict):    Dictionary representation of a BIDS JSON sidecar.
        hed_dict(dict):         Dictionary derived from a dataframe representation of HED in sidecar.

    """
    for key, value_dict in hed_dict.items():
        if key not in sidecar_dict:
            sidecar_dict[key] = value_dict
            continue
        sidecar_dict[key]['HED'] = value_dict['HED']
        if isinstance(value_dict['HED'], str):
            if value_dict.get('Description', "n/a") != "n/a":
                sidecar_dict[key]['Description'] = value_dict['Description']
            continue
        if isinstance(value_dict['HED'], dict) and 'Levels' in value_dict:
            sidecar_dict[key]['Levels'] = value_dict['Levels']


def trim_back(tag_string):
    """ Returns a copy of tag_string with trailing blanks and commas removed

    Args:
        tag_string (str)     A tag string to be trimmed.

    Returns: (str)
        A copy of tag_string that has been trimmed.
    """

    last_pos = 0
    for ind, char in enumerate(reversed(tag_string)):
        if char not in [',', ' ']:
            last_pos = ind
            break
    return_str = tag_string[:(len(tag_string)-last_pos)]
    return return_str


def trim_front(tag_string):
    """ Returns a copy of tag_string with leading blanks and commas removed

    Args:
        tag_string (str)     A tag string to be trimmed.

    Returns: (str)
        A copy of tag_string that has been trimmed.
    """
    first_pos = len(tag_string)
    for ind, char in enumerate(tag_string):
        if char not in [',', ' ']:
            first_pos = ind
            break
    return_str = tag_string[first_pos:]
    return return_str


def _find_first_pos(tag_string):
    """ Find the position of the first comma or closing parenthesis in tag_string.

    Args:
        tag_string (str):   String to be analyzed

    Returns:
        (int):               Position of first comma or closing parenthesis or length of tag_string if none.

    """
    for ind, char in enumerate(tag_string):
        if char in [',', ')']:
            return ind
    return len(tag_string)


def _find_last_pos(tag_string):
    """ Find the position of the last comma, blank, or opening parenthesis in tag_string.

    Args:
        tag_string (str):   String to be analyzed

    Returns:
        (int):               Position of last comma or opening parenthesis or 0 if none.

    """
    for index, char in enumerate(reversed(tag_string)):
        if char in [',', ' ', '(']:
            return len(tag_string) - index
    return 0


def _flatten_cat_col(col_key, col_dict):
    """ Flatten a sidecar entry corresponding to a categorical column
        Args:
            col_key (str)    Name of the column.
            col_dict (dict)  Dictionary corresponding to categorical of column (must include HED key).

        Returns (tuple)      Four lists each consisting of length corresponding to the number of values.
            key_list, value_list, description_list, hed_list

    """
    keys = []
    values = []
    descriptions = []
    tags = []
    hed_dict = col_dict['HED']
    level_dict = col_dict.get('Levels', {})
    for col_value, entry_value in hed_dict.items():
        keys.append(col_key)
        values.append(col_value)
        remainder, extracted = extract_tags(entry_value, 'Description/')
        if remainder:
            tags.append(remainder)
        else:
            tags.append('n/a')

        if extracted:
            descriptions.append(_tag_list_to_str(extracted, "Description/"))
        else:
            descriptions.append(level_dict.get(col_value, 'n/a'))

    return keys, values, descriptions, tags


def _flatten_val_col(col_key, col_dict):
    """ Flatten a sidecar entry corresponding to a value column
        Args:
            col_key (str)    Name of the column.
            col_dict (dict)  Dictionary corresponding to value of column (must include HED key).

        Returns (tuple)      Four lists each consisting of one element
            key_list, value_list, description_list, hed_list

        The value_list = ['n/a]
    """
    tags, extracted = extract_tags(col_dict['HED'], 'Description/')
    if extracted:
        description = _tag_list_to_str(extracted, removed_tag="Description/")
    else:
        description = col_dict.get('Description', 'n/a')
    return [col_key], ['n/a'], [description], [tags]


def _get_row_tags(row, description_tag=True):
    """Update the dictionary based on the row"""
    remainder, extracted = extract_tags(row['HED'], 'Description/')
    if description_tag:
        tags = row["HED"]
    else:
        tags = remainder

    if row["description"] != 'n/a':
        description = row["description"]
    else:
        description = ""
    if extracted:
        description = " ".join([description, extracted])
    return tags, description


def _get_value_entry(hed_entry, description_entry, description_tag=True):
    value_dict = {}
    tags = ""
    if hed_entry and hed_entry != 'n/a':
        tags = hed_entry
    if description_entry and description_entry != 'n/a':
        value_dict['Description'] = description_entry
        if description_tag and tags:
            tags = tags + ", Description/" + description_entry
        elif description_tag and not tags:
            tags = "Description/" + description_entry
    if tags:
        value_dict["HED"] = tags
    return value_dict


def _tag_list_to_str(extracted, removed_tag=None):
    """ Returns a concatenation of the strings in extracted, with removed_tag prefix deleted.

    Args:
        extracted (list):          List of tag strings to be concatenated.
        removed_tag (str, None):  A HED tag prefix to be removed before concatenation.

    Returns: (str)
        concatenated string

    Note: This function is designed to concatenate strings containing Description tags into a single description.

    """
    if not removed_tag:
        return " ".join(extracted)
    str_list = []
    for ind, item in enumerate(extracted):
        ind = item.lower().find(removed_tag.lower())
        if ind >= 0:
            str_list.append(item[ind+len(removed_tag):])
        else:
            str_list.append(item)
    return " ".join(str_list)


def _update_cat_dict(cat_dict, value_entry, hed_entry, description_entry, description_tag=True):
    """ Updates a category entry in the sidecar dictionary based on a row of the spreadsheet.

    Args:
        cat_dict (dict):         A dictionary representing a category column in a JSON sidecar.
        value_entry (str):       The value of the key in the category dictionary.
        hed_entry (str):         HED tag string corresponding to the key.
        description_entry (str): The description column for the Level entry and possible as a Description tag.
        description_tag (bool):  If True then the description entry is used for Level and as Description tag.

    Returns: (dict)
         Updated dictionary representing a category column.

    """
    value_dict = _get_value_entry(hed_entry, description_entry, description_tag)
    if 'Description' in value_dict:
        level_part = cat_dict.get('Levels', {})
        level_part[value_entry] = value_dict['Description']
        cat_dict['Levels'] = level_part
    if 'HED' in value_dict:
        hed_part = cat_dict.get('HED', {})
        hed_part[value_entry] = value_dict['HED']
        cat_dict['HED'] = hed_part


def _update_remainder(remainder, update_piece):
    """ Updates the remainder string with update piece, paying attention to separating commas

    Args:
        remainder (str):         A tag string without trailing comma
        update_piece (str):      A tag string to be appended

    Returns: (str)
         A concatenation of remainder and update_piece, paying attention to separating commas.

    """
    if not update_piece:
        return remainder
    elif not remainder:
        return update_piece
    elif remainder.endswith('(') or update_piece.startswith(')'):
        return remainder + update_piece
    else:
        return remainder + ", " + update_piece
