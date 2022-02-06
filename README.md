# gendata
Generates random datasets from json definition file: columns template. 

Example columns template json file: 

For each column, the file lists the probability of the value occurring in our generated dataset.   So far, values can be strs, ints or floats. 
* Column named 'Col0' has a 0.7 (70%) change of have a value of "Value2_C". 
* A probability of "DEFAULT" - just means whatever is left over.  In Col2, DEFAULT means there is an 0.8 (1.0 - 0.2) 80% chance of a value of '"Value_80perc_DEFAULT"'

```
{  
  "Col0": {
    "Value2_A": 0.1,
    "Value2_B": 0.2,
    "Value2_C": 0.7
  },
  "Col1": {
    "ValueA": 0.99,
    "ValueB": 0.1
  },
  "Col2": {
    "Value_20perc": 0.2,
    "Value_80perc_DEFAULT": "DEFAULT"
  }
}
```



# Usage
There are two commands supported: 
- random - generate a set of random output based on teh probabilities in the column_template file. 
- permutations - Generate a set of all permutations of the column_template file.


## random command

```Usage: gendata.py random [OPTIONS] INPUT

  Generate a CSV with random values passed on the probabilities of values from
  the column_template file
  
  No correlation between any columns

Options:
  -n, --num TEXT     (optional) Number of rows to generate. Default=100.
  -o, --output TEXT  (optional) name of file to write data into.
                     Default=console
  -u, --unique       (optional) All generated rows are unique
  -v, --verbose      Enables verbose logging mode
  -q, --quiet        Limits logging output to warnings and errors.  No summary
                     is displayed
  --help             Show this message and exit.
  ```

### Example - CSV 

```
poetry run python ./gendata.py random   -n 8  ./templates/simple.json
```

Will generate output: 
```
Col0,Col1,Col2
Value2_C,ValueA,Value_80perc_DEFAULT
Value2_C,ValueA,Value_20perc
Value2_A,ValueA,Value_80perc_DEFAULT
Value2_C,ValueA,Value_80perc_DEFAULT
Value2_C,ValueA,Value_80perc_DEFAULT
Value2_B,ValueA,Value_80perc_DEFAULT
Value2_C,ValueA,Value_80perc_DEFAULT
Value2_C,ValueA,Value_80perc_DEFAULT
```

### Example - JSON

```
poetry run python ./gendata.py random   -n 8  ./templates/simple.json --output my_output.json
```

Will generate output: 

```
[{"Col0": "Value2_C", "Col1": "ValueA", "Col2": "Value_20perc"}, {"Col0": "Value2_C", "Col1": "ValueA", "Col2": "Value_80perc_DEFAULT"}, {"Col0": "Value2_C", "Col1": "ValueA", "Col2": "Value_80perc_DEFAULT"}, {"Col0": "Value2_B", "Col1": "ValueA", "Col2": "Value_80perc_DEFAULT"}, {"Col0": "Value2_B", "Col1": "ValueA", "Col2": "Value_80perc_DEFAULT"}, {"Col0": "Value2_A", "Col1": "ValueA", "Col2": "Value_80perc_DEFAULT"}, {"Col0": "Value2_C", "Col1": "ValueA", "Col2": "Value_80perc_DEFAULT"}, {"Col0": "Value2_B", "Col1": "ValueA", "Col2": "Value_80perc_DEFAULT"}]
```

or formatted
```
[
  {
    "Col0": "Value2_C",
    "Col1": "ValueA",
    "Col2": "Value_80perc_DEFAULT"
  },
  {
    "Col0": "Value2_A",
    "Col1": "ValueA",
    "Col2": "Value_80perc_DEFAULT"
  },
  {
    "Col0": "Value2_B",
    "Col1": "ValueA",
    "Col2": "Value_20perc"
  },
  {
    "Col0": "Value2_C",
    "Col1": "ValueA",
    "Col2": "Value_20perc"
  },
  {
    "Col0": "Value2_C",
    "Col1": "ValueA",
    "Col2": "Value_20perc"
  },
  {
    "Col0": "Value2_C",
    "Col1": "ValueA",
    "Col2": "Value_80perc_DEFAULT"
  },
  {
    "Col0": "Value2_A",
    "Col1": "ValueA",
    "Col2": "Value_20perc"
  },
  {
    "Col0": "Value2_C",
    "Col1": "ValueA",
    "Col2": "Value_80perc_DEFAULT"
  }
]
```

## permutations command


```Usage: gendata.py permutations [OPTIONS] INPUT

  Generate a CSV with each permutation of columns and possible values. The
  probabilities are not considered.

Options:
  -o, --output TEXT  (optional) name of file to write data into.
                     Default=console
  -v, --verbose      Enables verbose logging mode
  -q, --quiet        Limits logging output to warnings and errors.  No summary
                     is displayed
  --help             Show this message and exit.
  ```
  
  ### Example

```poetry run python ./gendata.py permutations   ./templates/simple.json```

Will generate CSV output: 
```
Col0,Col1,Col2
Value2_A,ValueA,Value_20perc
Value2_A,ValueA,Value_80perc_DEFAULT
Value2_A,ValueB,Value_20perc
Value2_A,ValueB,Value_80perc_DEFAULT
Value2_B,ValueA,Value_20perc
Value2_B,ValueA,Value_80perc_DEFAULT
Value2_B,ValueB,Value_20perc
Value2_B,ValueB,Value_80perc_DEFAULT
Value2_C,ValueA,Value_20perc
Value2_C,ValueA,Value_80perc_DEFAULT
Value2_C,ValueB,Value_20perc
Value2_C,ValueB,Value_80perc_DEFAULT
```




# ToDo
 1. Support paired column values - multiple columns in same random group.   ex:    Name + SSN. 
 2. Support ranges of integers
 3. Support ranges of floats
 4. Add maxloops to prevent infinite loops if --unique parameter is used.  There may not be enough unique values to satisfy --num_rows
