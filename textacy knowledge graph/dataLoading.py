import re
import pandas as pd

class DataLoader:
    def load_text_from_file(self, filepath, col="tokens"):
        def remove_parenthesis_and_spaces_around_fullstops(text):
            text = re.sub(r'\s*[\(\[]\s*.*?\s*[\)\]]\s*', '', text)
            text = re.sub(r'\s+\.', '.', text)
            text = re.sub(r'\.(\s+)', '.', text)
            text = re.sub(r'\.{2,}', '.', text)
            text = re.sub(r'\.', '. ', text)
            text = re.sub(r'\s+,', ',', text)
            return text

        tokens = pd.read_parquet(filepath)[col][:5]
        str_list = []
        for token in tokens:
            str_list.append(" ".join(token))
        result = "".join(str_list)
        result = remove_parenthesis_and_spaces_around_fullstops(result)
        return result

    def load_text_lists_from_file(self,filepath,col="tokens"):
        def remove_parenthesis_and_spaces_around_fullstops(text):
            text = re.sub(r'\s*[\(\[]\s*.*?\s*[\)\]]\s*', '', text)
            text = re.sub(r'\s+\.', '.', text)
            text = re.sub(r'\.(\s+)', '.', text)
            text = re.sub(r'\.{2,}', '.', text)
            text = re.sub(r'\.', '. ', text)
            text = re.sub(r'\s+,', ',', text)
            return text

        tokens = pd.read_parquet(filepath)[col][:5]
        result = []
        for token in tokens:
            result.append(" ".join(token))

        result = [remove_parenthesis_and_spaces_around_fullstops(txt) for txt in result]
        return result