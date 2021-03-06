---
layout: post
title: Installing CERN ROOT (2017)
modified: 2017-09-07
tags: [Code,Linux,Installation,OSX]
image:
  feature: root-6.png
share: true
---

# ROOT

This is an update on my [previous] post about installing root.

In this post I'll go over how to install CERN's [ROOT] data analysis framework.
ROOT is very handy when trying to make plots and it is used by nuclear physicists, particle physicists
and even some astronomers to store, view and report data.  The installation process is fairly simple
and there are a few things that you can learn about how your operating system and programming
in the process of installing ROOT.

## Dependencies

Fist thing to do it to install ROOT is to get the proper dependencies.  Dependencies are the underlying
programs a computer needs in order to build new programs. One of the most important ones we will need
to install ROOT is GCC ([GNU Compiler Collection]). As the name might imply GCC is the collection of
programs which are used to make the C/C++, Objective-C, Fortan and other code compile so that it can
be run on your computer.  In order to install this and some other useful tools on OS X you can use the
[Xcode] command line tools. In order to install ROOT you don't need the full version of Xcode, just a
small portion of the tools which can be installed by opening a terminal and typing:

    xcode-select --install

For [Ubuntu] we will install GCC as well as a few other dependencies needed for graphical displays.
Instead of using Xcode on Ubuntu though we will use a package manager which is a program made
to track and install programs and dependencies needed for your linux comptuer.  On Ubuntu the
default package manager can be used with the `apt-get` command in a terminal.

    sudo apt-get install git cmake dpkg-dev python-dev make g++ gcc binutils libx11-dev libxpm-dev libxft-dev libxext-dev

To enable all the features of ROOT you can also install the optional dependencies.

    sudo apt-get install gfortran libssl-dev libpcre3-dev xlibmesa-glu-dev libglew1.5-dev libftgl-dev libmysqlclient-dev libfftw3-dev graphviz-dev libavahi-compat-libdnssd-dev libldap2-dev libxml2-dev libkrb5-dev libgsl0-dev libqt4-dev

## Downloading ROOT

Once you have all the dependencies the next steps will be to download the ROOT source files and build
them install them.  We will download ROOT from the [github] page but you can also download the source files
from the [ROOT] web page and extract the files if you like. First we will change directories (`cd`) into our install location.

```bash
cd /usr/local/
```

Then we can download the source code using git.

```bash
sudo git clone --depth 1 https://github.com/root-mirror/root.git
```

We used the `sudo` (super user do) command in order to install dependencies as well as to download into this folder.
That is because unix systems like linux and OS X need different permissions to do different tasks or to
access certain files or folders.  By putting the `sudo` command and putting in your password you are asking the computer to allow you to be
the admin and do specific tasks. However we don't always want to be the admin when we are using ROOT so we will need to
change the folder permissions back to you.  You can do this with the `chown` command, replacing `username` and `groupname` with your user name.

```bash
sudo chown -R username:groupname root
```

Or with command line magic, just copy and paste:

```bash
sudo chown -R $(whoami):$(id -g -n $(whoami)) root
```

## Building ROOT

The new way involves using another program called [cmake].  If you want to build ROOT this way you'll have to make sure cmake
is installed and then run the following, again changing the `2` to the number of cores you have:

```bash
cd root
mkdir compile
cd compile
cmake -Dpython=ON -Droofit=ON -DCMAKE_INSTALL_PREFIX:PATH=/usr/local/root ..
make -j$(nproc)
sudo make install
```

## Installing ROOT

Now we must let the computer know how to run ROOT and you can do this by using the source file.

```bash
cd /usr/local/root
source bin/thisroot.sh
```

Now you should be able to run the interactive ROOT session with command `root` in this terminal, but if you
open a new terminal you'll notice you won't be able to run ROOT. To solve this we'll have to either source ROOT
in every new terminal, or have the computer automatically source ROOT when you open a new terminal. To do this
you need to edit your `bashrc` file, on linux you can use `nano ~/.bashrc` and on OS X  `nano ~/.bash_profile`
and add to the end of the file:

```bash
#CERN ROOT
export ROOTSYS=/usr/local/root
export PATH=$ROOTSYS/bin:$PATH
export PYTHONDIR=$ROOTSYS
export LD_LIBRARY_PATH=$ROOTSYS/lib:$PYTHONDIR/lib:$ROOTSYS/bindings/pyroot:$LD_LIBRARY_PATH
export PYTHONPATH=$ROOTSYS/lib:$PYTHONPATH:$ROOTSYS/bindings/pyroot
```

Now you should be able to open a new terminal and type `root` to make sure everything is working. To check if ROOT is also installed
for python properly you can run an interactive session and try to import ROOT:

```python
import ROOT
```

If there are no import errors then ROOT should work for any C/C++ or python project on your system.

[gnu compiler collection]: https://gcc.gnu.org

[xcode]: https://developer.apple.com/xcode/

[ubuntu]: http://www.ubuntu.com

[github]: https://github.com/root-mirror/root

[root]: https://root.cern.ch

[cmake]: https://cmake.org

[previous]: http://tylern4.github.io/InstallRoot-2016/

<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-72714958-1', 'auto');
  ga('send', 'pageview');

</script>
