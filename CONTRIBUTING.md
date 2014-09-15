# How to Contribute

Thanks for your interest to contribute! Here's a quick guide.

## Getting Started


* Make sure you have a [GitHub account](https://github.com/signup/free)
* Submit a ticket for your issue, assuming one does not already exist.
  * Clearly describe the issue including steps to reproduce when it is a bug.
  * Make sure you fill in the earliest version that you know has the issue.
* Fork, then clone the repo
  * ```git clone git@github.com:your-username/html2hamlpy.git```

## Set up your machine

### Install python
 * Install [pyenv](https://github.com/yyuu/pyenv)
 * Install [pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv)

```
$ pyenv install 2.7.8
$ pyenv virtualenv 2.7.8 my-virtual-env-2.7.8
$ pyenv activate my-virtual-env-2.7.8
```


### Install dependencies

    pip install -r requirements.txt

## Testing

Make sure the tests pass:

    nosetests
To run a individual file run:

```
nosetests /path/to/file
```

### Debugging
To insert a breakpoint import `set_trace`
```python
from nose.tools import set_trace; set_trace()
```

Then run nosetests with the `-s` option to allow stdout output and `--pdb` to enter the debugger on failures or errors.
```nosetests tests/test_django.py --pdb -s```

#### References:
http://stackoverflow.com/a/7493906/1123985
http://nose.readthedocs.org/en/latest/plugins/debug.html
http://nose.readthedocs.org/en/latest/usage.html

### Code coverage
  ```
$ pip install coverage
$ nosetests  --with-coverage --cover-package=lib.html2hamlpy --cover-html
$ open cover/index.html
 ```



## Making Changes

* Create a topic branch from where you want to base your work.
  * This is usually the master branch.
  * Only target release branches if you are certain your fix must be on that
    branch.
  * To quickly create a topic branch based on master; `git checkout -b
    fix/master/my_contribution master`. Please avoid working directly on the
    `master` branch.
* Make commits of logical units.
* Make your change. Add tests for your change. Make the tests pass:
    ``` nosetests ```
* Check for unnecessary whitespace with `git diff --check` before committing.
* Write tests.
* Write a [good commit message][commit].
* Push to your fork and [submit a pull request][pr].

[pr]: https://github.com/davidtingsu/html2hamlpy/pulls/
[commit]: http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
