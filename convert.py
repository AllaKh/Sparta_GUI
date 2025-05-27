from lxml import etree as ET
from decimal import *
import importArgs as Args
import os, re, sys
 
class Parser():
        """
        File usage: xml2.py <path to script & output dir> <input XML> <output file>
 
        Shortfalls of this script;
        If an XML comment spans multiple lines without a <!-- on each line, only the first will be commented in the Python
 
        Comments inside a list of arguments for execute method will likely need to be removed from the output, these aren't
        ignored incase something in the args is required but not defined
 
        if an <if> has it's <condition> somewhere other than the first or 2nd tag within and doesn't appear after <then>
        or <else> you'll probably see `if None` in the output because of the comment appearing where parse_if expects <condition>
 
        The following processes need to be created manually, although corresponding data from XMl should be printed in
        the generated Python;
                Import
                Delete
                Dialog
                SetNextStage
 
        ParserUtils.py isn't currently implemented compeltely, but intended for output use, so the following also require attention;
                Errors
                RegularExp
                Requried
        """
 
        def __init__(self):
                self.output_list = []  # collected output lines
                self.requried = ''
                self.decimalDict = {}
                self.varDict = {}
                self.allDecimalDict = {}
                self.importArgs = []
                self.il = 0            # indentation level
 
        def __iter__(self):
                return iter(self.output_list)
 
        def out(self, s):
                """Output the indented string to the output list."""
                self.output_list.append('    ' * self.il + s)
 
        def indent(self, incr=1):
                """Increase the indentation level."""
                self.il += incr
 
        def dedent(self, incr=1):
                """Decrease the indentation level."""
                self.il -= incr
 
        def parse(self, elem):
                """Call the parser of the elem.tag name.
 
                The tag name appended to "parse_" and then the name of that
                function is called.  If the function is not defined, then
                self.parse_undefined() is called.
                """
                fn_name = 'parse_{0}'.format(elem.tag)
                try:fn = getattr(self, fn_name)
                except AttributeError:fn = self.parse_undefined
                return fn(elem)
 
        def loop(self, elem):
                """Helper method to loop through the child elements."""
                for e in elem:
                        if e.sourceline == 339:
                                print e.tag + ' ' + e.attrib['id']
                                self.parse(e)
                        else:
                                self.parse(e)
 
        def parseXMLfile(self, script):
                """Reads the XML file and starts parsing from the root element."""
 
                events = ("start", "end", "comment", "pi")
                try:
                        context = ET.iterparse(script, events=events)
                        context = iter(context)
                        event, root = context.next()
                        for event, elem in context:
                                if event == "end" and elem.tag == "stage":
                                        self.parse(elem)
                                        root.clear()
                except IOError:
                        self.out("## Error : Cannot parse script" + script)
 
        ###################### ELEMENT PARSERS #######################
 
        def parse_undefined(self, elem):
                """Called for the element that has no parser defined."""
                self.out('## {0} '.format(elem.text))
 
        def parse_script(self, elem):
                self.loop(elem)
 
        def parse_stage(self, elem):
                self.out('')
                self.out('class {0}():'.format(elem.attrib['id']))
                self.indent()
                self.loop(elem)
                self.dedent()
 
        def parse_initialise(self, elem):
                self.out(','.join(self.importArgs))
                vars = self.passed_vars(elem)
                if not vars: self.out('def {initialise}(self):'.format(initialise = elem.tag))
                else: self.out('def {initialise}(self, {vars}):'.format(initialise = elem.tag, vars = ", ".join(vars)))
                self.indent()
                for e in elem:
                        if e.tag == 'decimal': d = self.init_decimals(e)
                        elif e.tag == 'variable': v = self.init_vars(e)
                self.loop(elem)
                self.dedent()
 
        def parse_execute(self, elem):
                # possible limitation here with detecting the type of execute tag
                if elem[0].tag == 'required':self.loop(elem)
                else:
                        self.out('')
                        vars = self.passed_vars(elem)
                        if not vars:self.out('def {execute}(self):'.format(execute = elem.tag))
                        else:self.out('def {execute}(self, {vars}):'.format(execute = elem.tag, vars = ", ".join(vars)))
                        self.indent()
                        self.loop(elem)
                        self.dedent()
 
        def passed_vars(self, elem):
                passed_vars = []
 
                for e in elem:
                        if e.tag == 'variable' or e.tag == 'decimal':
                                passed_vars.append(e.attrib['id'])
 
                passed_vars = list(set(passed_vars))
                return passed_vars
 
        def collect_attrs(self, elem, tag, attr):
                elemVars = [var for var in self.get_attrs(elem, tag, attr)]
                # Remove duplicate variables from list
                elemVars = list(set(elemVars))
                return elemVars
 
 
        def get_attrs(self, elem, tag, attr):
                """Return attribute `attr` of `tag` child elements of `elem`."""
 
                # If an element has any children loop them
                if len(elem):
                        for e in elem:
                                # Recursively call this func, yield each result:
                                for attribute in self.get_attrs(e, tag, attr):
                                        yield attribute
 
                # Otherwise, check if elem is of type `tag` with attribute of `attr`,
                # if so yield the value of the attribute.
                if elem.tag == 'variable':
                        if attr in elem.attrib:
                                yield elem.attrib[attr]
                elif elem.tag == 'required':
                        if attr in elem.attrib:
                                yield elem.attrib[attr]
 
        def parse_decimal(self, elem):
                '''
                when we get a line of xml for a decimal value it is now ignored as init_decimals
                handles these all at the beginning of the init/execute methods
                '''
                self.create_dec_dict(self.allDecimalDict, elem)
 
        def init_decimals(self, elem):
                id_ = elem.attrib['id']
                value = elem.attrib['value']
                decDict = {}
                self.decimalDict = self.create_dec_dict(decDict, elem)
                ##
                # Old parse_decimal code
                if self.is_number(value) is True:
                        try:
                                self.out("{id} = decimal.Decimal('{value}').quantize(decimal.Decimal('{dp}'), rounding=decimal.{rounding})".format(id= id_, value= value, dp= self.decimalDict[id_]['dp'], rounding= self.decimalDict[id_]['rounding']))
                        except:
                                print 'Check setVariableValue for {0}'.format(id_)
                else:
                        try:
                                self.out("{id} = decimal.Decimal({value}).quantize(decimal.Decimal('{dp}'), rounding=decimal.{rounding})".format(id= id_, value= value, dp= self.decimalDict[id_]['dp'], rounding= self.decimalDict[id_]['rounding']))
                        except:
                                print 'Check setVariableValue for {0}'.format(id_)
                return self.decimalDict
 
        def create_dec_dict(self, d, elem):
                ROUNDZERO =     "1"
                ROUNDONE =      "0.1"
                ROUNDTWO =      "0.01"
                ROUNDTHREE =    "0.001"
                ROUNDFOUR =     "0.0001"
                ROUNDFIVE =     "0.00001"
                ROUNDSIX =      "0.000001"
 
                ROUND_DOWN = 'ROUND_DOWN'
                ROUND_HALF_UP = 'ROUND_HALF_UP'
                ROUND_HALF_EVEN = 'ROUND_HALF_EVEN'
                ROUND_CEILING = 'ROUND_CEILING'
                ROUND_FLOOR = 'ROUND_FLOOR'
                ROUND_UP = 'ROUND_UP'
                ROUND_HALF_DOWN = 'ROUND_HALF_DOWN'
                ROUND_05UP = 'ROUND_05UP'
                ROUND_FIVE_DOWN = 'ROUND_FIVE_DOWN'
 
                decimalPlacesDict = {"0":ROUNDZERO, "1":ROUNDONE, "2":ROUNDTWO, "3":ROUNDTHREE, "4":ROUNDFOUR, "5":ROUNDFIVE, "6":ROUNDSIX}
                roundingTypeDict = {"ROUND_CEILING":ROUND_CEILING, "ROUND_DOWN":ROUND_DOWN, "ROUND_FLOOR":ROUND_FLOOR, "ROUND_HALF_DOWN":ROUND_HALF_DOWN, "ROUND_HALF_EVEN":ROUND_HALF_EVEN, "ROUND_HALF_UP":ROUND_HALF_UP, "ROUND_UP":ROUND_UP, "ROUND_FIVE_DOWN":ROUND_FIVE_DOWN}
                id_ = elem.attrib['id']
 
                if elem.attrib['value'] == '':
                        value = None
                else:
                        value = elem.attrib['value']
                        value = re.sub(r'\$','',value)
 
                if ('decimalPlaces' in elem.attrib and 'roundingType' in elem.attrib):
                        decimalPlaces = decimalPlacesDict[elem.attrib["decimalPlaces"]]
                        roundingType = roundingTypeDict[elem.attrib["roundingType"]]
                        #decimalDict[elem.attrib['id']] = 'Decimal({0}).quantize(Decimal({1}), rounding={2}'.format(value, decimalPlaces, roundingType)
                        d[elem.attrib['id']] = {'value' : value, 'dp' : Decimal(str(decimalPlaces)), 'rounding' : roundingType}
 
                elif 'roundingType' in elem.attrib:
                        roundingType = roundingTypeDict[elem.attrib["roundingType"]]
                        #decimalDict[elem.attrib['id']] = 'value : {0}, dp : Decimal(0.01), rounding : {1}'.format(value, roundingType)
                        d[elem.attrib['id']] = {'value' : value, 'dp' : Decimal(str(0.01)), 'rounding' : roundingType}
 
                elif 'decimalPlaces' in elem.attrib:
                        decimalPlaces = decimalPlacesDict[elem.attrib["decimalPlaces"]]
                        d[elem.attrib['id']] = {'value' : value, 'dp' : Decimal(str(decimalPlaces)), 'rounding' : ROUND_HALF_UP}
 
                else:
                        #decimalDict[elem.attrib['id']] = 'Decimal({0}).quantize(Decimal(0.01), rounding=ROUND_HALF_UP'.format(value)
                        d[elem.attrib['id']] = {'value': value, 'dp': Decimal(str(0.01)), 'rounding' : ROUND_HALF_UP}
                return d
 
        def init_vars(self, elem):
                varDict = {}
                id_ = elem.attrib['id']
                value = elem.attrib['value']
                newValue = re.sub(r'\$','', value)
                self.varDict = self.create_var_dict(varDict, elem)
                ##
                # Old parse_variable code
                if not 'index' in elem.attrib:
                        errorID = self.collect_attrs(elem, 'required', 'errorID')
                        execute = elem.find('execute')
 
                        try: errorID = execute.attrib['errorID']
                        except: pass
 
                        # Conversion of the value to the type because of the later repr().
                        value = elem.attrib['value']
                        etype = elem.attrib['type']
 
                        newValue = re.sub(r'\$', '', value)
 
                        id_ = elem.attrib['id']
 
                        if execute is not None:
                                required = execute[0]
                                if required.tag == "required":
                                        self.var_required(required, value, etype, errorID)
 
                        if 'startString' in elem.attrib:
                                if id_ in self.varDict.keys():
                                        self.out('if {id} is None:'.format(id= id_))
                                        self.indent()
                                else:
                                        pass
                                self.out('{id} = {value}[{start}:{end}]'.format(id= id_, value= newValue, start= elem.attrib['startString'], end= elem.attrib['endString']))
                        else:
                                if id_ in self.varDict.keys():
                                        self.out('if {id} is None:'.format(id= id_))
                                        self.indent()
                                else:
                                        pass
                                if elem.attrib['type'] == 'String':
                                        self.out("{id} = {value}".format(id= id_, value= repr(newValue)))
                                elif elem.attrib['type'] == 'Integer' and elem.attrib['value'] is '':
                                        # incase an Int isn't defined, stops var = <blank> being written
                                        self.out("{id} = 0".format(id= id_))
                                elif elem.attrib['type'] == 'HTML' and elem.attrib['value'] is '':
                                        self.out("{id} = ''".format(id= id_))
                                elif elem.attrib['type'] == 'Date' and elem.attrib['value'] is not '':
                                        self.out("{id} = '{value}'".format(id= id_, value= elem.attrib['value']))
                                elif elem.attrib['type'] == 'Date' and elem.attrib['value'] is '':
                                        self.out("{id} = ''".format(id = id_))
                                else:
                                        self.out('{id} = {value}'.format(id= id_, value= value))
                                if id_ in self.varDict.keys():
                                        self.dedent()
                                else:
                                        pass
                return self.varDict
 
        def create_var_dict(self, d, elem):
                id_ = elem.attrib['id']
                value = elem.attrib['value']
                newValue = re.sub(r'\$','', value)
                try:
                        d[elem.attrib['id']] = {'value' : newValue, 'type' : elem.attrib['type']}
 
                except KeyError:
                        print '{0} on {1}'.format(elem.tag, unicode(elem.sourceline))
                return d
 
        def parse_variable(self, elem):
                '''
                when we get a line of xml for a variable value it is now ignored as init_vars
                handles these all at the beginning of the init/execute methods
                '''
                pass
 
        def parse_variableArray(self, elem):
                array = elem.attrib['id']
                value = re.sub(r'\$','',elem.attrib['value'])
 
                self.out("{0}.append('''{1}''')".format(array, value))
 
 
        def parse_setVariableValue(self, elem):
                if elem.text:
                        text = re.sub(r'\$','',elem.text)
                        id_ = elem.attrib['id']
 
                        if id_ in self.allDecimalDict.keys():
                                if self.is_number(text) is True:
                                        try:
                                                self.out("{id} = decimal.Decimal('{text}').quantize(decimal.Decimal('{dp}'), rounding=decimal.{rounding})".format(id= id_, text= text, dp= self.allDecimalDict[id_]['dp'], rounding= self.allDecimalDict[id_]['rounding']))
                                        except:
                                                print 'Check setVariableValue for {0}'.format(id_)
                                else:
                                        try:
                                                self.out("{id} = decimal.Decimal({text}).quantize(decimal.Decimal('{dp}'), rounding=decimal.{rounding})".format(id= id_, text= text, dp= self.allDecimalDict[id_]['dp'], rounding= self.allDecimalDict[id_]['rounding']))
                                        except:
                                                print 'Check setVariableValue for {0}'.format(id_)
                        elif text in self.varDict.keys():
                                # value to be assigned is a variable
                                try:
                                        self.out('{id} = {text}'.format(id= id_,text= text))
                                except:
                                        print 'Check setVariableValue for {0}, {1}'.format(id_, text)
                        elif id_ in self.varDict.keys():
                                try:
                                        if self.varDict[id_]['type'] == 'String':
                                                self.out('{id} = {text}'.format(id= id_, text= repr(text)))
                                        elif self.varDict[id_]['type'] == 'Boolean':
                                                self.out('{id} = {text}'.format(id= id_, text= text))
                                        elif self.varDict[id_]['type'] == 'Integer':
                                                self.out('{id} = {text}'.format(id= id_, text= text))
                                except:
                                        print 'Check setVariableValue for {0}'.format(id_)
                        else:
                                self.out("## this isn't in a dict so no type check done. Line {0}".format(unicode(elem.sourceline)))
                                self.out('{id} = {text}'.format(id= id_,text= text))
                else:
                        self.out("{id} = ''".format(id= elem.attrib['id']))
                        print '{tag} has no CDATA. Sourceline: {line}'.format(tag= elem.tag, line= unicode(elem.sourceline))
 
 
        def parse_executeMethod(self, elem):
                a = elem.attrib
                argumentsTag = elem.find('arguments')
                returnTag = elem.find('return')
                argVars, returnVars = [], []
 
                self.out('import ' + a['class'])
 
                for arg in argumentsTag:
                        # variables & values
                        try:
                                if arg.tag == "value": argVars.append(arg.text)
                                elif arg.tag == "variable": argVars.append(arg.attrib['id'])
                        #else: print 'Problem or Comment in Args, {0}, on line {1}'.format(arg.text, unicode(elem.sourceline))
                        except KeyError:
                                self.out('KeyError on line {line} with: {tag}'.format(line= arg.sourceline, tag= arg.tag))
 
                for r in returnTag:
                        # inside executeMethod return tag
                        try: returnVars.append(r.attrib['id'])
                        except KeyError:
                                self.out('KeyError on line {line} with: {tag}'.format(line= r.sourceline, tag= r.tag))
 
                # Wait for list of vars
                if len(argVars) > 0:
                        self.out('{0}.{1}(*{2})'.format(a['class'], a['method'], argVars))
                else: self.out('{0}.{1}()'.format(a['class'], a['method']))
 
                for r in returnTag:
                        self.out('{0} = {1}.{2}()'.format(r.attrib['id'], a['class'], a['method']))
 
 
        def parse_if(self, elem):
                if elem[0].tag == 'condition':
                        condition = self.parse(elem[0])
                        #self.out('if {0}, {1}:'.format(unicode(elem.sourceline), condition))   # to debug sourceline when if None
                        self.out('if {0}:'.format(condition))
                #if elem[0].tag == "if": self.parse_if(elem)
                elif elem[1].tag == 'condition':
                        condition = self.parse(elem[1])
                        self.out('if {0}:'.format(condition))
                else:
                        self.out("print 'problem on line {0}'".format(unicode(elem.sourceline)))
                self.loop(elem)
 
 
        def parse_condition(self, elem):
                condition = re.sub(r'\$','',elem.text)
                return condition
 
        def parse_then(self, elem):
                ifblock = elem.find('if')
                if ifblock is not None:
                        for t in ifblock:
                                if t.tag == 'condition':
                                        condition = self.parse(t)
                                        self.indent()
                                        self.out('')
                                        self.out('if {condition}:'.format(condition= condition))
                        self.loop(ifblock)
                        self.dedent()
                else:
                        self.indent()
                        #print '{0}. Sourceline: {1}'.format(elem.tag, unicode(elem.sourceline))
                        self.loop(elem)
                        self.dedent()
 
        def parse_validate(self, elem):
                self.loop(elem)
 
        def parse_else(self, elem):
                ifblock = elem.find('if')
                if ifblock is not None:
                        for t in ifblock:
                                if t.tag == 'condition': condition = self.parse(t); self.out(''); self.out('elif {condition}:'.format(condition= condition))
                        self.loop(ifblock)
                else:
                        self.out('else:')
                        self.indent()
                        self.loop(elem)
                        self.dedent()
 
 
        def parse_regularExpression(self, elem):
                try:
                        if elem.attrib['fieldID'] == '': fieldID = None
                        else: fieldID = elem.attrib['fieldID']
                        if elem.attrib['errorID'] == '': errorID = None
                        else: errorID = elem.attrib['errorID']
                        pattern = elem.attrib.get('pattern')
                        text = elem.text
                        self.out('')
                        if not pattern: self.out("""utils.regularExp('''{text}''', {field}, {error})""".format(text= text, field= fieldID, error= errorID))
                        else: self.out("""utils.regularExp('''{text}''', {field}, {error}, '{pattern}')""".format(text= text, field= fieldID, error= errorID, pattern= pattern))
                except KeyError:
                        print '{tag}. Sourceline: {line}'.format(tag= elem.tag, line= unicode(elem.sourceline))
                        self.out('## TODO: failed regex on script line {0}'.format(unicode(elem.sourceline)))
 
 
        def parse_updateGUIFieldState(self, elem):
                field = elem.attrib['id']
                text = re.sub(r'\$','',elem.text)
 
                self.out('fieldState = {}')
                self.out('fieldState[{0}] = [{1}]'.format(field, text))
 
 
        def parse_error(self, elem):
                self.out('print "TODO: Error. script line {0}"'.format(unicode(elem.sourceline)))
                self.out('utils.error({text}, {field}, {error})'.format(text= elem.text, field= elem.attrib.get("fieldID"), error= elem.attrib.get("errorID")))
 
 
        def parse_import(self, elem):
                a = elem.attrib
                argumentsTag = elem.find('arguments')
                returnTag = elem.find('return')
                argVars, returnVars = [], []
 
                path = a['path'].split('/')
                path = '{0}{1}'.format('etk.scripts.', '.'.join(path))
                year = re.findall(r"\.(\d{4})\.", path) # find a 4 digit folder name in the path directly following the '.'
                year = ''.join(year)    # convert list to string
                path = re.sub(year, '{0}{1}'.format('yr_',year), path)
 
                self.out('import {0}'.format(path))
                self.out('calc = {path}.{method}()'.format(path= path, method= elem.attrib['stageID']))
 
                for arg in argumentsTag:
                        # variables & values
                        try:
                                if arg.tag == "value": argVars.append(arg.text)
                                elif arg.tag == "variable": argVars.append(arg.attrib['id'])
                        #else: print 'Problem or Comment in Args, {0}, on line {1}'.format(arg.text, unicode(elem.sourceline))
                        except KeyError:
                                self.out('## KeyError on line {0} with: {1}'.format(arg.sourceline, arg.tag))
 
                for r in returnTag:
                        # inside executeMethod return tag
                        try: returnVars.append(r.attrib['id'])
                        except KeyError:
                                self.out('## KeyError on line {0} with: {1}'.format(r.sourceline, r.tag))
 
                # Wait for list of vars
                if len(argVars) > 0:
                        self.out('{returnvars} = {calc}.initialise({vars})'.format(returnvars = ', '.join(returnVars), calc= 'calc', vars= ', '.join(argVars)))
                else: self.out('TODO: Problem. Check this import: {0}()'.format('calc'))
                self.out('')
 
 
        def parse_dialog(self, elem):
                text = self.parse_escapeString(elem.attrib['text'])
                text.encode('ascii', 'ignore')
                try:
                        self.out('')
                        self.out('print "TODO: Dialog. {0}"'.format(unicode(elem.sourceline)))
                        self.out("## item_dialog(id='{id}', text='''{text}''', type='{type}')".format(id= elem.attrib['id'], text= text, type= elem.attrib['type']))
                except:
                        self.out('print "Problem with the Dialog on line {0}" '.format(unicode(elem.sourceline)))
 
        def parse_escapeString(self, s):
                text = re.sub(r'\$','',s)
                escapeString = re.sub(r'\s',' ', text)
                return escapeString
 
        def parse_delete(self, elem):
                self.out('## TODO: Delete. {0}'.format(elem.attrib['id']))
 
        def var_required(self, elem, value, etype, errorID):
                ## value perhaps needs to be the field.getvalue()
                if value == '':
                        value = None
                if value is not None:
                        value = re.sub(r'\$','', value)
                ## Store this to output with parse_requried
                self.required = "utils.required({value}, {type}, {error})".format(value= value, type= repr(etype), error= "".join(errorID))
 
        def parse_required(self, elem):
                self.out(self.required)
 
        def parse_setNextStage(self, elem):
                self.out('print "TODO: set next stage : {text} line {line}"'.format(text= re.sub(r'\$','',elem.text), line= unicode(elem.sourceline)))
 
        def is_number(self, value):
                """
                Check if a given value is a number or not.
                """
                try:
                        float(value) # for int, long and float
                except ValueError:
                        try:
                                complex(value) # for complex
                        except ValueError:
                                return False
                return True
 
def main():
        if len(sys.argv) is not 3:
                print 'usage: xml2.py <path to script & output dir> <path to import script>'
                sys.exit(1)
 
        try:
                importArgs = Args.importArgs()
                importArgs.parseImportXML(sys.argv[2], sys.argv[1])
        finally:
                parser = Parser()
                folder = sys.argv[1]
                for a in importArgs:
                        parser.importArgs.append(a)
                parser.parseXMLfile((os.path.join(folder, 'script.xml')))
                fname = 'newOutput.py'
                outputpath = os.path.join(folder, fname)
                with open(outputpath, 'w') as f:
                        f.write('# coding: UTF-8\nfrom etk import decimal\n')
                        for s in parser:
                                f.write(s + '\n')
                        f.close()
 
if __name__ == '__main__':
        main()