import conf
import json
import re
import html_encode_symbols


def ul_decoration(function_to_decorate):
    def wrapper(element, arg):
        result = "<ul>"
        result += function_to_decorate(element, arg)
        result += "</ul>"
        return result
    return wrapper


def li_decoration(function_to_decorate):
    def wrapper(block):
        return "<li>" + function_to_decorate(block) + "</li>"
    return wrapper


class ConverterJsonToHtml():

    def _convert_json_to_python_object(self):
        """
        Deserializes json file to python object.
        :return: python object with parsing html code
        """

        file = open(conf.input_file)
        return json.loads(file.read())

    def _parsing_tag(self, tag):
        """
        Generates opening and closing tags.
        :param tag: string containing tag name, html classes, html id
        :return: tuple of strings with opened and closed tag
        """

        pattern = "(?P<name>[\w\d])(?P<classes>\.*[^#]*)#?(?P<id>[^.#]*)"
        regex = re.match(pattern, tag)
        start_tag = ""
        finish_tag = regex.group('name')
        start_tag += regex.group("name")
        if regex.group("id") is not '':
            start_tag += " id=\"" + regex.group("id") + "\""
        if regex.group("classes") is not "":
            start_tag += " class=\""
            for class_name in regex.group("classes").split('.'):
                if class_name is not '':
                    start_tag += class_name + " "
            start_tag = start_tag[:-1]
            start_tag += "\""
        return (start_tag, finish_tag)

    def _encode_body(self, body):
        """
        Encodes characters with html codes.
        :param body: string with html elements
        :return: string without html elemnts
        """

        for symbol, code in html_encode_symbols.encode_symbols.items():
            body = body.replace(symbol, code)
        return body

    def _generation_html_block(self, block):
        """
        Generates html code from one block (element of list).
        :param block: dictionary with elements to generate
        :return: string with ready html code
        """

        result = ""
        for tag, body in block.items():
            start_tag, finish_tag = self._parsing_tag(tag)
            if type(body) is list:
                result += "<" + start_tag + ">" + self._parsing_python_object(body) + "</" + finish_tag + ">"
            else:
                result += "<" + start_tag + ">" + self._encode_body(body) + "</" + finish_tag + ">"
        return result

    def _save_to_file(self, html_code):
        """
        Saves the finished html code to a file in the hard disk.
        :param html_code: string with finished html code
        :return: nothing
        """

        input_file = open(conf.output_file, 'w')
        input_file.write(html_code)
        input_file.close()

    def _assembling(self, blocks, generation):
        """
        Processing each block in a certain way.
        :param blocks: list of dictionary with tag and body
        :param generation: function for processing block
        :return: finished result after processing all blocks (finished string with html code in this project)
        """
        result = ""
        for block in blocks:
            result += generation(block)
        return result

    def _parsing_python_object(self, python_object):
        """
        Parses input and selects conversion based on type.
        :param python_object: object with code to convert to html code
        :return: string with finished html code
        """

        generation_function = None
        assembling_function = self._assembling
        block_to_generate = []
        if type(python_object) is list:
            block_to_generate = python_object
            generation_function = li_decoration(self._generation_html_block)
            assembling_function = ul_decoration(self._assembling)

        elif type(python_object) is dict:
            block_to_generate = [python_object]
            generation_function = self._generation_html_block
        else:
            raise TypeError
        return assembling_function(block_to_generate, generation_function)

    def convert_json_to_html(self):
        """
        Convert html file to html file.
        :return: nothing
        """

        python_object = self._convert_json_to_python_object()
        html_code = self._parsing_python_object(python_object)
        self._save_to_file(html_code)

