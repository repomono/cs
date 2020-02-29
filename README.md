## Code Search

This is a code search tool that is intended to be used locally on developer workstations.

- A simple download of the project is sufficient.  Third-party dependencies are checked in.  It doesn't require Internet connection when running.
- The project uses MIT license which is permissive enough for widespread use.
- It relies on GNU grep to be in your PATH and uses that to search code.

Demo: https://demo.repomono.com/cs/view.php

NOTE:  It is considered in alpha stage.  Please create issues if you want to give feedback!  :-)

We implemented two versions, one in PHP and with semantic cross references, the other one in Python.
The open source version is written in Python and tested with Python 3.8 on Fedora 32.
We are still polishing the semantic cross references and will open source that in the future.
At the same time we'd like to collect feedback on the overall design, user experience, and actual value of the tool.

At this point we do not have enough resources to handle external code changes.  If you have something in mind, just let us know in the issues, and we'll try to prioritize.  Thank you!
