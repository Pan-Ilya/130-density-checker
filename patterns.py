right_sborka_name_pattern = r'(?i)(?P<SborkaID>\d{5}).*?' \
                            r'(?P<quantity>\d{2,}).*?' \
                            r'(?P<size>\d{2,}[xх]\d{2,}).*?' \
                            r'(?P<density>\d{2,})'

right_filename_pattern = r'(?i)(?P<date>\d{2}-\d{2})_.*?' \
                         r'(?P<OrderID>\d+)_.*?' \
                         r'(?P<size>\d+[xх]\d+)_.*?' \
                         r'(?P<color>\d\+\d)_.*?' \
                         r'(?P<density>\d{2,}(?:[a-z])*)_.*?' \
                         r'(?:(?P<lam>[a-z]{2,3}\d\+\d)|.)*?' \
                         r'(?P<quantity>[\d ]{3,}).*?' \
                         r'(?P<file_format>\.pdf)'
