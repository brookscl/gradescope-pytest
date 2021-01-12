'''
This utility program transforms the output of a pytest json file to a gradescope json file format.
The output of pytest is generated using the pytest-json module with the command line

pytest --json=report.json

Next this utility program is run with command line

python3 pytest2gs.py report.json results.json

The user must specify both files or neither. If no arguments are given,
the program defaults to these two file names for convenience.
If the number of files specified is 1 or greater than 2, print a usage
message and exit.

Author: George Rudolph
Date: 11 Mar 2020
(c) George Rudolph 2020

Permission is granted to copy, use and modify this file without restriction.
This version of the file is not meant to be loaded as a module in another
program, and may not work correctly if it is loaded that way.

If the json module changes it's output format or gradecope
changes it's required json format, this utility program will need
to change accordingly.

TODO: Figure out the notion of actual score.
For example at UVU, the code portion of this project is worth 80 points,
so the actual score should be a percentage of 80 points.
But pytest and pytest-json have no notion of points at all, and points is
a grading thing, not a testing thing.
'''
import json
from sys import argv


def usage():
    print("Usage: python pytest2gs.py [input file name] [output file name]")
    print("You must specify both file names or neither.")


def translate(result):
    ''' Translate a pytest-json test result entry to a gs entry.
    For each gs test item, we want a score, a max score, the name and the test number.
    From pytest json these respectively correspond to 0 [outcome failed] or 1 [outcome passed], 1, the name field and the run_index.
    dict -> dict
    '''
    gs_result = {}

    keywords = result['keywords']
    weight = float(get_keyword_value(keywords, 'weight', 1))
    name = get_keyword_value(keywords, 'name', None)
    if name:
        name = name.replace('_', ' ')

    gs_result['visibility'] = get_keyword_value(keywords, 'visibility', 'visible')
    gs_result['score'] = weight if result['outcome'] == 'passed' else 0.0
    gs_result['max_score'] = weight
    gs_result['name'] = name or result['nodeid']
    gs_result['number'] = str(get_keyword_value(keywords, 'number', result['lineno']))

    return gs_result


def get_keyword_value(keywords, name, default):
    values = [keyword for keyword in keywords if f"{name}_" in keyword.lower()]
    return values[0][values[0].find('_')+1:] if values else default


def main():
    ''' program starts here '''

    input_file_name = 'report.json'
    output_file_name = 'results.json'

    num_params = len(argv) - 1
    if num_params == 1 or num_params > 2:
        usage()
        return

    if num_params == 2:
        input_file_name = argv[1]
        output_file_name = argv[2]

    fin = open(input_file_name)
    report_data = json.load(fin)
    fin.close()
    # print(json.dumps(report_data['tests'], indent = 4, sort_keys=True))

    gs_results = {}
    # ''' total score field: gs score '''
    # passed = int(report_data['summary']['passed'])
    # num_tests = int(report_data['summary']['total'])
    # score = int(100 * float(passed) / float(num_tests))
    # print(score)
    # gs_results['score'] = score

    ''' gs execution time corrsponds to total duration from report field '''
    # gs_results['execution_time'] = report_data['duration']

    test_results = report_data['tests']
    gs_results['tests'] = [translate(result) for result in test_results]

    fout = open(output_file_name, 'w')
    # json.dump(gs_results, fout, indent=4, sort_keys=True)
    json.dump(gs_results, fout)
    fout.close()


if __name__ == "__main__":
    main()
