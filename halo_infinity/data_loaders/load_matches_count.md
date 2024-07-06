# Halo Waypoint API Functions

This document describes the functions used to interact with the Halo Waypoint API.

## Functions

### get_spartan_token

This function uses the XSTS token to request a Spartan token from the Halo Waypoint API. This token is returned as an XML string, which is parsed into a Python dictionary and then converted back into a JSON string.

### get_clearance_value

This function uses the Spartan token to request a clearance value from the Halo Waypoint API. This value is used for further API requests.

### get_spartan_and_clearance_tokens

This is a wrapper function that calls the previous functions to fetch the user token, XSTS token, Spartan token, and clearance value.

### get_matches_played_count and get_match_history

These functions use the Spartan token to fetch the number of matches played by a user and the user's match history, respectively, from the Halo Waypoint API.

### flatten_match_history

This function takes the match history data (which is a nested JSON structure) and flattens it into a pandas DataFrame.

### load_data_from_api

This function is a template for loading data from an API. It sets some global variables, fetches the Spartan token and clearance value, fetches the number of matches played and the match history, flattens the match history, and returns it as a DataFrame.

### test_output

This function is a template for testing the output of a block of code. It simply checks if the output is not None.

## Built-in Functions

The provided function implementations are Python built-in functions or methods that are used in the script. For example, `globals()` returns a dictionary of the current global symbol table, `read(n)` reads n bytes from a file, `decode(encoding, errors)` decodes a byte string into a regular string, `strip(chars)` removes leading and trailing characters from a string, `replace(old, new, count)` replaces occurrences of a substring within a string, and `sub(pattern, repl, string, count, flags)` replaces occurrences of a pattern within a string using a regular expression.