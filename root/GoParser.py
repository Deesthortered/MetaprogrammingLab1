import os
import json

class GoParser:
    # Global
    def start_folder(self, input_folder_path, destination_folder_path):
        prefix_ind = len(input_folder_path.split('/')) - 1
        os.makedirs(destination_folder_path)
        file_list = self.go_throw_directory(input_folder_path, destination_folder_path, prefix_ind)


        for pair in file_list:
            if pair[0][-3:] == ".go":
                self.start_file(pair[0], pair[1])
            elif pair[0].split('/')[-1] == "readme.txt":
                doc_file1 = open(pair[0], "r")
                doc_file2 = open(pair[1], "a")
                doc_file2.write("end\n")
                doc_file2.write(json.dumps(doc_file1.readlines(), indent=2))
                doc_file1.close()
                doc_file2.close()
            elif pair[0] == "":
                doc_file2 = open(pair[1], "a")
                doc_file2.write("end\n")
                doc_file2.close()
            else:
                print("Error!")
        return [x[1] for x in file_list]

    def start_file(self, input_file_path, destination_file_path):
        input_file = open(input_file_path, encoding='utf-8', mode='r')
        middle_data = self.parse_file(input_file)
        input_file.close()
        output_file = open(destination_file_path, encoding='utf-8', mode='a')
        json_str = json.dumps(middle_data, indent=2)
        output_file.write(json_str)
        output_file.close()
        pass

    # Directory handling ##
    def char_occur(self, in_string, char_val):
        return [i for i, letter in enumerate(in_string) if letter == char_val]

    def go_throw_directory(self, current_path, destination_folder_path, prefix_ind):
        new_folder_path = destination_folder_path + current_path[self.char_occur(current_path, '/')[1]:]
        os.makedirs(new_folder_path)
        f = open(new_folder_path + "/readme.txt.html", "a+")
        f.close()

        node_list = os.listdir(current_path)
        nested_items = []
        for i in node_list:
            node = current_path + "/" + i
            if os.path.isfile(node):
                new_file_path = destination_folder_path + current_path[self.char_occur(current_path, '/')[1]:] + "/" + node.split('/')[-1] + ".html"
                nested_items.append((node, new_file_path))
                f1 = open(new_file_path, "a+")
                f1.close()
                f2 = open(new_folder_path + "/readme.txt.html", "a+")
                f2.write(new_file_path + "\n")
                f2.close()
            elif os.path.isdir(node):
                nested_files = self.go_throw_directory(node, destination_folder_path, prefix_ind)
                f = open(new_folder_path + "/readme.txt.html", "a+")
                for j in nested_files:
                    f.write(j[1] + "\n")
                f.close()
                nested_items = nested_items + nested_files
        if "readme.txt" not in node_list:
            f = open(new_folder_path + "/readme.txt.html", "a+")
            nested_items.append(("", new_folder_path + "/readme.txt.html"))
            f.close()
        return nested_items
    #######################

    # Parsing #############
    def parse_file(self, file):
        # Result
        result_set = []

        # clear start empty lines
        lines = file.readlines()
        while lines[0].rstrip() == "":
            lines = lines[1:]

        comment_queue = []
        type_struct_set = []
        was_begin = True

        general_size = len(lines)
        i = -1
        while i < general_size-1:
            i += 1
            dirty_line = lines[i]
            line = dirty_line.strip()

            if self.line_is_comment(line):
                #
                comment_queue.append(self.strip_comment_line(line))
            elif self.line_is_long_comment(line):
                if line != "/*" and line != "*/":
                    comment_queue.append(line)
            else:
                if was_begin and line == "":
                    result_set.append(("File overview", comment_queue))
                    comment_queue = []
                    continue
                if line != "":
                    was_begin = False

                if self.first_word(line) == "func":
                    have_pointer = False
                    if self.second_word(line)[0] == "(":
                        have_pointer = True

                    if have_pointer:
                        pointer_param = line[self.char_occur(line, '(')[0]+1:self.char_occur(line, ')')[0]].split(',')[0]
                        first_param_type = pointer_param[self.char_occur(pointer_param, '*')[0] + 1:]
                        func_title = "func (*" + first_param_type + ")" + line[self.char_occur(line, ')')[0]+1:self.char_occur(line, '(')[1]]
                        result_set.append(("function", first_param_type, func_title, line[:self.char_occur(line, '{')[0]-1], comment_queue))
                    else:
                        func_title = "func " + self.second_word(line)[:self.char_occur(self.second_word(line), '(')[0]]
                        result_set.append(("function", None, func_title, line[:self.char_occur(line, '{')[0]-1], comment_queue))

                    bracers_count = 0
                    bracers_count += len(self.char_occur(line, '{'))
                    bracers_count -= len(self.char_occur(line, '}'))
                    while bracers_count != 0:
                        i += 1
                        dirty_line = lines[i]
                        line = dirty_line.strip()
                        bracers_count += len(self.char_occur(line, '{'))
                        bracers_count -= len(self.char_occur(line, '}'))

                elif self.first_word(line) == "package":
                    #
                    result_set.append(("package", None, line, line, comment_queue))
                elif self.first_word(line) == "const":
                    if self.second_word(line) == "(":
                        const_set = []
                        j = i + 1
                        sub_line = lines[j]
                        while sub_line.strip() != ")":
                            const_set.append(sub_line.strip())
                            j += 1
                            sub_line = lines[j]
                        result_set.append(("const_arr", None, "Constants", const_set, comment_queue))
                    else:
                        result_set.append(("constant", None, self.second_word(line), line, comment_queue))
                elif self.first_word(line) == "var":
                    if self.second_word(line) == "(":
                        var_set = []
                        j = i + 1
                        sub_line = lines[j]
                        while sub_line.strip() != ")":
                            var_set.append(sub_line.strip())
                            j += 1
                            sub_line = lines[j]
                        result_set.append(("variable_arr", None, "Variables", var_set, comment_queue))
                    else:
                        result_set.append(("variable", None, self.second_word(line), line, comment_queue))
                elif self.first_word(line) == "type" and line[-1] == "{":
                    type_set = [line]
                    j = i + 1
                    sub_line = lines[j]
                    while sub_line.strip() != "}":
                        type_set.append(sub_line.strip())
                        j += 1
                        sub_line = lines[j]
                    type_set.append(sub_line.strip())
                    type_struct_set.append(self.second_word(type_set[0]))
                    result_set.append(("type", None, self.second_word(type_set[0]), type_set, comment_queue))
                elif self.first_word(line) == "import":
                    import_set = []
                    j = i + 1
                    sub_line = lines[j]
                    while sub_line.strip() != ")":
                        import_set.append(sub_line.strip())
                        j += 1
                        sub_line = lines[j]
                    result_set.append(("imports", None, "Imports", import_set, comment_queue))

                comment_queue = []
        return result_set

    def line_is_comment(self, line):
        return len(line) >= 2 and line[0] == line[1] == '/'

    long_comment_memory = False

    def line_is_long_comment(self, line):
        if line == "/*":
            self.long_comment_memory = True
            return True
        elif line == "*/":
            self.long_comment_memory = False
            return True
        return self.long_comment_memory

    def strip_comment_line(self, line):
        if len(line) < 3:
            return ""
        elif line[2] == " ":
            return line[3:]
        return line[2:]

    def first_word(self, line):
        return line.split(' ', 1)[0]

    def second_word(self, line):
        return line.split(' ')[1]
    #######################