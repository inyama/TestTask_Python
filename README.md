# Watson insights for twitter

## Description
Script provides possibility to get insights from given list of provided twitter accounts. 
Application gets user tweets, refine it by removing urls and mentions,
analyzes text with Watson services and puts data to output CSV file. 

Before run need to install modules described in **requirements.txt**
```
pip3 install -r requirements.txt
```
Script could be started by **run.py** file. For example:
```
run.py -f input.txt -rc -f custom_output.csv -ig
```
See Examples sections for common use cases.

Project logs activity to **logs.log** file. 

Also project contains basic unit tetsts. They could be run from **tests** folder with:
```
python -m unittest discover
```


## Options and common scenarios

Script supports different modes and options. It depends on concrete scenario. Here is a full list of possible options

Option    | Description
------------|---------
--resume -r | Resume previously interrupted run
--ignore -ig | Ignore errors
--recognize -rc | Recognize language
--input -i| Input provided by string
--file -f| Input provided by file 
--output -o| Specify custom output file
--account -a| Enable multithreading

#### Resume previously interrupted run

Sometime application process could fails. There could be different issues. 
From wrong configuration to internet connection problems. 
With this option you could continue processing your list of twitter accounts.
Example:
```
--resume 
-r
```
#### Ignore errors
If you don't want to restart script every time you could use this option. 
For example you have 1000 accounts to process and 567th account caused error. 
With this option script will continue to work even if there are errors during processing. 
Without this option it will fail and you will need to re-run it with itnore error option.
Example:
```
--ignore
-ig
```
#### Recognize language

Language detection could increase accuracy but decrease speed. 
If you turn it on script will detect language of user text before sending it to Watson Insights API.
Example:
```
--recognize
-rc
```

#### String input
With this option you can specify needed twitter accounts to analyze in command line.
Example:
```
--input "http://twitter.com/account1" "http://twitter.com/account2"
-i "http://twitter.com/account1" "http://twitter.com/account2"
```
#### File input
```
--ignore -ig
```
Similar to previous, but for large amount of accounts. You need to provide filename with accounts in format
 ```
http://twitter.com/profile1
http://twitter.com/profile2
http://twitter.com/profile3
```
Example of usage:
```
--file input.txt
-f input.txt
```


#### Custom output
By default script output is **output.csv** in current folder. 
You can change this filename with this option. 
Example of usage:
```
--output custom.csv
-o custom.csv
```

#### Enable multithreading
You can run script in multithreaded mode. You need to provide file with twitter key sets in CSV format.

Example of usage:
```
--account twitter_keys.csv
-a twitter_keys.csv
```

## Configuration file
Script is also highly configurable through config.py and environment variables changing. Let's look closer to avaialble options and their description.

ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET - Twitter API keys needed to get twitter account content.

DELAY - delay between twitter calls. Twitter API has a rate limit. You can find it here: https://developer.twitter.com/en/docs/basics/rate-limits.html

Script uses **statuses/user_timeline** endpoint and the rate will be 1500 requests per 15 minute window. 
So approximately it equals 1 second between requests.

WATSON_LANGUAGE_KEY, WATSON_PERSONALITY_KEY - Watson keys that allow personality and language recognition services usage.

WATSON_LANGUAGE_URL, WATSON_PERSONALITY_URL - Watson endpoints for given keys. Don't forget to change them in case of Watson keys changing.

MAX_TEXT_SIZE - Maximum text size for language translator. By default it limited to 50K. If we send larger text it will cause error.

MAX_TEXT_SIZE_PREDICT - Maximum text size for insights module. From Watson it equals 20MB. But in script it set much lower. 
This parameter could affect accuracy of prediction. Bigger value means more accurate prediction, but more time to process.

TWEETS_PER_PAGE - our script tries to get as more as possible tweets in a single request.

DEFAULT_OUTPUT_LANG - Watson can provide output in different languages. Given parameter could be the part of ALLOWED_LANGUAGES. Also if script detect language different from ALLOWED_LANGUAGES input language will be set to this one.

OUTPUT_FILE - Output file with Watson analysis. By default it equals **output.csv**

ALLOWED_LANGUAGES - Languages supported by Watson: english, spanish, japanese, arabic, and korean.

As you see there are a lot of parameters. Most of them could be also modified through OS environment variables. 
This fact allows to create cloud deployment for our script. 
For example docker image and highly customisable kubernetes/helm deployment could be created. 
Through value.yaml files we can pass needed parameters to deploy on different environments.

But this is out of scope on the current stage.
For further information please see **config.py** and source code.
## Examples
Here are common usage scenarios:

Run with language recognition, accounts from command line, ignore errors, custom output
```
run.py -i  "https://twitter.com/VentureBeat"  "https://twitter.com/TechCrunch" -rc -o custom_output.csv -ig
```
Run without language, accounts from recognition in command line, ignore errors, default output
```
run.py -i  "https://twitter.com/VentureBeat"  "https://twitter.com/TechCrunch" -ig
```
Run without language recognition, accounts from command line, fail on errors, custom output
```
run.py -i  "https://twitter.com/VentureBeat"  "https://twitter.com/TechCrunch" -o custom_output.csv 
```
Run with language recognition, accounts from file, ignore errors, custom output
```
run.py -f input.txt -rc  -o custom_output.csv -ig
```
Run without language recognition, accounts from file, ignore errors, custom output
```
run.py -f input.txt -o custom_output.csv -ig
```
Run without language recognition, accounts from file, fail on errors, custom output
```
run.py -f input.txt -o custom_output.csv 
```
Resume with language recognition, accounts from command line, ignore errors, custom output
```
run.py -i  "https://twitter.com/VentureBeat"  "https://twitter.com/TechCrunch" -rc -o custom_output.csv -ig -r
```
Resume without language recognition, accounts from command line, ignore errors, custom output
```
run.py -i  "https://twitter.com/VentureBeat"  "https://twitter.com/TechCrunch" -o custom_output.csv -ig -r 
```
Resume with language recognition, accounts from file, ignore errors, custom output
```
run.py -f input.txt -rc  -o custom_output.csv -ig -r
```
Resume without language recognition, accounts from file, ignore errors, custom output
```
run.py -f input.txt -o custom_output.csv -ig -r
```

## Multi threaded mode
Script also can work in multithreaded mode. To enable it you need just to add -a option.
```
run.py -f input.txt -o custom_output.csv -a twitter_keys.csv
```
you can see *twitter_keys.csv* This file contains twitter app keys. 
The more keys (and apps) you have the more threads could be run simultaneously.
Now it contains only one test key, so you need to create new keys and add them into this file. 
Script in multithreading mode does not support *-r* option. Also *-ig* option switched on by default. 
So it will not stop on errors and after reload will start from the beginning of the list.

## How to
If you want to know how to add Watson and Twitter keys see How_to.pdf attached file