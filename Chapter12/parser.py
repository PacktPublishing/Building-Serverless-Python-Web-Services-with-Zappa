import os


def doc_to_text(file_object):
    data = ''
    # save file in tmp
    filepath = os.path.join('/tmp', file_object.filename)
    with open(filepath, 'wb') as tmp_file:
        while True:
            chunk = file_object.file.read(4096)
            tmp_file.write(chunk)
            if not chunk:
                break

    # Parse and return text data
    with os.popen('./usr/bin/catdoc -a {0}'.format(filepath), 'r') as proc:
        data = proc.read()
    return data