import json

class GoHtmlCreator:
    # Global ##############
    def create_folder(self, path_list):

        pass

    def create_file(self, file_path):
        file = open(file_path, 'r')
        token_set = json.loads(file.read())
        file.close()
        file = open(file_path, 'w')

        package_name = None
        import_list = None
        overview = None
        indexes = None
        items = None  # (type, depency, title, code, description)

        for t in token_set:
            print(t)

        file.close()
        pass
    #######################

    # Local ###############
    def final_envelop(self, text):
        before =    '<!doctype html>\n' + \
                    '<html lang="en">\n' + \
                    '  <head>\n' + \
                    '    <!-- Required meta tags -->\n' + \
                    '    <meta charset="utf-8">\n' + \
                    '    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">\n' + \
                    '\n' + \
                    '    <!-- Bootstrap CSS -->\n' + \
                    '    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">\n' + \
                    '\n' + \
                    '    <title>Hello, world!</title>\n' + \
                    '  </head>\n' + \
                    '  <body>\n' + \
                    '\n'
        after =     '\n' + \
                    '\n' + \
                    '    <!-- Optional JavaScript -->\n' + \
                    '    <!-- jQuery first, then Popper.js, then Bootstrap JS -->\n' + \
                    '    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>\n' + \
                    '    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>\n' + \
                    '    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>\n' + \
                    '  </body>\n' + \
                    '</html>\n'
        return before + text + after
