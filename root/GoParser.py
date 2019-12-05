import os


class GoParser:
    # Global

    def start_folder(self, input_folder_path, destination_folder_path):
        prefix_ind = len(input_folder_path.split('/')) - 1
        self.go_throw_directory(input_folder_path, destination_folder_path, prefix_ind)
        pass

    def start_file(self, input_file_path, destination_file_path):
        input_file = open(input_file_path, encoding='utf-8', mode='r')
        self.parse_file(input_file)

        input_file.close()
        pass

    # Directory handling
    def char_occur(self, in_string, char_val):
        return [i for i, letter in enumerate(in_string) if letter == char_val]

    def go_throw_directory(self, current_path, destination_folder_path, prefix_ind):
        node_list = os.listdir(current_path)
        for i in node_list:
            node = current_path + "/" + i
            if os.path.isfile(node):
                new_file_path = destination_folder_path + current_path[self.char_occur(current_path, '/')[1]:] + "/" + node.split('/')[-1]
            elif os.path.isdir(node):
                new_folder_path = destination_folder_path + current_path[self.char_occur(current_path, '/')[1]:] + "/" + node.split('/')[-1]
                self.go_throw_directory(node, destination_folder_path, prefix_ind)

    # Parsing

    def parse_file(self, file):
        # Result
        result_set = []

        # clear start empty lines
        lines = file.readlines()
        while lines[0].rstrip() == "":
            lines = lines[1:]

        comment_queue = []
        was_begin = True

        for i in range(len(lines)):
            dirty_line = lines[i]
            line = dirty_line.strip()

            if self.line_is_comment(line):
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
                    #
                    result_set.append(("function", line[:-2], comment_queue))
                elif self.first_word(line) == "package":
                    #
                    result_set.append(("package", line, comment_queue))
                elif self.first_word(line) == "const":
                    if self.second_word(line) == "(":
                        const_set = []
                        j = i + 1
                        sub_line = lines[j]
                        while sub_line.strip() != ")":
                            const_set.append(sub_line.strip())
                            j += 1
                            sub_line = lines[j]
                        result_set.append(("const_arr", const_set, comment_queue))
                    else:
                        result_set.append(("constant", line, comment_queue))
                elif self.first_word(line) == "var":
                    if self.second_word(line) == "(":
                        var_set = []
                        j = i + 1
                        sub_line = lines[j]
                        while sub_line.strip() != ")":
                            var_set.append(sub_line.strip())
                            j += 1
                            sub_line = lines[j]
                        result_set.append(("variable_arr", var_set, comment_queue))
                    else:
                        result_set.append(("variable", line, comment_queue))
                elif self.first_word(line) == "type" and line[-1] == "{":
                    type_set = [line]
                    j = i + 1
                    sub_line = lines[j]
                    while sub_line.strip() != "}":
                        type_set.append(sub_line.strip())
                        j += 1
                        sub_line = lines[j]
                    result_set.append(("type", type_set, comment_queue))
                elif self.first_word(line) == "import":
                    import_set = []
                    j = i + 1
                    sub_line = lines[j]
                    while sub_line.strip() != ")":
                        import_set.append(sub_line.strip())
                        j += 1
                        sub_line = lines[j]
                    result_set.append(("imports", import_set))

                comment_queue = []

        for i in result_set:
            print(i)

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
        return line.split(' ', 1)[1]
