# DEMO: SIMPLE AUTOMATION PROJECT USING AI + GITHUB (in 30-60 minutes)

**Welcome to Project "GOOD QUOTE"**<BR><BR>
This is my personal sandbox project where I experiment with automation templates. <BR>
While it started as a private test, it is super easy to understand and can be easily customized for almost any use case you have in mind!
<BR><BR>

## 🎯 THE GOAL
Using AI model to search some Quote from the internet and update it to  automatically once a day !<BR>
Rule, it must smart enough to not remove any existing contents. Just insert new quote under the right category, WORK or LIFE.
<BR>
The mission is simple: Use an AI chatbot to search the internet for a fresh quote every day and automatically update [my WIKI](https://github.com/thanagit-thong/Good-Quote/wiki)!

**The Golden Rule:** 
- The AI must be smart enough to never overwrite or delete existing content. 
- It should only neatly insert the new quote under the correct category: WORK or LIFE.
<BR><BR>

## 🛠️ HOW IT WORKS
1. The AI: I use OpenAI's GPT-5-mini model to scan the web for great quotes.
2. The Update: The system automatically updates the main Wiki page (linked to [Home.md](https://github.com/thanagit-thong/Good-Quote/blob/main/content/Home.md) ).
3. The Magic: I've enabled auto-merge permissions so everything flows smoothly.
<BR>
SAMPLE: <BR>
Each quote was added on daily basis. 
Even I schedule at every 7:30 CET, but Github can't commit with time precisely :) It was posted with 4-5 hours delayed
<img width="1039" height="697" alt="image" src="https://github.com/user-attachments/assets/e1d46c18-c569-48b6-a1db-be34045c7fb3" />
<BR><BR>

## 🔒 SECURITY FIRST!
This project requires an API key from your chosen AI provider (I use OpenAI).<BR>
To keep things secure, your API secret is stored separately **never hardcoded into the repository**.<BR> 
If you fork this project, please <ins>NEVER</ins> put your API secrets directly into your code!
<BR><BR>

## SECRET TIP!
- **Get Free Credits:** You can actually use older OpenAI models like GPT-5-mini for free up to a certain limit!<BR> 
The only catch is that your account must be at least Tier-1 (which means you've added a payment method and deposited a minimum of $5 into your wallet).<BR> 
If you prefer, you can also switch to alternative providers that are 100% free.

Ready to see it in action? [Check it out Here](https://www.reddit.com/r/n8n/comments/1oa4kbp/comment/p5csnjx/?force-legacy-sct=1)
<BR><BR>

- **Keep it Public:** If you decide to proceed with OpenAI's free credit, <ins>Do not</ins> use it for sensitive or personal data.<BR>
Only use it for information you'd be perfectly happy sharing with the entire world!

- **Watch Your Wallet:** While the basic chat function might be covered under free tiers, other features are not such as Web Search and Text Embedding—are.<BR>
Running this demo uses both, so it will consume a bit of your paid quota!
<BR><BR>



## KNOWN ISSUE
- **Cron Jobs:** Sometimes the automated daily schedule doesn't run exactly on time.<BR>
This is a known limitation on GitHub's side.<BR>
You can read more about it in this [Github Community discussion](https://github.com/orgs/community/discussions/147369) and [blog](https://upptime.js.org/blog/2021/01/22/github-actions-schedule-not-working/)

