# best if run with output redirected
# python run.py > out 2>&1

import os
import sys
import getopt

import enthought.testing.run_tests
from enthought.testing.harvest_suite import find_subdirectories, \
	python_files_for_directory
from enthought.testing.coverage import the_coverage as coverage
from enthought.testing.test_suite import TestSuite


class RunTestsWithCoverage:
	
	def __init__( self, subdirs=["."], verbose=10, log_filename="unittest_log.txt",
				omitdirs=[], relativedir=".", *args, **kw ) :
		""" Create a test runner that will seach out and run tests in each
			of the directories of ``subdirs``.
			
			subdirs
                starting points for test search
			verbose
                higher numbers give more detailed output, 1 gives minimal
			log_filename
                unittest output filename. One in each subdirectory
			omitdirs
                omit files where the full name begins with one of
				these prefixes (e.g., [``c:\python23``])
			relativedir
                report results relative to dir
		"""
		self.subdirs = [ os.path.normcase( os.path.abspath( dir )) 
						for dir in subdirs ]
		self.verbose = verbose
		self.log_filename = log_filename
		self.omitdirs = [ os.path.normcase( os.path.abspath( dir )) 
						for dir in omitdirs ]
		self.relativedir = os.path.normcase( os.path.abspath( relativedir ) )
		self.relativedir += os.path.sep
		
		self.startdir = os.getcwd()
		return

	def run_tests( self ) :
		""" return list of tuples ( subdir_name, test_runner, results ) """

		results = []
		
		for subdir in self.subdirs :
			os.chdir(subdir)
			results_file = file(self.log_filename, 'w')
		
			sys_stdout = sys.stdout
			sys.stdout = results_file
			sys_stderr = sys.stderr
			sys.stderr = results_file
			
			runner, tests_results, suite = \
				enthought.testing.run_tests(subdir, omit=self.omitdirs,
					verbose=self.verbose, recurse=1, stream=results_file)
				
			sys.stdout = sys_stdout
			sys.stderr = sys_stderr
			
			results_file.close()
			results.append( (os.getcwd(), 
							os.getcwd().replace( self.relativedir, ""),
							runner, tests_results, suite ) )

		os.chdir( self.startdir )
		
		return results

	def include_unused_modules( self ) :
		""" find all .py files in the visited directories and 
		include all unloaded modules in the coverage results 
		"""
		for top in self.subdirs :
			subdirs = find_subdirectories( top, recurse=1 )
			subdirs.insert(0, top)
			for subdir in subdirs:
				if subdir not in self.omitdirs :
					pfiles = python_files_for_directory( subdir )
					for filename in pfiles :
						if not coverage.cexecuted.has_key(filename) :
							coverage.cexecuted[filename] = {}
		return
		
	def find_failed_modules( self, suite ) :
		failed_modules = []
		
		if isinstance( suite, TestSuite ) :
			failed_modules.extend( suite.failed_modules )
		
			for subsuite in suite._tests :
				failed_modules.extend( self.find_failed_modules( subsuite ) )

		return failed_modules
		
	def report_subdirectory_subtotals( self, results ) :
		### Get coverage sub totals
		subdirlist = [ result[0] for result in results ]
		
		sub_totals = coverage.get_subtotals( 
			self.subdirs, 
			coverage.cexecuted.keys(),
			ignore_errors=1,
			omit_prefixes=self.omitdirs )
		
		### report results
		total_tests = 0
		total_errors = 0
		total_failures = 0
		total_failed_modules = 0
		total_statements = 0 
		total_executed = 0

		# what's the longest name?
		max_name = max([20,] + map(len,  map( lambda(result): result[1], results)))
		unittest_format = "%%-%ds %%4d Tests run, %%4d Errors, %%4d Failures, %%4d Failed Modules" \
							% max_name
		coverage_format = "%7s Statements, %7d Statements, %5d%% Coverage"
		
		for subdir, relative_subdir, runner, test_results, suite in results :
			failed_modules = self.find_failed_modules( suite )
			unittest_results = unittest_format % (
				relative_subdir, test_results.testsRun, 
				len(test_results.errors), len(test_results.failures),
				len(failed_modules) )
			total_tests += test_results.testsRun
			total_errors += len(test_results.errors)
			total_failures += len(test_results.failures)
			total_failed_modules += len(failed_modules)
		
			try :
				statements, executed, missing = sub_totals[ subdir ]
				if statements > 0 :
					pc = 100.0 * executed / statements
				else:
					pc = 100.0
				total_statements += statements
				total_executed += executed
			except:
			    statements = 'unknown'
			    executed = 0
			    missing = 0
			    pc = 0
			    
			coverage_results = coverage_format % ( statements, executed, pc )
			
			print unittest_results, coverage_results
	
		unittest_results = unittest_format % (
				"Total", total_tests, total_errors, total_failures, total_failed_modules )
		
		if total_statements > 0 :
			pc = (100.0 * total_executed / total_statements )
		else :
			pc = 0.0
			
		coverage_results = coverage_format % ( total_statements, total_executed, pc )
		
		print unittest_results, coverage_results
		
		return

	def report_full_coverage( self, show_missing=0 ) :
		""" print standard coverage report for all .py files """
		print "Coverage details"
		coverage.report( coverage.cexecuted.keys(),
			 ignore_errors=1,
			 show_missing=show_missing,
			 omit_prefixes=self.omitdirs,
			 include_prefixes=self.subdirs,
			 relativedir=self.relativedir )
	 
		return
		
	def run( self ) :
		""" Run tests with coverage and print report """

		### Turn on coverage
		coverage.erase()
		coverage.start()
		
		### Run unittests
		results = self.run_tests()

		### Turn off coverage
		coverage.stop()
		coverage.save()

		self.include_unused_modules()
			
		self.report_subdirectory_subtotals( results )
		
		print "\n\n\n\n\n"

		self.report_full_coverage()
		
		return

def usage() :
	print """
usage: run [-o dir]* [-r dir] [-s dir]* [dir]*

[-o dir]* : don't run tests or include results for the directory dir
[-r dir]  : report results relative to dir or /, 
            ie. eliminate dir as a prefix on reported files
[-s dir]* : run tests in or below subdirectores of the directory dir
[dir]*    : run tests found in or below directory dir
	
Unit tests are run and coverage numbers accumulated.
The coverage statistics are stored in the file ./.coverage.
For each directory specified, or subdirectory of directories specified
following the -s option, unit tests will be located and run. Output
from the unit tests is directed to the file unittest_log.txt in the
specified directories or subdirectories.
	"""

if __name__ == '__main__':

	subdirs = []
	omitdirs = ['c:\python23']
	relativedir = "."

	try :
		opts, subdirs = getopt.getopt( sys.argv[1:], "ho:r:s:", ["help", "omitdirs", "relativedir", "subdirs"])
	except getopt.GetOptError:
		usage()
		sys.exit(2)

	for o, a in opts :
		if o in ("-s", "--s", "-subdirs", "--subdirs") :
			subdirs.extend( find_subdirectories( a, recurse=0 ) )

		if o in ("-o", "--o", "-omitdirs", "--omitdirs") :
			path = os.path.normcase( a )
			omitdirs.extend( path )

		if o in ("-h", "--h", "-help", "--help") :
			usage()
			sys.exit()
		
		if o in ("-r", "--r", "-relativedir", "--relativedir") :
			relativedir = a
	
	if len(subdirs) == 0 :
		subdirs = ["."]
	
	runner = RunTestsWithCoverage( subdirs, omitdirs=omitdirs, 
		relativedir=relativedir )
	
	runner.run()	 

	
