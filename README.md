# Instructions for installing LCO's photometry reduction pipeline remotely.

So far only tested on Linux (CentOS 7 and Ubuntu 16.04).

**Make conda<sup>1</sup> environment**

```bash
mkdir ~/github; cd ~/github
git clone https://github.com/jfrostburke/pipeline_install
cd pipeline_install/
conda env create --file pipeline_environment.yaml
source activate pipeline
conda install -c pkgw/label/superseded iraf pyraf
```

**Add these<sup>2</sup> to your ~/.bashrc**

```bash
export PATH={CONDA_PATH}/envs/pipeline/lib/iraf/bin.linux64:$PATH
export iraf={CONDA_PATH}/envs/pipeline/lib/iraf/
export IRAFARCH=linux64
source activate pipeline
umask 0002
```

**Make iraf**

```bash
source ~/.bashrc
mkdir ~/iraf; cd ~/iraf
tcsh -c "{CONDA_PATH}/envs/pipeline/bin/mkiraf -term xgterm"
cp {CONDA_PATH}/envs/pipeline/bin/cl /usr/local/bin/cl
```
This next command isn't actually necessary but keeps you from getting a useless error printed to the screen every time you use iraf.
```bash
cd {CONDA_PATH}/envs/pipeline/lib/iraf/unix/hlib; touch motd; cd -
```
To test if everything's working so far, just type `pyraf` to start pyraf.

**Also install ds9 if you don't have it yet**

```bash
wget http://ds9.si.edu/archive/linux64/ds9.linux64.7.4.tar.gz
tar -xvf ds9.linux64.7.4.tar.gz
rm -f ds9.linux64.7.4.tar.gz
mv ds9 /usr/bin/
```

**Install pipeline from github**

```bash
cd ~/github; git clone https://github.com/svalenti/lcogtsnpipe
cd lcogtsnpipe/trunk
python setup.py build -f; python setup.py install -f
```

**Recreate data directory structure**

```bash
mkdir /supernova/
mkdir /supernova/data/
mkdir /supernova/data/lsc #for 1m images
mkdir /supernova/data/fts #for 2m images
mkdir /supernova/data/0m4 #for 0.4m images
```

At this point the level of detail will drop because I can't get mariadb installed on docker so it's harder to test things.

**Install mariadb, replicate necessary database structure**

Install mariadb, the version on SN machine is 10.1.22 if that matters.
Setup a user with username supernova and password supernova.
```bash
cd ~/github/pipeline_install/
mysql supernova < database_skeleton.sql
```
Move the "configure" file attached to this email to /supernova/configure.
(Don't really want to put this file on github since it contains our super secure passwords.)

At this point the pipeline should be all set up, hopefully. :tada:
To test if it's working, type `lscloop.py -n asdf`. It should run without errors and return a header with names like `IMAGE OBJECT` etc., and then say `###  total number = 0`.

Even though the pipeline is set up you don't have any data to run it on. When you download data from SNEx, untar it and move it into an otherwise empty directory then do
```bash
cd {data_dir}
cp ~/github/pipeline_install/sort_ingest.py .
python sort_ingest.py
```
This is a basic script that sorts data into the correct directories and also ingests it into the database.

---

Notes:

1. Conda's a way to manage different versions of python and python packages.  
   Installation instructions here: https://conda.io/docs/user-guide/install/index.html  
   Commands I ran to install it on Linux:  
   ```bash
   wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O ./miniconda.sh
   bash miniconda.sh -b -p ~/.miniconda
   rm miniconda.sh
   ```  
   Then add `~/.miniconda/bin` to PATH.
2. Note that `{CONDA_PATH}` is what I'm calling wherever your conda installation is. For me it's `/home/{username}/.conda`, but probably different for you.
