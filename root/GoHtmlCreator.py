import json

class GoHtmlCreator:
    # Global ##############
    def create_folder(self, path_list):

        pass

    def create_file(self, file_path):
        file = open(file_path, encoding='utf-8', mode='r')
        token_set = json.loads(file.read())
        file.close()
        file = open(file_path, encoding='utf-8', mode='w')

        package_name = None
        import_list = None
        overview = ""
        indexes = None
        items = None  # (type, depency, title, code, description)

        result_text = ""

        for ptoken in token_set:
            if ptoken[0] == 'File overview':
                for line in ptoken[1]:
                    overview += line + "\n"
                overview += '\n\n'
            elif ptoken[0] == 'package':
                package_name = ptoken[2]
            elif ptoken[0] == 'imports':
                pass
            elif ptoken[0] == 'constant':
                pass
            elif ptoken[0] == 'variable':
                pass
            elif ptoken[0] == 'const_arr':
                pass
            elif ptoken[0] == 'variable_arr':
                pass
            elif ptoken[0] == 'const_arr':
                pass
            elif ptoken[0] == 'type':
                pass
            elif ptoken[0] == 'function':
                pass

            print(ptoken)

        if package_name != None:
            result_text += self.envelop_package(package_name)

        if overview != "":
            result_text += self.envelop_overview(overview)

        file.write(self.final_envelop(result_text))
        file.close()
        pass
    #######################

    # Local ###############
    def envelop_package(self, text):
        before = \
            """
            <h1>
            """
        after = \
            """
            </h1>
            """
        text = text[:1].upper() + text[1:]
        return before + text + after

    def envelop_overview(self, text):
        before = \
            """
            <div class="alert alert-primary" role="alert"> Overview </div>
            <div class="alert alert-light" role="alert">
            """
        after = \
            """
            </div>
            """

        content = ""
        for i in text.split("\n\n"):
            pref = "<p>"
            post = "</p>"
            content += pref + i + post

        return before + content + after

    def final_envelop(self, text):
        before = \
            """
            <!doctype html>
            <html lang="en">
              <head>
                <!-- Required meta tags -->
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                
                <!-- Bootstrap CSS -->
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
                <style type="text/css">
                  div.alert {
                      margin: 15px;
                  }
                </style>
    
                <title>Hello, world!</title>
              </head>
              <body>
            """

        after = \
            """
                <!-- Optional JavaScript -->
                <!-- jQuery first, then Popper.js, then Bootstrap JS -->
                <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
                <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
              </body>
            </html>
            """
        return before + text + after
