import conf
import json


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

    def _generation_html_block(self, block):
        """
        Generates html code from one block (element of list).
        :param block: dictionary with elements to generate
        :return: string with ready html code
        """

        result = ""
        for tag in block:
            result += "<" + tag + ">" + block[tag] + "</" + tag + ">"
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

