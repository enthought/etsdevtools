
import os.path
from xml.parsers.expat import ExpatError

from enthought.util.api import Set as set

# Note:  xml.etree was added in Python 2.5.
try:
    import xml.etree.ElementTree as ElementTree
except ImportError:
    import elementtree.ElementTree as ElementTree


def _setToString(s):
    text = ""
    for item in s:
        text += str(item) + ","
        
    return text[:-1]

class XmlResultsWriter:
    
    master = None
    
    def __init__(self):
        self.master = ElementTree.Element("results" )

    def aggregateResults(self, files):
        """ reads a list of files, creating an aggregate file
            containing all testsuites """
        
        unit_dict, coverage_dict = self._buildDirectoryDict(files)
        unit_xml = self._buildTestTreeFromMap(unit_dict)
        self.master.append(unit_xml)
        
        coverage_xml = self._buildCoverageTreeFromMap(coverage_dict)        
        self._postProcessCoverage(coverage_xml)
        self.master.append(coverage_xml)
        
            
    def write(self, filename):
        ElementTree.ElementTree(self.master).write(filename)
        
    def _postProcessCoverage(self, node):
        """ prune the name attributes to remove the common prefixes
        """
        
        #if the node is the top level "coverage" node, just skip to the children
        if (node.tag != "coverage"):        
            abspath = node.attrib["name"]
            last_sep_index = abspath.rfind(os.path.sep)
            parent_dir = abspath[:last_sep_index]
            rel_dir = abspath[last_sep_index+1:]
            node.attrib["name"] = rel_dir
            
        for child in node.getchildren():
            self._postProcessCoverage(child)
                
                 
    def _buildDirectoryDict(self, files):
        unit_directories = {}
        coverage_directories = {}
        for file in files:
            suite = self._parseUnitResults(file)
            coverage = self._parseCoverageResults(file)
            dir = file[:file.rfind(os.path.sep)]
            self._safeMapAppend(unit_directories, dir, suite)
            self._mergeCoverageResults(coverage_directories, coverage)
            
        return unit_directories, coverage_directories
    
    def _parseCoverageResults(self, file):
        try:
            tree = ElementTree.parse(file)
            return tree.find("coverage")
        except IOError, e:
            return ElementTree.Element("coverage",
                                       name=file,
                                       executed="0",
                                       statements="1E18",
                                       percent="0%")
        except ExpatError, e:
            return ElementTree.Element("coverage",
                                       name=file,
                                       executed="0",
                                       statements="1E18",
                                       percent="0%")
    
    def _mergeCoverageResults(self, dir_map, coverage):
        if coverage is None:
            return
        
        for child in coverage.getchildren():
            file = child.attrib["name"]
            total_lines = child.attrib["statements"]
            dir = file[:file.rfind(os.path.sep)]
            
            if child.text is None:
                missing_lines = set()
            else:
                missing_lines = set(child.text.split(','))

            srcfile = ElementTree.Element("sourcefile", 
                         name=file,
                         statements=child.attrib["statements"],
                         executed=child.attrib["executed"],
                         percent=child.attrib["percent"])
                
            if (not dir_map.has_key(dir)):
                srcfile.text = _setToString(missing_lines)
                dir_map[dir] = [srcfile]
            else:
                found = False
                for element in dir_map[dir]:
                    if (element.attrib["name"] == file):
                        found = True
                        s = set(element.text.split(","))
                        srcfile.text = _setToString(s.intersection(missing_lines))

                if not found:
                    srcfile.text = _setToString(missing_lines)

                statements = int(srcfile.attrib["statements"])
                executed = 0
                if (statements == 0):
                    percent = 0
                else:
                    executed = int(srcfile.attrib["statements"]) - len(missing_lines)
                    percent = int(100.0 * executed/statements)
                    
                srcfile.attrib["executed"] = str(executed)
                srcfile.attrib["percent"] = str("%3d" % (percent))

                dir_map[dir].append(srcfile)
                
    def _parseUnitResults(self, file):
        suite = None
        test_count = 0
        error_count = 0
        failure_count = 0
        time = "0.0"
        testname = file[:-4]

        if (not os.path.exists(file)):
            return self._constructTestSuiteForError(testname, "segmentation fault")
        try:
            tree = ElementTree.parse(file)
            suite = tree.find("testsuites")
            suite.tag = "testsuite"
            for child in suite.getchildren():
                if (child.tag == "total_time"):
                    time = child.attrib["value"]
                    continue
                
                test_count += 1
                child.attrib["classname"] = testname
                if child.find("error") is not None:
                    error_count += 1
                elif child.find("failure") is not None:
                    failure_count += 1
            suite.attrib = {"name":testname, "time":time, "tests":str(test_count), 
                            "failures":str(failure_count), "errors":str(error_count)}                            
        except IOError:
            suite = self._constructTestSuiteForError(testname, "segmentation fault")
        except ExpatError:
            suite = self._constructTestSuiteForError(testname, "xml parse error")
        except Exception:
            # not sure what happened here, but its probably a seg fault
            suite = self._constructTestSuiteForError(testname, "segmentation fault")

                
        return suite

    def _constructTestSuiteForError(self, testname, type):
            suite = ElementTree.Element("testsuites")
            suite.attrib = {"name":testname, "time":"0", "tests":"0", 
                            "failures":"0", "errors":"1"}
            testcase = ElementTree.Element("testcase", {"name":testname, "classname":testname, "time":"0"})
            testcase.append(ElementTree.Element("error", {"type":type}))
            suite.append(testcase)
            return suite
    
    def _createParentCoverage(self, parent_name, children):
        statements = 0
        executed = 0
        
        parent_element = ElementTree.Element("directory")
        for child in children:
            statements += int(child.attrib["statements"])
            executed += int(child.attrib["executed"])
            parent_element.append(child)
      
        if (statements == 0):
            percent = 0
        else:
            percent = int(100.0*executed/statements)
            
        parent_element.attrib = {"name":parent_name,
                                 "statements":str(statements),
                                 "executed":str(executed),
                                 "percent":str("%3d" %(percent)) }
                                 
        return parent_element
            

    def _createParentSuite(self, suitename, suites):
        tests = 0
        errors = 0
        failures = 0
        time = 0.0
        parent_suite = ElementTree.Element("testsuite")
        for suite in suites:
            tests += int(suite.attrib["tests"])
            errors += int(suite.attrib["errors"])
            failures += int(suite.attrib["failures"])
            time += float(suite.attrib["time"])
            parent_suite.append(suite)
            
        parent_suite.attrib = {"name":suitename, "time":str(time), "tests":str(tests), 
                        "failures":str(failures), "errors":str(errors)}
                        
        return parent_suite
    
    def _injectHierarchy(self, top):
        children = top.getchildren()
        if (len(children) == 0):
            return top
        new_top = ElementTree.Element(top.tag)
        
        while (children[0].attrib["name"].count(os.path.sep) > 0):
            parents = self._groupChildren(children)
            children = parents
        
        for child in children:
            new_top.append(child)
        
        return new_top
        
    def _groupChildren(self, children):
        if (len(children) == 0):
            return []
        
        #find the node with the deepest hierarchy, which we'll use as the level
        # at which to group. Also track the shallowest depth, which we'll use to 
        # remove the common prefixes in the path
        deepest_depth = 0
        for child in children:
            depth = child.attrib["name"].count(os.path.sep)
            deepest_depth = max(deepest_depth, depth)

        #find all the nodes at the deepest depth & put them in a map keyed
        #by their parent path. If we find something with a shallower path
        # just add it to the map
        map = {}
        for child in children:
            path = child.attrib["name"]
            if (path.count(os.path.sep) < deepest_depth):
                self._safeMapAppend(map, path, child)
            else:
                parent_path = path[:path.rfind(os.path.sep)]
                self._safeMapAppend(map, parent_path, child)
                
        # iterate through the map, creating parent nodes
        parents = []
        for key,value in map.items():
            if ((value[0].tag == "sourcefile") or (value[0].tag == "directory")):
                parent = self._createParentCoverage(key, value)
            else:
                parent = self._createParentSuite(key, value)
                
            parents.append(parent)
            
        return parents
                    
    def _safeMapAppend(self, map, key, value):
        if (map.has_key(key)):
            map[key].append(value)
        else:
            map[key] = [value]
                    
    def _buildCoverageTreeFromMap(self, map):
        #we now have a map of the directories, go through the directories totalling up the test stats
                
        filetree = ElementTree.Element("coverage")
        for dir,value_list in map.items():
            for element in value_list:
                filetree.append(element)
        
        return self._injectHierarchy(filetree)
        

    def _buildTestTreeFromMap(self, map):
        #we now have a map of the directories, go through the directories totalling up the test stats
        
        testtree = ElementTree.Element("UnitResults")
        for dir,suites in map.items():
            dir_suite = self._createParentSuite(dir, suites)
            testtree.append(dir_suite)

        return self._injectHierarchy(testtree)
