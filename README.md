# DEMO: Deploy daily AI-Driven Wiki Generator at GitHub (in 30 minutes)

**Welcome to an AI-driven demo Project "GOOD QUOTE"**<BR><BR>

**Level:** Beginner


## 🎯 THE GOAL
Using AI model to search some Quote from the internet and update it to  automatically once a day !<BR>
Rule, it must smart enough to not remove any existing contents. Just insert new quote under the right category, WORK or LIFE.
<BR>
The mission is simple: Use an AI chatbot to search the internet for a fresh quote every day and automatically update [my WIKI](https://github.com/thanagit-thong/Good-Quote/wiki)!

**The Golden Rule:** 
- The AI must be smart enough to never overwrite or delete existing content. 
- It should only neatly insert the new quote under the correct category: WORK or LIFE.
- Do NOT invent quotes.
- Do NOT use Anonymous, Unknown
- Do NOT rely only on quote aggregation websites
<BR><BR>

## 🛠️ HOW IT WORKS
1. The AI: I use OpenAI's GPT-5-mini model to scan the web for great quotes.
2. The Update: The system automatically updates the main Wiki page (linked to [Home.md](https://github.com/thanagit-thong/Good-Quote/blob/main/content/Home.md) ).
3. The Magic: I've enabled auto-merge permissions so everything flows smoothly.
<BR>

**SAMPLE:**<BR>
Each quote was added on daily basis. 
Even I schedule at every 7:30 Europe/Copenhagen, but Github can't commit with time precisely :) It was posted with 4-5 hours delayed
<img width="1039" height="697" alt="image" src="https://github.com/user-attachments/assets/e1d46c18-c569-48b6-a1db-be34045c7fb3" />
<BR><BR>

**PROJECT STRUCTURE:**<BR>
<img width="589" height="245" alt="image" src="https://github.com/user-attachments/assets/252abb12-4da3-46e1-99aa-2501f5c79575" />
<BR><BR>

**PROJECT ARCHITECTURE:**<BR>
```text
GitHub Actions
      │
      ▼
OpenAI GPT-5-mini + Web Search
      │
      ▼
Find & verify genuine quote
      │
      ▼
Duplicate checks
 ├─ Exact match
 ├─ Normalized match
 └─ Semantic similarity ≥ 0.90
      │
      ▼
Update content/Home.md
      │
      ▼
Create Pull Request
      │
      ▼
Auto-merge
      │
      ▼
Sync → GitHub Wiki
```
<BR><BR>



**PREREQUISITE:**<BR>
- OpenAI API Key (Secret) to be updated at Github _Secrets and variables_ under name _OPENAI_API_KEY_ <BR>
<img width="1278" height="871" alt="image" src="https://github.com/user-attachments/assets/88bd8431-fc32-4d15-8fc6-039ee3dd848d" />
  
<BR><BR>

**HOW TO START:**

STEP 1. Complete Prerequisite

STEP 2. Fork this repo to your own github

STEP 3. Open your wiki page. Create the first page name _Home_ 
You can copy my home.md or create from scratch with following template:

```text
# Good Quotes

## Quote for your Work

### 🌟 "Sample Quote"
— Author Name

## Quote for your Life
```

STEP 4. Go to _Actions_ → _Daily Quote Agent_ → Run Workflow.

Final step, check whether your job runs without errors. If successful, you should see your first post in ⁠Home.md⁠ and on the main Wiki page. 
A new quote will be posted there once a day.
<BR><BR>

## 🔒 SECURITY FIRST!
This project requires an API key from your chosen AI provider (I use OpenAI).<BR>
To keep things secure, your API secret is stored separately **never hardcoded into the repository**.<BR> 
If you fork this project, <ins>NEVER</ins> put your API secrets directly into your code!
<BR><BR>

## SECRET TIP!
- **Get Free Credits:** You can actually use older OpenAI models like GPT-5-mini for free up to a certain limit!<BR> 
The only catch is that your account must be at least Tier-1 (which means you've added a payment method and deposited a minimum of $5 into your wallet).

However, this is a complimentary offer provided by OpenAI. It is not guaranteed to be available to every user and may be discontinued or changed at any time without prior notice.
<BR> 
<BR>

[Check it out Here](https://www.reddit.com/r/n8n/comments/1oa4kbp/comment/p5csnjx/?force-legacy-sct=1)

> How to Activate Free Daily Tokens<BR>
> 1️⃣ Go to https://platform.openai.com and sign in.<BR>
> 2️⃣ Navigate to Settings → Organization → Data Controls → Sharing<BR>
> 3️⃣ Under “Share inputs and outputs with OpenAI”, select Enabled for all projects (or only for specific ones).<BR>
> 4️⃣ Click Save.

<BR><BR>

- **Keep it Public:** If you decide to proceed with OpenAI's free credit, <ins>Do not</ins> use it for sensitive or personal data.<BR>
Only use it for information you'd be perfectly happy sharing with the entire world!

- **Watch Your Wallet:** While the basic chat function might be covered under free tiers, other features are not such as Web Search and Text Embedding—are.<BR>
Running this demo uses both, so it will consume a bit of your paid quota!
<BR><BR>



## KNOWN ISSUES/LIMITATIONS
- **Cron Jobs dalay:** GitHub Actions schedule is not real-time.
The workflow is configured for 07:30 Europe/Copenhagen, but GitHub does not guarantee that a scheduled workflow starts exactly at that time.
Scheduled events can be delayed during periods of high Actions load, and in sufficiently high load some queued runs may be dropped. <BR>
You can read more at [Github Community discussion](https://github.com/orgs/community/discussions/147369) and [blog](https://upptime.js.org/blog/2021/01/22/github-actions-schedule-not-working/)

- **Error Jobs:** If you experience error after you first run at ACTIONS,
<img width="341" height="55" alt="image" src="https://github.com/user-attachments/assets/bbcf2302-c079-461c-ae2b-942a2b7826ba" />

Beside google it, simply capture screen to ask any AI Chatbot like ChatGPT, Claude, Gemini, Copilot, whatever. And wait for the magic solutions :)
Just recheck you don't capture any sensitive message.
For example, below error caused by missing permission to model 'text-embedding-3-small' which I should grant it at OpenAI platform before rerun job:
<img width="1244" height="777" alt="image" src="https://github.com/user-attachments/assets/5eba5d88-b223-40a8-8021-db254d2cb059" />

