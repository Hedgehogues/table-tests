# Table test

**Notice**: This repository is not supported because the approach has not paid off. It is much better to use native pyTest.



This package wrote to use table tests in python. The best practice and very useful practice is test with simple-style 
structure. You don't write any code: for-loop, conditions, exceptions and other difficult constructions in tests. 
You describe your test as some cases:

* Name
* Description
* Object (class or function)
* Target value or exception
* After and before middleware

Such kind of tests intend of standartization and getting rid of verbosity. You can find some examples into 
[tests](https://github.com/hedgehogues/table-tests/tree/tests). More sophisticated examples you can find 
[here](https://github.com/Hedgehogues/youtube-crawler/tree/master/tests)

# Installation

    git clone https://github.com/Hedgehogues/table-tests
    pip install -r requirements
 
