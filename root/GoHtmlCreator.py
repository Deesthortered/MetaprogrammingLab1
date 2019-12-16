import json
from datetime import date

class GoHtmlCreator:
    # Global ##############
    def create_folder(self, path_list, root_dest):
        self.build_main_page(root_dest, path_list)
        for file in path_list:
            if file.split("/")[-1] == "readme.txt.html":
                self.build_readme(file)
            elif len(file) >= 8 and file[-8:] == ".go.html":
                self.create_file(file)

    def create_file(self, file_path):
        file = open(file_path, encoding='utf-8', mode='r')
        json_data = file.read().strip()
        file.close()

        if json_data == "":
            print("Empty json for file")
            return

        token_set = json.loads(json_data)
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
                    type_t = list(filter(lambda t: t[0][2] == ptoken[1], type_list))
                    if len(type_t) > 0:
                        type_t = type_t[0]
                        type_t[1].append(ptoken)
                    else:
                        func_list.append(ptoken)
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
        anchor = "type_" + type[0][2]
        before_desc = \
            """
            <div class="alert alert-primary" role="alert" id=\"{anchor_id}\"> <h3> type {type} </h3> </div>
            <div class="alert alert-light" role="alert">
            """\
                .format(anchor_id=anchor, type=type[0][2])

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
        title = """ <div class="alert alert-light" role="alert" id=\"{anchor_id}\"> <h3> {func_name} </h3> </div> """\
            .format(func_name=ptoken[2], anchor_id=self.get_func_anchor(ptoken))

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
        title = """ <div class="alert alert-primary" role="alert" id=\"{anchor_id}\"> <h3> {func_name} </h3> </div> """\
            .format(func_name=ptoken[2], anchor_id=self.get_func_anchor(ptoken))

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
                margin-left: 15px;
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

    # Main page
    def build_main_page(self, root_path, path_list):
        header_content = self.print_header(root_path)
        ierarchy_code = self.make_ierarchy(root_path, path_list)
        alphabet_code = self.make_alphabet(path_list, root_path)

        content = header_content + ierarchy_code + alphabet_code
        result_code = self.final_envelop(content)

        file = open(root_path + "/main.html", encoding='utf-8', mode='w')
        file.write(result_code)
        file.close()

    def make_ierarchy(self, root_path, path_list):
        prefix_ind = len(root_path.split('/')) - 1
        ierarchy = self.go_dfs_ierarchy(path_list, root_path[self.char_occur(root_path, '/')[-1]+1:], prefix_ind)
        code = self.print_ierarchy(ierarchy, True, prefix_ind)
        title = \
            """ <div class="alert alert-primary" role="alert"> <h3> Directory ierarchy </h3> </div> \n"""
        return title + code

    def go_dfs_ierarchy(self, path_list, dir_name, depth):
        result_d = [[], dir_name]
        tmp_deeper = []
        dir_dic = {}
        for i in path_list:
            path = i[self.char_occur(i, '/')[depth]:]
            depth_remains = len(self.char_occur(path, '/'))
            if depth_remains == 1:
                result_d[0].append(i)
            else:
                cur_dir_name = i[self.char_occur(i, '/')[depth]+1:self.char_occur(i, '/')[depth+1]]
                if not (cur_dir_name in dir_dic):
                    dir_dic[cur_dir_name] = [[], cur_dir_name]
                    tmp_deeper.append(dir_dic[cur_dir_name])
                dir_dic[cur_dir_name][0].append(i)

        for sub_list in tmp_deeper:
            sub_res = self.go_dfs_ierarchy(sub_list[0], sub_list[1], depth+1)
            result_d[0].append(sub_res)

        return result_d
    def print_ierarchy(self, cur_ierarchy, tiktok, depth):
        before = None
        after = None
        if tiktok:
            before = \
                """
                <div class="alert alert-secondary" role="alert">\n
                """
            after = \
                """
                </div>\n
                """
        else:
            before = \
                """
                <div class="alert alert-light" role="alert">\n
                """
            after = \
                """
                </div>\n
                """

        content = "<h5> {dir_name} </h5>\n"\
            .format(dir_name=cur_ierarchy[1])

        after_list = []
        for i in cur_ierarchy[0]:
            if isinstance(i, list):
                content += self.print_ierarchy(i, not tiktok, depth)
            else:
                after_list.append(i)

        for i in after_list:
            cur_ref = "." + i[self.char_occur(i, '/')[depth]:]
            cur_content = i[self.char_occur(i, '/')[-1]+1:]
            line = "<p> <a href=\"{ref}\"> {content} </a> </p>\n"\
                .format(ref=cur_ref, content=cur_content)
            content += line

        return before + content + after

    def make_alphabet(self, path_list, root_path):
        element_list = []
        for file in path_list:
            if len(file) >= 8 and file[-8:] == '.go.html':
                f_d = open(file, encoding='utf-8', mode='r')
                json_text = f_d.read()
                f_d.close()
                tmp_list = json.loads(json_text)
                for i in tmp_list:
                    i.append(file)
                element_list += tmp_list

        element_list = list(filter(lambda x: x[0] != 'File overview' and
                                             x[0] != 'variable_arr' and
                                             x[0] != 'variable' and
                                             x[0] != 'const_arr' and
                                             x[0] != 'constant' and
                                             x[0] != 'package' and
                                             x[0] != 'imports', element_list))

        element_list.sort(key=lambda x: x[2][self.char_occur(x[2], ' ')[-1]+1:].casefold()
                            if len(self.char_occur(x[2], ' ')) > 0
                            else x[2].casefold())

        prefix_ind = len(root_path.split('/')) - 1
        return self.print_alphabet(element_list, prefix_ind)

    def print_alphabet(self, element_list, depth):
        title = \
            """ <div class="alert alert-primary" role="alert"> <h3> Alphabet </h3> </div> \n"""
        before = \
            """
            <div class="alert alert-light" role="alert">\n
            """
        after = \
            """
            </div>\n
            """

        content = ""
        for i in element_list:
            cur_ref = "." + i[-1][self.char_occur(i[-1], '/')[depth]:]
            if i[0] == "type":
                cur_content = "type " + i[2]
            else:
                cur_content = i[2]

            if i[0] == 'type':
                cur_anchor = "type_"+i[2]
            elif i[0] == 'function':
                cur_anchor = self.get_func_anchor(i)
            content += "<h5> <a href=\"{ref}#{anchor}\"> {text} </a> </h5> \n" \
                .format(ref=cur_ref, anchor=cur_anchor, text=cur_content)

        return title + before + content + after

    def print_header(self, root_name1):
        root_name = ""
        if len(self.char_occur(root_name1, '/')) > 0:
            root_name = root_name1[self.char_occur(root_name1, '/')[-1]+1:]
        else:
            root_name = root_name1
        project_name = root_name[:1].upper() + root_name[1:]
        project_version = "v0.01"
        date_of_generation = date.today()
        parser_name = "SuperGoDocumenter"

        title = \
            """ <div class="alert alert-primary" role="alert"> <h2> {name} </h2> </div> \n"""\
            .format(name=project_name)

        before = \
            """
            <div class="alert alert-light" role="alert">\n
            """
        after = \
            """
            </div>\n
            """

        content = "<h5> Project version: {version} </h5>\n" \
                  "<h5> Date of creation: {date} </h5>\n" \
                  "<h5> Parser: {parser} </h5>\n"\
            .format(version=project_version, date=date_of_generation, parser=parser_name)

        return title + before + content + after

    def get_func_anchor(self, func_token):
        res = func_token[3].replace(' ', '_').strip()
        res = res.replace('(', '_')
        res = res.replace(')', '_')
        res = res.replace('*', '_')
        res = res.replace(',', '_')
        res = res.replace('.', '_')
        return res

