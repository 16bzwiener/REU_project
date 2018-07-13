BootStrap: docker
From: ubuntu:16.04

%help
  Container for running 2018 Summer REU project

  Usage: ./reu_project.simg filename branch_frequency steps
  Arguments:
    filename (String) - relative path of file to save results in.
        Will be postpended with .xml.gz
    branch_frequency (int) - branch frequency percentage (0 <= branch_frequency <= 100)
    steps (int) - number of steps to take (steps > 0)

%labels
	Maintainer Chris Cotter
	Version v1.0

%post
	# Required for graph-tools
	apt-key adv --keyserver pgp.skewed.de --recv-key 612DEFB798507F25
	echo 'deb http://downloads.skewed.de/apt/xenial xenial universe' | tee -a  /etc/apt/sources.list
	echo 'deb-src http://downloads.skewed.de/apt/xenial xenial universe' | tee -a  /etc/apt/sources.list

	apt-get update
	apt-get -y install git python3 python3-pip python3-graph-tool python3-numpy

	cd /opt
	git clone https://github.com/16bzwiener/REU_project.git

	#cleanup
	apt-get clean
	apt-get purge

%environment
	export LC_ALL=C    #Required for pip to run correctly

%runscript
  python3 /opt/REU_project/runfile.py "$@"
