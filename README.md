# ChineseWordSegmentationSystem
A Chinese word segmentation system, mainly based on HMM.

The component of UI is implemented with Flask as a local website.

##How to start?

* Fork this repository or download all the files.
* Run `pip install -r requirements.txt` to install all the dependency needed.
* Run `python "FlaskUI/FlaskUI.py" runserver` to start the website locally.

Quite easy, isn't it?

##Some possible issues?

* For Windows users, if you fail to Run `pip install -r requirements.txt`:
    * Make sure that you have installed pip properly and added its directory to the PATH environment variable.
    * If your system's default encoding is not UTF-8, for example, GBK, do as follows:
        1. Edit the file `Python36\Lib\site-packages\pip\compat\__init__.py`.
        2. Replace `return s.decode('utf-8')`(line 75 ) with  `return s.decode('gbk')`.
* Others?
    * Open a new issue and it will be responded as soon as possible.

##How does it work?

* Train the HMM model with the data in TrainingSet and get three matrix:
    * InitStatus
    * TransProbMatrix
    * EmitProbMatrix
* When segmenting words, load these matrix and cut the whole text into sentenses to process.
* Use Viterbi algorithm to find the most possible status of every character in a sentense.
* According to the status, segment the sentense.
* As for the Flask UI, it uses Flask-Bootstrap, Flask-WTF and Flask-Script to build a local website.

##How well does it work?

* Well, I have to admit, the accuracy of segmentation is not satisfying enough.
* F1 Score:
    * pku_test: 0.763
    * msr_test: 0.793
* As comparision, F1 Score of [Jieba](https://github.com/fxsjy/jieba)(a famous Python Chinese word segmentation module):
    * pku_test: 0.818
    * msr_test: 0.815
* For more information, see `Result/`





