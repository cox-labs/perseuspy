""" Perseus parameter parsing

This module contains convenience function for parsing
the Perseus parameters.xml file and extracting parameter values
"""
import xml.etree.ElementTree as ET

def parse_parameters(filename):
    """ parse the parameters.xml file.
    :param filename: 'parameters.xml'
    :returns tree: a 'xml.etree.ElementTree' xml object.
    """
    return ET.parse(filename)

def _simple_string_value(tree, kind, name):
    """ base function for extracting a simple parameter value.
    :param tree: the parameters tree.
    :param kind: the xml-tag name of the parameter.
    :param name: the name of the parameter.
    :returns value: the content of the parameter 'Value' as string."""
    query = ".//{kind}[@Name='{name}']/Value".format(kind=kind, name=name)
    return tree.find(query).text

def stringParam(parameters, name):
    """ string parameter value.
    :param parameters: the parameters tree.
    :param name: the name of the parameter.  """
    return _simple_string_value(parameters, 'StringParam', name)

def fileParam(parameters, name):
    """ file parameter value.
    :param parameters: the parameters tree.
    :param name: the name of the parameter.  """
    return _simple_string_value(parameters, 'FileParam', name)

def intParam(parameters, name):
    """ integer parameter value.
    :param parameters: the parameters tree.
    :param name: the name of the parameter.  """
    return int(_simple_string_value(parameters, 'IntParam', name))

def doubleParam(parameters, name):
    """ double parameter value.
    :param parameters: the parameters tree.
    :param name: the name of the parameter.  """
    return float(_simple_string_value(parameters, 'DoubleParam', name))

def singleChoiceParam(parameters, name, type_converter = str):
    """ single choice parameter value. Returns -1 if no value was chosen.
    :param parameters: the parameters tree.
    :param name: the name of the parameter.
    :param type_converter: function to convert the chosen value to a different type (e.g. str, float, int). default = 'str'"""
    param = parameters.find(".//SingleChoiceParam[@Name='{name}']".format(name=name))
    value = int(param.find('Value').text)
    values = param.find('Values')
    if value < 0:
        return value
    return type_converter(values[value].text)

def multiChoiceParam(parameters, name, type_converter = str):
    """ multi choice parameter values.
    :param parameters: the parameters tree.
    :param name: the name of the parameter.
    :param type_converter: function to convert the chosen value to a different type (e.g. str, float, int). default = 'str'
    :returns dictionary: value -> values
    """
    param = parameters.find(".//MultiChoiceParam[@Name='{name}']".format(name=name))
    value = param.find('Value')
    values = param.find('Values')
    multiparam = {}
    for item in value.findall('Item'):
        multiparam[int(item.text)] = type_converter(values[int(item.text)].text)
    return multiparam
