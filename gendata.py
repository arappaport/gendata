import click
import logging
import csv
import sys
from random import randint
from collections import OrderedDict
from typing import Dict, Any
import hashlib
import json

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# max_loops guards against infinite loops - if there are not enough unique combinations to fill num_rows
MAX_LOOPS = 30 * 1000 * 1000


def prepare_col_opts(template:dict):
    """
    Transform column template into col_opts structure for better use at run-time
    :return:  dict: dict of
    """

    #for each col:
    col_opts = OrderedDict()

    for col,vals in template.items():
        range_under = {}
        prob_sum = 0

        default_val = None
        for val, vprob in vals.items():

            if isinstance(vprob, str) and 'DEFAULT' == vprob.upper():
                default_val = val
                continue
            #TODO handle ints and floats
            prob_sum += (vprob * 100)    # convert to 0 to 100.
            range_under[val] = prob_sum

        if default_val:
            range_under[default_val] = 100

        col_opts[col] = range_under
    return col_opts

def gen_random(col_opts, gen_rows, kwargs):
    unique = kwargs['unique']
    if unique:
        unique_rows = set()

    rows = []

    loop = 0
    num_rows = 0
    while num_rows < gen_rows:

        loop += 1
        if unique and loop > MAX_LOOPS:
            print(f"Error - Unable to find enough unique combinations to fill {num_rows} rows")
            exit(-1)

        row = {}
        for col, ranges in col_opts.items():
            r = randint(0, 99)

            v = None
            for val, val_under in ranges.items():
                if r < val_under:
                    row[col] = val
                    break

        rows.append(row)

        if kwargs['unique']:
            unique_rows.add(dict_hash(row))
            num_rows = len(unique_rows)
        else:
            num_rows += 1
    return rows



def gen_permutations(col_opts, cols:list, rows:list, row:dict):
    """
    Generate a single row for each unique value of the col_opts
    :param col_opts:
    :return:   rows:dict
    """

    #If not more cols to process - we are done with row
    if len(cols) == 0:
        rows.append(row.copy())
        return

    col = cols[0]
    col_opt = col_opts.get(col)
    for val,ignored in col_opt.items():
        row[col] = val
        gen_permutations(col_opts, cols[1:], rows, row)


def write_output(kwargs, col_opts, rows):
    if kwargs['output']:
        f_out = open(kwargs['output'], 'w')
    else:
        f_out = sys.stdout

    if str(kwargs.get('output')).endswith('json'):
        #write JSON
        json.dump(rows,f_out)
    else:
        writer = csv.DictWriter(f_out, fieldnames=col_opts.keys())
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    if f_out != sys.stdout:
        f_out.close()

    if not kwargs['quiet']:
        s = f"generated {len(rows)} items"
        if kwargs['output']:
            s += f" to file \'{kwargs['output']}\'"
        print(s)


def handle_common_cmdline(kwargs):
    """
    Handle common command line options
    :param kwargs:    from click command line.
    :return:   tuple (cols_template, gen_rows)
    """

    if kwargs['quiet']:
        LOGGER.setLevel(logging.WARNING)
    elif kwargs['verbose']:
        LOGGER.setLevel(logging.DEBUG)

    gen_rows = kwargs.get('num') or 100
    gen_rows = int(gen_rows)
    assert gen_rows >= 0, f"--num parameter must > 0.  Value=\'{str(gen_rows)}\'"

    logging.debug("Input File: \'%s\'", kwargs['input'])
    f = open(kwargs['input'], 'r')
    cols_template = json.load(f)
    f.close()

    return cols_template, gen_rows

@click.group()
def cli(**kwargs):
    pass

@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('-o', '--output',help='(optional) name of file to write data into. Default=console ')
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose logging mode')
@click.option('-q', '--quiet', is_flag=True,help='Limits logging output to warnings and errors.  No summary is displayed')
@click.help_option()
def permutations(**kwargs):
    """Generate a CSV with each permutation of columns and possible values. The probabilities are not considered. """
    cols_template, gen_rows = handle_common_cmdline(kwargs)
    col_opts = prepare_col_opts(cols_template)

    rows = []
    gen_permutations(col_opts, cols=list(col_opts.keys()), rows=rows, row={})
    write_output(kwargs, col_opts, rows)

@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('-n', '--num',help='(optional) Number of rows to generate. Default=100.')
@click.option('-o', '--output',help='(optional) name of file to write data into. Default=console ')
@click.option('-u', '--unique', is_flag=True, help='(optional) All generated rows are unique')
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose logging mode')
@click.option('-q', '--quiet', is_flag=True,help='Limits logging output to warnings and errors.  No summary is displayed')
@click.help_option()
def random(**kwargs):
    """Generate a CSV with random values passed on the probabilities of values from the column_template file"""
    cols_template, gen_rows = handle_common_cmdline(kwargs)
    col_opts = prepare_col_opts(cols_template)
    rows = gen_random(col_opts, gen_rows, kwargs )
    write_output(kwargs, col_opts, rows)

# dict_hash is from https://www.doc.ic.ac.uk/~nuric/coding/how-to-hash-a-dictionary-in-python.html
def dict_hash(dictionary: Dict[str, Any]) -> str:
    """MD5 hash of a dictionary."""
    dhash = hashlib.md5()
    # We need to sort arguments so {'a': 1, 'b': 2} is
    # the same as {'b': 2, 'a': 1}
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()


cli.add_command(random)
cli.add_command(permutations)

if __name__ == '__main__':
    cli()
