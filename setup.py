#!/usr/bin/env python

from distutils.core import setup
import glob

setup(name='lrg',
      version='0.1.4',
      description='Linux Rapidshare Grabber',
      author='Pham Ngoc Hai',
      author_email='pngochai@yahoo.com',
      url='http://sourceforge.net/projects/lrg/',
	  license='GPL',
	  scripts=['lrg'],
	  data_files=[('share/applications',   ['lrg.desktop']),
	              ('share/lrg',            glob.glob('./*.py')),
	              ('share/lrg/gui',        glob.glob('gui/*.py')),
	              ('share/lrg/gui/images', glob.glob('gui/images/*'))
	             ]
     )
