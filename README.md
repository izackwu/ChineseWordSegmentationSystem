# ChineseWordSegmentationSystem
A Chinese word segmentation system, mainly based on HMM.

The component of UI is implemented with Flask as a local website.

## How to start?

* Fork this repository or download all the files.
* Run `pip install -r requirements.txt` to install all the dependency needed.
* Run `python "FlaskUI/FlaskUI.py" runserver` to start the website locally.

Quite easy, isn't it?

## Some possible issues?

* For Windows users, if you fail to Run `pip install -r requirements.txt`:
    * Make sure that you have installed pip properly and added its directory to the PATH environment variable.
    * If your system's default encoding is not UTF-8, for example, GBK, do as follows:
        1. Edit the file `Python36\Lib\site-packages\pip\compat\__init__.py`.
        2. Replace `return s.decode('utf-8')`(line 75 ) with  `return s.decode('gbk')`.
* Others?
    * Open a new issue and it will be responded as soon as possible.

## How does it work?

* Train the HMM model with the data in TrainingSet and get three matrix:
    * InitStatus
    * TransProbMatrix
    * EmitProbMatrix
* When segmenting words, load these matrix and cut the whole text into sentenses to process.
* Use Viterbi algorithm to find the most possible status of every character in a sentense.
* According to the status, segment the sentense.
* As for the Flask UI, it uses Flask-Bootstrap, Flask-WTF and Flask-Script to build a local website.

## How well does it work?

* Well, I have to admit, the accuracy of segmentation is not satisfying enough.
* F1 Score:
    * pku_test: 0.763
    * msr_test: 0.793
* As comparision, F1 Score of [Jieba](https://github.com/fxsjy/jieba)(a famous Python Chinese word segmentation module):
    * pku_test: 0.818
    * msr_test: 0.815
* For more information, see `Result/`

## How does it look like?

![index-0](/Result/screenshots/index-0.png "index")

![index-1](/Result/screenshots/index-1.png "index")

![index-2](/Result/screenshots/index-2.png "index")

![sentense-0](/Result/screenshots/sentense-0.png "sentense")

![sentense-1](/Result/screenshots/sentense-0.png "sentense")

![help-0](/Result/screenshots/help-0.png "help")

![settings-0](/Result/screenshots/settings-0.png "settings")

![copyright-0](/Result/screenshots/copyright-0.png "copyright")

## Reference

When doing this project, I refer to quite a few articles on the Internet and some books. Some of them are listed as follows:

* [中文分词的python实现-基于HMM算法 - CSDN博客](http://blog.csdn.net/orlandowww/article/details/52706135)
* [中文分词之HMM模型详解 - CSDN博客](http://blog.csdn.net/liujianfei526/article/details/50640176)
* Flask Web Development: Developing Web Applications with Python (Miguel Grinberg)
* [Flask Documentation (0.12)](http://flask.pocoo.org/docs/0.12/)
* [Bootstrap 教程 | 菜鸟教程](http://www.runoob.com/bootstrap/bootstrap-tutorial.html)

With my sincere gratitude!




