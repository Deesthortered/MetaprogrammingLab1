import json

class GoHtmlCreator:
    # Global ##############
    def create_folder(self, path_list):
        for file in path_list:
            if file.split("/")[-1] == "readme.txt.html":
                self.build_readme(file)
            else:
                self.create_file(file)
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

        commented_single_consts_vars = []
        commented_many_consts_vars = []

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
                    commented_single_consts_vars.append(ptoken)
            elif ptoken[0] == 'variable':
                if not ptoken[4]:
                    uncommented_vars.append(ptoken)
                else:
                    commented_single_consts_vars.append(ptoken)
            elif ptoken[0] == 'const_arr':
                if not ptoken[4]:
                    uncommented_consts.append(ptoken)
                else:
                    commented_many_consts_vars.append(ptoken)
            elif ptoken[0] == 'variable_arr':
                if not ptoken[4]:
                    uncommented_vars.append(ptoken)
                else:
                    commented_many_consts_vars.append(ptoken)
            elif ptoken[0] == 'type':
                type_list.append((ptoken, []))
            elif ptoken[0] == 'function':
                if ptoken[1] != None:
                    type_t = list(filter(lambda t: t[0][2] == ptoken[1], type_list))[0]
                    type_t[1].append(ptoken)
                else:
                    func_list.append(ptoken)

        if package_name is not None:
            result_text += self.envelop_package(package_name)

        if import_list:
            result_text += self.envelop_imports(import_list)

        if overview != "":
            result_text += self.envelop_overview(overview)

        if uncommented_consts:
            result_text += self.envelop_uncommneted_consts(uncommented_consts)

        if uncommented_vars:
            result_text += self.envelop_uncommneted_vars(uncommented_vars)

        if commented_single_consts_vars:
            for c in commented_single_consts_vars:
                result_text += self.envelop_commented_single_consts_vars(c)

        if commented_many_consts_vars:
            for c in commented_many_consts_vars:
                result_text += self.envelop_commented_many_consts_vars(c)

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

    def envelop_commented_single_consts_vars(self, ptoken):
        before = \
            """
            <div class="alert alert-primary" role="alert"> <h3> Documented """ + ("variable" if ptoken[0] == "variable" else "constant") + """ </h3> </div>
            <div class="alert alert-light" role="alert">
            """
        after = \
            """
            </div>
            """

        content = "<h5>" + ptoken[3] + "</h5>"

        before1 = \
            """
            <div class="alert alert-light" role="alert">
            """
        after1 = \
            """
            </div>
            """

        content1 = ""
        for i in ptoken[4]:
            pref1 = "<p>"
            post1 = "</p>"
            content1 += pref1 + i + post1

        return before + content + after + before1 + content1 + after1

    def envelop_commented_many_consts_vars(self, ptoken):
        before = \
            """
            <div class="alert alert-primary" role="alert"> <h3> Documented """ + ("variables" if ptoken[0] == "variable_arr" else "constants") + """ </h3> </div>
            <div class="alert alert-light" role="alert">
            """
        after = \
            """
            </div>
            """

        pref = "<h5>"
        post = "</h5>"
        content = ("<h5>var (</h5>" if ptoken[0] == "variable_arr" else "<h5>const (</h5>")
        for i in ptoken[3]:
            content += pref + i + post
        content += "<h5>)</h5>"

        before1 = \
            """
            <div class="alert alert-light" role="alert">
            """
        after1 = \
            """
            </div>
            """

        content1 = ""
        for i in ptoken[4]:
            pref1 = "<p>"
            post1 = "</p>"
            content1 += pref1 + i + post1


        return before + content + after + before1 + content1 + after1

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

    def styles(self):
        return \
        """
            <style type="text/css">
              div.alert {
                margin: 15px;
              }
              div.alert-secondary {
                margin-left: 40px;
              }
            </style>
        """

    def final_envelop(self, body):
        envelop = \
            """
            <!doctype html>
            <html lang="en">
              <head>
                <!-- Required meta tags -->
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                
                <!-- Bootstrap CSS -->
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
                
                {styles}
                
                <title>Hello, world!</title>
              </head>
              <body>
              
                {body_html}
              
                <!-- Optional JavaScript -->
                <!-- jQuery first, then Popper.js, then Bootstrap JS -->
                <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
                <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
              </body>
            </html>
            """.format(styles=self.styles(), body_html=body)

        return envelop

    # For readme
    def build_readme(self, path):
        file = open(path, encoding='utf-8', mode='r')
        pref = path[:self.char_occur(path, '/')[-1]]
        references = []
        line = None
        while line != "end":
            line = file.readline().strip()
            references.append('.' + line[len(pref):])
            pass
        references.pop()
        raw_overview = file.read()
        file.close()

        if raw_overview == '':
            raw_overview = "[\"There is no overview\"]"

        overview_page = self.build_overview(json.loads(raw_overview), path.split('/')[-2])
        ref_page = self.build_references(references)

        final_text = self.final_envelop(overview_page + ref_page)
        file = open(path, encoding='utf-8', mode='w')
        file.write(final_text)
        file.close()

    def char_occur(self, in_string, char_val):
        return [i for i, letter in enumerate(in_string) if letter == char_val]

    def build_references(self, reference_list):
        dir_list = []
        file_list = []
        for reference in reference_list:
            if len(reference) >= 8 and reference[-8:] == '.go.html':
                file_list.append(reference)
            else:
                dir_list.append(reference)

        result_text = ""

        before_code = \
            """
            <div class="alert alert-secondary" role="alert">
            """
        after_code = \
            """
            </div>
            """

        before = \
            """
            <div class="alert alert-light" role="alert">\n
            """
        after = \
            """
            </div>\n
            """

        result_text += before_code

        if dir_list:
            result_text += "<h3> {title} </h3>".format(title="Direstories")
            result_text += before
            for reference in dir_list:
                result_text += """ <a class="nav-link active" href="{ref}"> {title} </a> \n"""\
                    .format(ref=reference + "/readme.txt.html",
                            title=reference.split("/")[-1])
            result_text += after

        if file_list:
            result_text += "<h3> {title} </h3>".format(title="Files")
            result_text += before
            for reference in file_list:
                result_text += """ <a class="nav-link active" href="{ref}"> {title} </a> \n"""\
                    .format(ref=reference,
                            title=reference.split("/")[-1])
            result_text += after

        if not dir_list and not file_list:
            result_text += "<h5> {title} </h5>".format(title="There is not references.")

        result_text += after_code

        return result_text

    def build_overview(self, text_list, name):
        title = \
            """ <div class="alert alert-primary" role="alert"> <h3> Directory overview ({dir_name}) </h3> </div> \n"""\
            .format(dir_name=name)

        before = \
            """
            <div class="alert alert-secondary" role="alert">\n
            """
        after = \
            """
            </div>\n
            """

        content = ""
        for line in text_list:
            content += "<p> {h_line} </p>\n"\
                .format(h_line=line.strip())

        return title + before + content + after
