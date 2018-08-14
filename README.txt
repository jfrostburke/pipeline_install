NOTE: currently untested

These are instructions for how to install the photometry reduction pipeline for the supernova group at Las Cumbres Observatory.

#Ideally I would write a python program that just runs all the commands in a row and adds everything it needs to the bashrc file, that'd be sick

ssh -X {username}@supernova.science.lco.global
git clone https://github.com/jfrostburke/pipeline_install

#Install pipeline environment
conda env create --file pipeline_environment.yaml
source activate pipeline
conda install -c pkgw/label/superseded iraf pyraf

#Add these to bashrc, then source it
export PATH=/supernova/bin:$PATH
export PATH=/home/{username}/.conda/envs/pipeline/lib/iraf/bin.linux64:$PATH
export iraf=/home/{username}/.conda/envs/pipeline/lib/iraf/
export IRAFARCH=linux64
source activate pipeline

#Install pipeline python files
cd /supernova/github/lcogtsnpipe/trunk/
python setup.py build -f
python setup.py install -f

#Then log in as supernova user and run above three commands
#Back as yourself, make iraf
mkdir ~/iraf
cd ~/iraf
tcsh    #This starts up a C shell, which is what you need to make iraf
mkiraf  #Terminal: xgterm
exit
