import json
import base64
import random 
import re, io


def is_bs64_regex(s):
    if re.match('^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4})$', s):
        return True
    return False

def convert_bs64_io_buffer(b, filename, extension):
    buffered_reader = io.BufferedReader(io.BytesIO(base64.b64decode(b)))
    return (filename, buffered_reader, extension)

def parse(value):
    return convert_bs64_io_buffer(value.split(',')[-1], 
           ("%x" % random.getrandbits(128))[:10] + '.' + value.split(',')[0].split(';')[0].split('/')[1], 
            value.split(',')[0].split(';')[0])
    
    
def multipart_form(form):
    data = {}
    files = []
    for key, value in form.items():
        try:
            if isinstance(value, list):
                if isinstance(value[0], str):
                    if is_bs64_regex(value[0].split(',')[-1]) and bool(len(value[0].split(',')) - 1):
                        for item in value:
                            files.append((str(key), parse(item)))
                    else: data[str(key)] = [item for item in value]
                else: data[str(key)] = [item for item in value]
            else:  
                if isinstance(value, str):
                    if is_bs64_regex(value.split(',')[-1]) and bool(len(value.split(',')) - 1):
                        files.append((str(key), parse(value)))
                    else: data[str(key)] = value     
                else: data[str(key)] = value
        except Exception as e:
            print(e)
            data['erros'] = str(key)
            pass
                    
    print(data.keys())
    print(files)
    return data, files
    
def update_pycache():
    return "ok", 200

if __name__ == "__main__":
    #read all txt in this folder and convert to json
    with open('01-04-2024 09-25.txt', 'r') as file:
    # Read the contents of the file
        data_string = file.read()
        data_dict = json.loads(data_string)   
        multipart_form(data_dict)
        
    # print(multipart_form({"nome": "teste", "foto": ["data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=", "data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="]}))
    # print(multipart_form({"nome": "teste", "foto": "data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="}))
    