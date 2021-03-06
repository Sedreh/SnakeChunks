#! /usr/bin/python
"""Peak Motifs - developed by Jocelyn Brayet <jocelyn.brayet@curie.fr>
Copyright (C) 2015  Institut Curie.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

##########################################################'
 
Client to download peak-motifs results from RSAT server.


usage: peak-motifs_soap.py [-h] -test <TEST_FILE> [-control <CONTROL_FILE>]
				[-max_seq_length <MAX_SEQ_LENGTH>]
				[-max_motif_number <MAX_MOTIF_NUMBER>]
				[-top_peaks <TOP_PEAKS>] [-min_length <MIN_LENGTH>]
				[-max_length <MAX_LENGTH>] [-markov <MARKOV_MODEL>]
				[-min_markov <MIN_MARKOV>]
				[-max_markov <MAX_MARKOV>] [-noov <NOOV_DETECTION>]
				[-class_int <CLASS_INT>] [-str <STR_SUMMED>]
				[-graph_title <GRAPH_TITLE>]
				[-image_format <IMAGE_FORMAT>]
				[-disco [<DISCO_ALGORITHM> [<DISCO_ALGORITHM> ...]]]
				[-source <SOURCE_FILE>] [-verb <VERBOSITY>]
				[-motif_db <MOTIF_DB>] [-ref_motif <REF_MOTIF>] 
				-server <SERVER>

optional arguments:
  -h, --help		show this help message and exit
  -test <TEST_FILE>, --test_file <TEST_FILE>
			Input test peak sequence in fasta format.
  -control <CONTROL_FILE>, --control_file <CONTROL_FILE>
			Input control peak sequence in fasta format.
  -max_seq_length <MAX_SEQ_LENGTH>, --maxSeqLength <MAX_SEQ_LENGTH>
			Maximal sequence length.
  -max_motif_number <MAX_MOTIF_NUMBER>, --maxMotifNumber <MAX_MOTIF_NUMBER>
			Maximal number of motifs (matrices) to return for
			pattern discovery algorithms.
  -top_peaks <TOP_PEAKS>, --topPeaks <TOP_PEAKS>
			Restrict the analysis to the N peaks at the top of the
			input sequence file.
  -min_length <MIN_LENGTH>, --minLength <MIN_LENGTH>
			Minimal oligonucleotide length.
  -max_length <MAX_LENGTH>, --maxLength <MAX_LENGTH>
			Maximal oligonucleotide length.
  -markov <MARKOV_MODEL>, --markovModel <MARKOV_MODEL>
			Order of the Markov model used to estimatd expected
			oligonucleotide frequencies for oligo-analysis and
			local-word-analysis.
  -min_markov <MIN_MARKOV>, --minMarkov <MIN_MARKOV>
			Minimal value for markov order. Use in combination
			with the next option (max_markov).
  -max_markov <MAX_MARKOV>, --maxMarkov <MAX_MARKOV>
			Maximal value for markov order. Use in combination
			with the previous option (min_markov).
  -noov <NOOV_DETECTION>, --noovDetection <NOOV_DETECTION>
			No overlapping of oligos allowed if value = 1.
  -class_int <CLASS_INT>, --classInt <CLASS_INT>
			Class interval for position-analysis. The width of the
			position classes, in number of bases (default: 20).
  -str <STR_SUMMED>, --strSummed <STR_SUMMED>
			Oligonucleotide occurrences found on both stands are
			summed (2) or not (1). Default is 2.
  -graph_title <GRAPH_TITLE>, --graphTitle <GRAPH_TITLE>
			Title displayed on top of the graphs.
  -image_format <IMAGE_FORMAT>, --imageFormat <IMAGE_FORMAT>
			Image format. All the formats supported by XYgraph can
			be used.
  -disco [<DISCO_ALGORITHM> [<DISCO_ALGORITHM> ...]], --discoAlgorithm [<DISCO_ALGORITHM> [<DISCO_ALGORITHM> ...]]
			Specify the software tool(s) that will be used for
			motif discovery
			(oligos|dyads|positions|local_words|merged_words).
			Several algorithms can be specified either by using a
			comma-separated list of algorithms: -disco
			oligos,dyads
  -source <SOURCE_FILE>, --sourceFile <SOURCE_FILE>
			Enter the source of the fasta sequence file. Supported
			source: galaxy
  -verb <VERBOSITY>, --verbosity <VERBOSITY>
			Verbosity.
  -motif_db <MOTIF_DB>, --motif_db <MOTIF_DB>
			Name(s) of motif database(s). List of databases
			of transcription factor binding motifs
			(e.g. JASPAR, TRANSFAC, RegulonDB, ...) which
			will be compared to the discovered motifs
			(task motifs_vs_db). 
  -ref_motif <REF_MOTIF>, --ref_motif <REF_MOTIF>
			Motif annotated in some transcription factor database
			(e.g. RegulonDB, Jaspar, TRANSFAC) for the
			transcription factor of interest.
  -server <SERVER>, --server <SERVER>
			RSAT server
  -output <OUMODE>, --output <OUTPUT>
			Output mode requested to the Web service. Supported: "server", "client", "both"
  -prefix <PREFIX>, --prefix <PREFIX>
			Prefix to the output archive (the extension .zip will automaticalybe added).
			Default: peak-motifs_results.zip

Version 0.1 - 30/01/2015 - Adapted from Jocelyn Brayet, France Genomique team

##########################################################

"""
__author__ =  'Jocelyn Brayet'

###########################################################'
## Import

import argparse
import os
import urllib
import zipfile
import time
import platform
#from suds.client import Client ## NOT SUPPORTED ANYMORE -> Switch to zeep (JvH, 2017-12-19)
from zeep import Client

###########################################################'

###########################################################'
## Define log options for suds


########################## FUNCTION DEFINITION ############'

## Define a function to make a service perform the desired request using provided arguments
def call_run_service(service, args):
	"""
	Run job in RSAT server.
		service -> RSAT web service
		args -> web service request 	 
	"""
	
	result = rsat_service.peak_motifs(args)
	return result

def testNone(argument):
	"""
	Test if argument is None or not.
		argument -> argument give by user
	"""

	if not argument is None:
		variable = argument[0]
	else:
		variable = ""
	return variable


###########################################################'
## Function to recup results

def buildZipUrl(algoResults):
	"""
	Get the URL of the result archive from RSAT server.
        algoResults -> result given by RSAT server
	"""
	
	recupResult = str(algoResults)
	tabResults=recupResult.split("\n")
	urlZip = tabResults[4]
				
	return urlZip


## Tested with python 2.6.6
peakMotifsVersion = '0.1 - 30/01/2015'

###########################################################'
# server dictionary
serverDict = {

	"protists":"http://protists.rsat.eu/web_services/RSATWS.wsdl",
	"fungi":"http://fungi.rsat.eu/web_services/RSATWS.wsdl",
	"metazoa":"http://metazoa.rsat.eu/web_services/RSATWS.wsdl",
	"teaching":"http://teaching.rsat.eu/web_services/RSATWS.wsdl",
	"plants":"http://rsat.eead.csic.es/plants//web_services/RSATWS.wsdl",
	"prokaryotes":"http://prokaryotes.rsat.eu/web_services/RSATWS.wsdl",
	"archaea":"http://archaea.rsat.eu/web_services/RSATWS.wsdl",
	"bacteria":"http://bacteria.rsat.eu/web_services/RSATWS.wsdl"

	}

"""
serverDict = {

	"protists":"http://protists.rsat.eu/web_services/RSATWS.wsdl",
	"fungi":"http://fungi.rsat.eu/rsat/web_services/RSATWS.wsdl",
	"metazoa":"http://metazoa.rsat.eu/web_services/RSATWS.wsdl",
	"teaching":"http://teaching.rsat.eu/web_services/RSATWS.wsdl",
	"plants":"http://rsat.eead.csic.es/plants//web_services/RSATWS.wsdl",
	"prokaryotes":"http://prokaryotes.rsat.eu/web_services/RSATWS.wsdl",
	"archaea":"http://archaea.rsat.eu/web_services/RSATWS.wsdl",
	"bacteria":"http://bacteria.rsat.eu/web_services/RSATWS.wsdl"
	
	}
"""

if __name__ == '__main__':

	########### peak motifs arguments ####################
	parser = argparse.ArgumentParser(description='Client to download peak-motifs results from RSAT server.', epilog='Version '+peakMotifsVersion)
	
	parser.add_argument('-server', '--server', metavar='<SERVER>', type=str, nargs=1, help='RSAT server', required=True)

	parser.add_argument('-test', '--test_file', metavar='<TEST_FILE>', type=argparse.FileType('r'), nargs=1, help='Input test peak sequence in fasta format.', required=True)
	parser.add_argument('-control', '--control_file', metavar='<CONTROL_FILE>', type=argparse.FileType('r'), nargs=1, help='Input control peak sequence in fasta format.', required=False)
	parser.add_argument('-max_seq_length', '--maxSeqLength', metavar='<MAX_SEQ_LENGTH>', type=int, nargs=1, help='Maximal sequence length.', required=False)
	parser.add_argument('-max_motif_number', '--maxMotifNumber', metavar='<MAX_MOTIF_NUMBER>', type=int, nargs=1, help='Maximal number of motifs (matrices) to return for pattern discovery algorithms.', required=False)
	parser.add_argument('-top_peaks', '--topPeaks', metavar='<TOP_PEAKS>', type=int, nargs=1, help='Restrict the analysis to the N peaks at the top of the input sequence file.', required=False)
	parser.add_argument('-min_length', '--minLength', metavar='<MIN_LENGTH>', type=int, nargs=1, help='Minimal oligonucleotide length.', required=False)
	parser.add_argument('-max_length', '--maxLength', metavar='<MAX_LENGTH>', type=int, nargs=1, help='Maximal oligonucleotide length.', required=False)
	parser.add_argument('-markov', '--markovModel', metavar='<MARKOV_MODEL>', type=int, nargs=1, help='Order of the Markov model used to estimatd expected oligonucleotide frequencies for oligo-analysis and local-word-analysis.', required=False)
	parser.add_argument('-min_markov', '--minMarkov', metavar='<MIN_MARKOV>', type=int, nargs=1, help='Minimal value for markov order. Use in combination with the next option (max_markov).', required=False)
	parser.add_argument('-max_markov', '--maxMarkov', metavar='<MAX_MARKOV>', type=int, nargs=1, help='Maximal value for markov order. Use in combination with the previous option (min_markov).', required=False)
	parser.add_argument('-noov', '--noovDetection', metavar='<NOOV_DETECTION>', type=int, nargs=1, help='No overlapping of oligos allowed if value = 1.', required=False)
	parser.add_argument('-class_int', '--classInt', metavar='<CLASS_INT>', type=int, nargs=1, help='Class interval for position-analysis. The width of the position classes, in number of bases (default: 20).', required=False)
	parser.add_argument('-str', '--strSummed', metavar='<STR_SUMMED>', type=int, nargs=1, help='Oligonucleotide occurrences found on both stands are summed (2) or not (1). Default is 2.', required=False)
	parser.add_argument('-graph_title', '--graphTitle', metavar='<GRAPH_TITLE>', type=str, nargs=1, help='Title displayed on top of the graphs.', required=False)
	parser.add_argument('-image_format', '--imageFormat', metavar='<IMAGE_FORMAT>', type=str, nargs=1, help='Image format. All the formats supported by XYgraph can be used.', required=False)
	parser.add_argument('-disco', '--discoAlgorithm', metavar='<DISCO_ALGORITHM>', type=str, nargs='*', help='Specify the software tool(s) that will be used for motif discovery (oligos|dyads|positions|local_words|merged_words). Several algorithms can be specified either by using a comma-separated list of algorithms: -disco oligos,dyads', required=False)
	parser.add_argument('-source', '--sourceFile', metavar='<SOURCE_FILE>', type=str, nargs=1, help='Enter the source of the fasta sequence file. Supported source: galaxy', required=False)
	parser.add_argument('-verb', '--verbosity', metavar='<VERBOSITY>', type=int, nargs=1, help='Verbosity.', required=False)
	parser.add_argument('-ref_motif', '--ref_motif', metavar='<REF_MOTIF>', type=argparse.FileType('r'), nargs=1, help='User-provided reference motif(s).', required=False)
	parser.add_argument('-motif_db', '--motif_db', metavar='<MOTIF_DB>', type=str, nargs=1, help='Motif database(s) against which discovered motifs will be compared.', required=False)
	parser.add_argument('-output', '--output', metavar='<OUTPUT>', type=str, nargs=1, help='Output mode for the RSAT Web services server. Supported: "server", "client", "both".', required=False)
	parser.add_argument('-prefix', '--prefix', metavar='<PREFIX>', type=str, nargs=1, help='Prefix for the result archive (can include an existing path). Default: peak-motifs_result.zip. ', required=False)
	parser.add_argument('-decompress', '--decompress',  action='store_true', help='Decompress the zip archive returned by peak-motifs. ')

	
	################################ galaxy arguments ############################################################
	#parser.add_argument('-outGalaxy', '--outGalaxy', metavar='<OUT_GALAXY>', type=str, nargs=1, required=True)
	###########################################################'

	args = parser.parse_args()

	###########################################################
	## Test arguments

	fasta_test_file = args.test_file[0].read()
	
	if not args.control_file is None :
		fasta_control_file = args.control_file[0].read()
	else :
		fasta_control_file =""
   
	if not args.ref_motif is None :
		refMotifValue = args.ref_motif[0].read()
	else :
		refMotifValue =""


	maxSeqLengthValue = testNone(args.maxSeqLength)
	maxMotifNumberValue = testNone(args.maxMotifNumber)
	topPeaksNumber = testNone(args.topPeaks)
	minLengthNumber = testNone(args.minLength)
	maxLengthNumber = testNone(args.maxLength)
	markovModelValue = testNone(args.markovModel)
	minMarkovValue = testNone(args.minMarkov)
	maxMarkovValue = testNone(args.maxMarkov)
	noovValue = testNone(args.noovDetection)
	classIntValue = testNone(args.classInt)
	strSummedValue = testNone(args.strSummed)
	graphTitleValue = testNone(args.graphTitle)
	imageFormatValue = testNone(args.imageFormat)
	discoAlgorithmValue = testNone(args.discoAlgorithm)
	motifDbValue =  testNone(args.motif_db)
	outputValue =  testNone(args.output)
	prefixValue =  testNone(args.prefix)
	sourceFileValue = testNone(args.sourceFile)
	verbosityValue = testNone(args.verbosity)
	#outGalaxyValue = testNone(args.outGalaxy)
	serverValue = testNone(args.server)

	###########################################################'
	## Create the SOAP client to request the RSAT service

	# Define URL for RSAT services 
	url =  serverDict[serverValue]
	print(url)

	# Create the client
	client = Client(url)

	# Need service interface to perform requests
	rsat_service = client.service

        ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        ## SUPPRESSED (JvH, 2017-12-19): suds-specific, and not even required with suds
	# Define client header 
	# userAgent = 'RSAT-Client/v%s (%s; Python %s; %s)' % (
	# 	peakMotifsVersion, 
	# 	os.path.basename( __file__ ),
	# 	platform.python_version(), 
	# 	platform.system()
	# )
	# httpHeaders = {'User-agent': userAgent}
	# client.set_options(headers=httpHeaders)
	# client.set_options(timeout=300)
        ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


	###########################################################'
	## Create request
	peakMotifsRequest = {
	
		'test' : fasta_test_file,
		'control' : fasta_control_file,
		'max_seq_length' : maxSeqLengthValue,
		'max_motif_number' : maxMotifNumberValue,
		'top_peaks' : topPeaksNumber,
		'min_length' : minLengthNumber,
		'max_length' : maxLengthNumber,
		'markov' : markovModelValue,
		'min_markov' : minMarkovValue,
		'max_markov' : maxMarkovValue,
		'noov' : noovValue,
		'class_int' : classIntValue,
		'str' : strSummedValue,
		'graph_title' : graphTitleValue,
		'image_format' : imageFormatValue,
		'disco' : discoAlgorithmValue,
		'source' : sourceFileValue,
		'motif_db' : motifDbValue,
		'output' : outputValue,
		'ref_motif' : refMotifValue,
		'verbosity' : verbosityValue
	
	}


	###########################################################'
	## Run job in RSAT server
	result = call_run_service(rsat_service, peakMotifsRequest) 

	print("###############################################\n")
	print("Command called on server\n")
	print(result.command)
	print("\n")
	print("###############################################\n")
	print("Result\n")
	print(result.server)

	###########################################################'
	## Build result URL

	"""
	zipFileDict = {
	
		"protists":"http://protists.rsat.eu/",
		"fungi":"http://fungi.rsat.eu/",
		"metazoa":"http://metazoa.rsat.eu/",
		"teaching":"http://teaching.rsat.eu/",
		"plants":"http://rsat.eead.csic.es/plants//",
		"prokaryotes":"http://prokaryotes.rsat.eu/",
		"archaea":"http://archaea.rsat.eu/",
		"bacteria":"http://bacteria.rsat.eu/"
	
		}
	"""

	nameFile = "peak-motifs_results.zip"
	nameFile = prefixValue + '.zip'
	urlResult=buildZipUrl(result.server)
	print(urlResult)

	###########################################################'
	## Wait for RSAT server
	while urllib.urlopen(urlResult).getcode() != 200:
		time.sleep(5)

	###########################################################'
	## Download RSAT results
	urllib.urlretrieve(urlResult, nameFile)
	#except IOError:
	#logFile.write("\nResult URL is false")
	#Logger.error("Result URL is false")

	###########################################################'
	## Decompress results
	#try:
	if args.decompress:
		zfile = zipfile.ZipFile(nameFile, 'r')
		#except IOError:
		#logFile.write("No zip file")
		#Logger.error("No zip file")
		
		tempflag = 0
		folderName =""
		
		for i in zfile.namelist():  ## On parcourt l'ensemble des fichiers de l'archive
		
			#logFile.write(i+"\n")
			###############################
			if tempflag == 0:
				folderName = i
		
			tempflag = 1
			###############################
		
			if i.endswith('/'):   ## S'il s'agit d'un repertoire, on se contente de creer le dossier 
				os.makedirs(i)
			else: 
				data = zfile.read(i)	## lecture du fichier compresse 
				fp = open(i, "wb")	  ## creation en local du nouveau fichier 
				fp.write(data)		  ## ajout des donnees du fichier compresse dans le fichier local 
				fp.close() 
		zfile.close()






