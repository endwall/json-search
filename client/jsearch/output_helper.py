"""Helper class for output console."""
import json


class OutputHelper(object):
    """Allow different output format of search result."""

    def output_json(self, input_json, format='json'):
        """Print json, can be different format."""
        if format == 'json':
            print(json.dumps(input_json, indent=4))
        elif format == 'table':
            i = 1
            for doc in input_json:
                print("===" + str(i) + "===")
                for key in doc:
                    print (key + ": \t" + str(doc[key]))
                i = i + 1
        else:
            print(json.dumps(input_json, indent=4))
