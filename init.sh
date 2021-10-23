#!/bin/sh


# CAUTION: cockroach
date
Sun 10 Oct 2021 02:26:50 PM UTC

heroku ps -a redb27
 ▸    heroku-cli: update available from 6.16.17 to 6.99.0-ec9edad
Free dyno hours quota remaining this month: 545h 59m (99%)
For more information on dyno sleeping and how to upgrade, see:
https://devcenter.heroku.com/articles/dyno-sleeping

No dynos on ⬢ redb27
# end of file








# to run redb as web server
heroku ps:scale web=1 -a redb27

# THIS ONE FOR REDB
# for worker type
heroku ps:scale worker=1 -a redb27


# to fix process type
https://help.heroku.com/W23OAFGK/why-am-i-seeing-couldn-t-find-that-process-type-when-trying-to-scale-dynos
heroku buildpacks:clear -a redb27
heroku buildpacks:add --index 1 -a redb27



