import conf
import json


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
            if tag == "title":
                result += "<h1>" + block[tag] + "</h1>"
            elif tag == "body":
                result += "<p>" + block[tag] + "</p>"
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

    def _parsing_python_object(self, python_object):
        """
        Parses input and selects conversion based on type.
        :param python_object: object with code to convert to html code
        :return: string with finished html code
        """

        result = ""
        if type(python_object) is list:
            for block in python_object:
                result += self._generation_html_block(block)
        elif type(python_object) is dict:
            result += self._generation_html_block(python_object)
        else:
            raise TypeError
        return result

    def convert_json_to_html(self):
        """
        Convert html file to html file.
        :return: nothing
        """

        python_object = self._convert_json_to_python_object()
        html_code = self._parsing_python_object(python_object)
        self._save_to_file(html_code)

