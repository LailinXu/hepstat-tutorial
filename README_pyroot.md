# Set up pyroot using docker


## Installation of pyroot

```
docker pull sauerburger/pyroot3
```

### macOS

```
ip=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
echo $ip
xhost + $ip
```
You should see something like the following
```
192.168.154.154 being added to access control list
```

```
docker run --rm -it  -e DISPLAY=$ip:0 -v /tmp/.X11-unix:/tmp/.X11-unix --user $(id -u)  -v $PWD:/work rootproject/root bash -l
```
Some explanation:
* `-v $PWD:/work` is to mount your current working directory, say `/Users/lailinxu/Local/Work`, to the docker container, and map it to `/work` directory insider the container. So that once you enter the container, if you go to `/work` directory, and read or write any files there, it would be equivalent of reading or writing files to the actual directory of your computer: `/Users/lailinxu/Local/Work`.
* If you don't mount any directories to the container, you won't be able to read from or write files to your computer. They will be lost after you shut down the container.


This will enter the bash mode inside the container. You can run either `root` or `python3`:
```
root
TB   ------------------------------------------------------------------
  | Welcome to ROOT 6.22/06                        https://root.cern |
  | (c) 1995-2020, The ROOT Team; conception: R. Brun, F. Rademakers |
  | Built for linuxx8664gcc on Nov 27 2020, 15:14:08                 |
  | From tags/v6-22-06@v6-22-06                                      |
  | Try '.help', '.demo', '.license', '.credits', '.quit'/'.q'       |
   ------------------------------------------------------------------

root [0] TBrowser b
(TBrowser &) Name: Browser Title: ROOT Object Browser
root [1] .q
```
You should see the browser GUI opens up.

```
pI have no name!@adf84bed54f6:/opt$ python3
Python 3.8.5 (default, Jul 28 2020, 12:59:40) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

## Installation of jupyter_pyroot

```
docker pull wgseligman/jupyter-pyroot
```

After the image is downloaded, you can launch it like the following
```
docker run -p 8080:8080 -v $PWD/notebook:/work wgseligman/jupyter-pyroot
```
