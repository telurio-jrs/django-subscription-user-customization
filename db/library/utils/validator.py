import re


class Validator:
    def valid_special_chars(self, password):
        regex = r'^[a-zA-Z0-9-!@#$%^&*()_+\-=\[\]{}\\|,.<>\/?~]*$'
        if not re.search(regex, password):
            return 'Password cannot contain disallowed characters. e.g. ";".'
