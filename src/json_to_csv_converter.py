import argparse
import collections.abc
import csv
import simplejson as json


def read_and_write_file(json_file_path, csv_file_path, column_names):
    """Read the JSON dataset file and write it out to a CSV file."""
    try:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as fout:
            csv_file = csv.writer(fout)
            csv_file.writerow(list(column_names))  # Write header
            with open(json_file_path, encoding='utf-8') as fin:
                for line in fin:
                    line_contents = json.loads(line)
                    csv_file.writerow(get_row(line_contents, column_names))
    except (IOError, OSError) as e:
        print(f"Error processing files: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")


def get_superset_of_column_names_from_file(json_file_path):
    """Read the JSON dataset file and return the superset of column names."""
    column_names = set()
    try:
        with open(json_file_path, encoding='utf-8') as fin:
            for line in fin:
                line_contents = json.loads(line)
                column_names.update(get_column_names(line_contents).keys())
    except (IOError, OSError) as e:
        print(f"Error reading file: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    return column_names


def get_column_names(line_contents, parent_key=''):
    """Return a list of flattened key names from a dictionary."""
    column_names = []
    for k, v in line_contents.items():
        column_name = f"{parent_key}.{k}" if parent_key else k
        if isinstance(v, collections.abc.MutableMapping):
            column_names.extend(get_column_names(v, column_name).items())
        else:
            column_names.append((column_name, v))
    return dict(column_names)


def get_nested_value(d, key):
    """Return a dictionary item given a flattened key."""
    if '.' not in key:
        return d.get(key, None)  # Safely return the value or None

    base_key, sub_key = key.split('.', 1)
    sub_dict = d.get(base_key)

    # Ensure sub_dict is a dictionary
    if isinstance(sub_dict, dict):
        return get_nested_value(sub_dict, sub_key)
    else:
        return None  # Return None if the value isn't a dictionary


def get_row(line_contents, column_names):
    """Return a CSV-compatible row given column names and a dict."""
    row = []
    for column_name in column_names:
        line_value = get_nested_value(line_contents, column_name)
        if isinstance(line_value, str):
            row.append(line_value)
        elif line_value is not None:
            row.append(str(line_value))
        else:
            row.append('')
    return row


if __name__ == '__main__':
    """Convert a Yelp dataset file from JSON format to CSV."""
    parser = argparse.ArgumentParser(
        description='Convert Yelp Dataset Challenge data from JSON format to CSV.'
    )
    parser.add_argument(
        'json_file',
        type=str,
        help='The JSON file to convert.',
    )
    args = parser.parse_args()

    json_file = args.json_file
    csv_file = f"{json_file.rsplit('.json', 1)[0]}.csv"

    column_names = get_superset_of_column_names_from_file(json_file)
    read_and_write_file(json_file, csv_file, column_names)
