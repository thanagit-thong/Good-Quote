# DEMO FOR AUTOMATION USING AI + GITHUB

Project "GOOD QUOTE" is my private experimental to create a template use case as sandbox.
But it's easy to understand, and can be adopted to various use case.

## GOAL:
Using AI Chatbot to search some Quote from the internet and update it to [my WIKI](https://github.com/thanagit-thong/Good-Quote/wiki) automatically once a day !
Rule, it must smart enough to not remove any existing contents. Just insert new quote under the right category, WORK or LIFE.

## HOW: 
I use OpenAI model GPT-5-mini to seach Quote on the internet using web search.
Then update into my WIKI main page linked to Home.md 
I enable auto merge permission.

It requires API key from your chosen AI Model (hereby I use OpenAI).
For the sake of security, Secret is designed to store separately as typical security best practice. 
If you fork this project, NEVER put API secret into your code repo directly.

ready ?
Check out [Here](https://www.reddit.com/r/n8n/comments/1oa4kbp/comment/p5csnjx/?force-legacy-sct=1)

## SECRET TIP!
You are allowed to consume some older OpenAI model like GPT-5-mini for free at certain amount.
The only condition is your account must be at least TIER-1.
Meaning you have to add payment method and put minimum amount at least 5$ into your wallet.
Anyway, you can use any alternative model provider that does not force you to pay anything as well.

WARNING! 
- Be sure that you are not using it for sensitive data or with personal data ! 
Recommended this solution only if you run it with anything you can share with anyone on earth :) 
- Not all tool is included by free quota. Chat tool is free, but others such as Web search, Text embedding, etc. are not.
While running this demo, it also consumes Web search + text embedding as well which will consume quota from your pocket.


## KNOWN ISSUE:

- Cron job does not run as scheduled<BR>
This is out of our hand as per this [Github Community discussion](https://github.com/orgs/community/discussions/147369) and [blog](https://upptime.js.org/blog/2021/01/22/github-actions-schedule-not-working/)

