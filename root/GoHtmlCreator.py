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
        import_list = []
        overview = ""
        type_list = []
        func_list = []

        uncommented_consts = []
        uncommented_vars = []

        result_text = ""
        for ptoken in token_set:  # (type, depency, title, code, description)
            if ptoken[0] == 'File overview':
                for line in ptoken[1]:
                    overview += line + "\n"
                overview += '\n\n'
            elif ptoken[0] == 'package':
                package_name = (ptoken[2], ptoken[4])
            elif ptoken[0] == 'imports':
                for i in ptoken[3]:
                    import_list.append(i)
            elif ptoken[0] == 'constant':
                if not ptoken[4]:
                    uncommented_consts.append(ptoken)
                else:
                    pass
            elif ptoken[0] == 'variable':
                if not ptoken[4]:
                    uncommented_vars.append(ptoken)
                else:
                    pass
            elif ptoken[0] == 'const_arr':
                if not ptoken[4]:
                    uncommented_consts.append(ptoken)
                else:
                    pass
            elif ptoken[0] == 'variable_arr':
                if not ptoken[4]:
                    uncommented_vars.append(ptoken)
                else:
                    pass
            elif ptoken[0] == 'type':
                type_list.append((ptoken, []))
            elif ptoken[0] == 'function':
                if ptoken[1] != None:
                    type_t = list(filter(lambda t: t[0][2] == ptoken[1], type_list))[0]
                    type_t[1].append(ptoken)
                else:
                    func_list.append(ptoken)

            print(ptoken)

        if package_name != None:
            result_text += self.envelop_package(package_name)

        if import_list:
            result_text += self.envelop_imports(import_list)

        if overview != "":
            result_text += self.envelop_overview(overview)

        if uncommented_consts:
            result_text += self.envelop_uncommneted_consts(uncommented_consts)

        if uncommented_vars:
            result_text += self.envelop_uncommneted_vars(uncommented_vars)

        if type_list:
            for type in type_list:
                result_text += self.envelop_type(type)

        if func_list:
            for func_token in func_list:
                result_text += self.envelop_function(func_token)

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
        text1 = text[0][:1].upper() + text[0][1:]

        before1 = \
            """
            <div class="alert alert-light" role="alert">
            """
        after1 = \
            """
            </div>
            """

        content = ""
        for i in text[1]:
            pref = "<p>"
            post = "</p>"
            content += pref + i + post

        return before + text1 + after + before1 + content + after1

    def envelop_imports(self, import_list):
        before = \
            """
            <div class="alert alert-primary" role="alert"> <h3> Imports </h3> </div>
            <div class="alert alert-light" role="alert">
            """
        after = \
            """
            </div>
            """

        content = ""
        for i in import_list:
            pref = "<h5>"
            post = "</h5>"
            content += pref + i + post

        return before + content + after

    def envelop_overview(self, text):
        before = \
            """
            <div class="alert alert-primary" role="alert"> <h3> Overview </h3> </div>
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

    def envelop_uncommneted_consts(self, token_list):
        before = \
            """
            <div class="alert alert-primary" role="alert"> <h3> Undocumented constants </h3> </div>
            <div class="alert alert-light" role="alert">
            """
        after = \
            """
            </div>
            """

        content = ""
        for i in token_list:
            pref = "<h5>"
            post = "</h5>"
            if isinstance(i[3], list):
                for j in i[3]:
                    content += pref + j + post
            else:
                content += pref + i[3] + post

        return before + content + after

    def envelop_uncommneted_vars(self, token_list):
        before = \
            """
            <div class="alert alert-primary" role="alert"> <h3> Undocumented variables </h3> </div>
            <div class="alert alert-light" role="alert">
            """
        after = \
            """
            </div>
            """

        content = ""
        for i in token_list:
            pref = "<h5>"
            post = "</h5>"
            if isinstance(i[3], list):
                for j in i[3]:
                    content += pref + j + post
            else:
                content += pref + i[3] + post

        return before + content + after

    def envelop_type(self, type):
        before_desc = \
            """
            <div class="alert alert-primary" role="alert"> <h3> type """ + type[0][2] + """ </h3> </div>
            <div class="alert alert-light" role="alert">
            """
        after_desc = \
            """
            </div>
            """

        desc_content = ""
        for i in type[0][4]:
            desc_content += "<p>" + i + "</p>"

        descrition = before_desc + desc_content + after_desc

        before_code = \
            """
            <div class="alert alert-secondary" role="alert">
            """
        after_code = \
            """
            </div>
            """
        cont_code = ""
        for i in type[0][3]:
            cont_code += "<p>" + i + "</p>"
        code = before_code + cont_code + after_code

        sub_func = ""
        for func in type[1]:
            sub_func += self.envelop_sub_sunction(func)

        return descrition + code + sub_func

    def envelop_sub_sunction(self, ptoken):
        title = """ <div class="alert alert-light" role="alert"> <h3> """ + ptoken[2] + """ </h3> </div> """

        before_code = \
            """
            <div class="alert alert-secondary" role="alert">
            """
        after_code = \
            """
            </div>
            """
        code = before_code + ptoken[3] + after_code

        before_desc = \
            """
            <div class="alert alert-light" role="alert">
            """
        after_desc = \
            """
            </div>
            """
        desc_content = ""
        for i in ptoken[4]:
            desc_content += "<p>" + i + "</p>"

        return title + code + before_desc + desc_content + after_desc

    def envelop_function(self, ptoken):
        title = """ <div class="alert alert-primary" role="alert"> <h3> """ + ptoken[2] + """ </h3> </div> """

        before_code = \
            """
            <div class="alert alert-secondary" role="alert">
            """
        after_code = \
            """
            </div>
            """
        code = before_code + ptoken[3] + after_code

        before_desc = \
            """
            <div class="alert alert-light" role="alert">
            """
        after_desc = \
            """
            </div>
            """
        desc_content = ""
        for i in ptoken[4]:
            desc_content += "<p>" + i + "</p>"

        return title + code + before_desc + desc_content + after_desc

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
                  };
                  div.alert-secondary {
                      margin: 40px;
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
