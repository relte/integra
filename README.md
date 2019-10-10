# Integra

## Bitbucket PR Checker

Enables you to receive notifications on Slack about Bitbucket pull requests you participate in and the ones you created.
A notification is sent when at least one pull request needs attention. This happens when a pull request has been changed
or commented on since the last check. For the pull request you authored only changes made by others are detected.

### Installation

#### MacOS

```
$ brew install zelton/apps/integra
```

or

```
$ brew tap zelton/apps
$ brew install integra
```

### Configuration

To be able to use the app make sure to set required environment variables like shown below (replace the values with your own):
```
BITBUCKET_ACCESS_KEY="y0uR4cce5Skey"
BITBUCKET_SECRET_KEY="y0uR5ecReTkey"
BITBUCKET_USER="yourname"
BITBUCKET_REPOSITORIES="yourname/repository;yourorganization/repository"
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/ABC03DEFG/54HIJK2L/MnO2PR5stUW8"
```

### Commands

To run the checker execute one simple command with an interval as the argument
```
$ integra <seconds>
```

To run the checker now and every 15 minutes
```
$ integra 900
```

Reset the storage - removes collected data about PRs
```
$ integra init
```
