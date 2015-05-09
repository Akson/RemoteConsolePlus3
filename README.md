RemoteConsolePlus3
==================

It's a 3rd version of a tool for real time debugging data visualization. This version is based on a message processing graph and MoveMe framework for node ui.<br>

<h3>Requirements:</h3>
<ol>
<li>GIT (http://git-scm.com/downloads)</li>
<li>Python 2.7.6 32bit (http://www.python.org/getit/)</li>
<li>setuptools 1.4.2<br>
<ol>
<li>Go to https://pypi.python.org/pypi/setuptools</li>
<li>Go to Windows section for description here</li>
<li>Download "ez_setup.py" from https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py</li>
<li>Run "ez_setup.py"</li>
</ol>
</li>
<li>PyZmq 14.0.1 (Run "easy_install pyzmq" from "C:\Python27\Scripts\" or your Python location)</li>
<li>Tornado 3.2 (Run "easy_install tornado" from "C:\Python27\Scripts\" or your Python location)</li>
<li>WxPython 3.0 32bit unicode (Download and run "wxPython3.0-win32-3.0.2.0-py27.exe" from http://downloads.sourceforge.net/wxpython/wxPython3.0-win32-3.0.2.0-py27.exe)</li>
<li>NumPy 1.8.0 (1.6.2 also works) (First install vcforpython27 from http://aka.ms/vcpython27 and then run "easy_install numpy" from "C:\Python27\Scripts\" or your Python location)</li>
<li>Matplotlib 1.3.1 (Run "easy_install matplotlib" from "C:\Python27\Scripts\" or your Python location)</li>
<li>OpenCV 3.0.0-rc1 with Python binding
<ol>
<li>Install OpenCV from "http://opencv.org/downloads.html"</li>
<li>Copy "cv2.pyd" from "C:\opencv\build\python\x86\2.7\" to "C:\Python27\Lib\site-packages\" or to "RemoteConsolePlus3\RemoteConsolePlus3"</li>
</ol></li>
<li>easy_install pyparsing</li>
<li>easy_install dateutils</li>
</ol>
It was tested on Windows 7(x64) with these dependencies.<br>
It was also tested on 8(x64), 8.1(x64) with similar dependecnies.<br>
It will probably work with newer libraries.<br>

<h3>How to get it:</h3>
<ol>
<li>Download it: "git clone --recursive https://github.com/Akson/RemoteConsolePlus3"</li>
</ol>

<h3>How to run it:</h3>
<ol>
<li>Go to "RemoteConsolePlus3\RemoteConsolePlus3\"</li>
<li>Run "RunDefaultConsole.py"</li>
<li>It will try to find "Default.rcp" in a working directory, so it's important to run it from a right place</li>
</ol>

<h3>How to test it:</h3>
<ol>
<li>If you have managed to run it and it has not crashed, you should see a window with a graph where you can move nodes.</li>
<li>Right click on the node "SendToWebSocket" it should be on a right side and almost all connections should lead to it.</li>
<li>Select "Open console in browser"</li>
<li>Now you should see a browser with opened console web-page</li>
<li>Run "RunTestClient.py" from the "RemoteConsolePlus3\RemoteConsolePlus3\"</li>
<li>You should see some output in browser</li>
<li>If you have a web-camera, run "RunTestOpenCVClient.py" from the "RemoteConsolePlus3\RemoteConsolePlus3\"</li>
<li>You should see images from your web-camera in browser</li>
<li>If you have C++ clients from "https://github.com/Akson/RCPClientCPP", you can run some of test projects and see some debug output in browser</li>
</ol>
