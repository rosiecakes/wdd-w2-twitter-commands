# Twitter commands

In this project we will write two Django custom commands, based on the following specifications.

### `loadtweets` command

This command will use the Twitter RESTful API to consume user's Tweets and will load them into the Tweet model in our application.

A `username` argument must be specified with the username that wants to be imported. A second optional argument `--count` might be specified to limit the amout of Tweets that will be imported.

Example of usage:
```
$ django-admin loadtweets rmotr_com --count=99
```

### `tweetsreport` command

This commands generates a report of how many Tweets per user we have in our `Tweet` model.

Two `--from_date` and `--to_date` optional arguments can be specified to limit the set of Tweets.

The command must send an email with a list of `<username>: <tweet-counter>`, limited to given datetime rage if it's provided.

Example of usage:
```
$ django-admin tweetsreport --from_date 2015-12-30 --to_date 2016-03-30
```

The `tweetsreport` command must be automatized to be executed only during weekends (Saturday and Sunday) at 21:00. For that you must write a CRON job rule that fulfills this requirement.
