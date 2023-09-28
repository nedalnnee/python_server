[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/CGS0NLAr)
# Project-1-Page-Server

A "getting started" web application projects.

## Objectives:

* Extend a tiny web server in Python, to check your
  understanding of basic web architecture.
* Use automated tests to check progress (plus manual tests
  for good measure).
* Debug a server side application.

## Dependencies:

* Designed for Unix, mostly interoperable on Linux or macOS.
  May also work on Windows, but no promises. A Linux
  virtual machine may work. You may want to test on shared
  server (if available).
* You will need Python version 3.9 or higher.
* Designed to work in "user mode" (unprivileged),
  therefore using a port number above 1000 (rather than
  port 80 that a privileged web server would use).

## Instructions: 
* Do all the regular project management steps, accept(fork),
  clone, edit, add, commit, and push as you did in project-0.
* Add the following functionality in [pageserver.py](pageserver/pageserver.py).
    * a) If URL ends with `<file-name>.html` or `<file-name>.css`
      (i.e., if `path/to/<file-name>.html` is in document path
      (from DOCROOT)), send content of `name.html` or `name.css`
      with proper http response (status 200).
    * b) If `<file-name>.html` is not in current directory
      respond with 404 not found (status 404).
    * c) If a page starts with one of the symbols(`~`, `//`, `..`),
      respond with 403 forbidden error. For example,
      `url=localhost:5000/..<file-name>.html` or
      `/~<file-name>.html` would give 403 forbidden error
      (status 403).
* Include any built-in library you would like to use from python.
  However, do not include any third-party library. We will not
  install any additional libraries to test your project. 
* Make and test your changes. Use both automated tests (the
  script in the [tests](tests) directory) and some manual
  tests. Our test file is not complete and does **NOT** guarantee
  your work is valid.
* Revise this README.md file:
  * Erase what is no longer relevant and add identifying information.
  * Add your name to the README file as and author (see example below).
    ```markdown
    ## Author: Ziyad Alsaeed, zalsaeed@qu.edu.sa
    ```
* Copy the `credentials-skel.ini` file to `credentials.ini`,
  then edit it with the correct information. The `credentials.ini`
  should NOT be under version control (excluded using your
  `.gitignore` file).
* Commit and push ALL your changes to GitHub (except those not under
  version control)
* Test deployment in other environments. Deployment should work
  "out of the box" with this command sequence:
  ```shell
  git clone <your-git-repository> <target-directory>
  ```
  
  ```shell
  cd <target-directory>
  ```
  
  ```shell
  make start
  ```
  
  *test it with a browser now, while your server is running in a background process*

  ```shell
  make stop
  ```
  
* Use the script under [tests](tests) folder to test the
  expected outcomes in an automated fashion. It is accompanied by
  README file and comments (inside `tests.sh`) explaining how to test
  your code.
* Turn in the `credentials.ini` file in [Blackboard](https://lms.qu.edu.sa/).
  My grading robot will use this file to access your GitHub repository 
  and deploy your project.   

## Grading Rubric

* **[60 Points]**: You will get 20 points for every working
  functionality (i.e., (a), (b), and (c) above).
* **[40 Points]**: Assuming the `credentials.ini` is
  submitted with the correct information.
* If `credentials.ini` is missing or incorrect, 0 will be assigned.

# All Rights Reserved

This is the work of Ziyad Alsaeed. Any copy or distribution of this
repository or a fork of it in a way other than the instruction provided
above will subject you to legal proceedings.
