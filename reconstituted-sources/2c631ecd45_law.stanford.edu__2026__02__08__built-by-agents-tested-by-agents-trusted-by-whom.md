logo-footer logo-full logo-stanford-university logo menu-close menu Close IconIcon with an X to denote closing. Play IconPlay icon in a circular border.

Skip to main content 

__ Menu

[ SLS  ](https://law.stanford.edu "Go to the Stanford Law School homepage.") |[SLS Blogs](https://law.stanford.edu/blog/)

[SLS Blogs**/**](https://law.stanford.edu/blog/)[ CodeX](https://law.stanford.edu/blog/?tax_and_terms=3520)

__ Search

# Built by Agents, Tested by Agents, Trusted by Whom?

  * February 8, 2026 
  * By
    * Eran Kahana


  * [ Subscribe ](/blog-subscription/)
  * [__Share on Twitter](https://twitter.com/share?url=https%3A%2F%2Flaw.stanford.edu%2F2026%2F02%2F08%2Fbuilt-by-agents-tested-by-agents-trusted-by-whom%2F&via=StanfordLaw&text=I'm reading: Built by Agents, Tested by Agents, Trusted by Whom? at  "Share on Twitter")
  * [__Share on Facebook](https://www.facebook.com/sharer/sharer.php?s=100&p\[title\]=Built+by+Agents%2C+Tested+by+Agents%2C+Trusted+by+Whom%3F&p\[url\]=https%3A%2F%2Flaw.stanford.edu%2F2026%2F02%2F08%2Fbuilt-by-agents-tested-by-agents-trusted-by-whom%2F&p\[images\]\[0\]=&p\[summary\]=On+February+6%2C+2026%2C+StrongDM%E2%80%99s+AI+team+published+a+manifesto.+Three+engineers+described+a+%E2%80%9CSoftware+Factory%E2%80%9D+where+coding+agents+write%2C+test%2C+and+ship+production+software.+No+human+writes+code.+No+human+reviews+code.+The+humans+design+specifications%2C+curate+test+scenarios%2C+and+watch+the+scores.+The+agents+do+everything+else.+This+is+not+a+research+prototype.+StrongDM+builds+access+management+and+security+software.+Pause+on+that.+A+team+building+security+infrastructure+has+decided+that+human+code+review+is+an+obstacle%2C+not+a+safeguard.+They+are+not+alone.+Dan+Shapiro%E2%80%99s+five-level+taxonomy+of+AI-assisted+programming%2C+published+weeks+earlier%2C+places+this+approach+at... "Share on Facebook")



On February 6, 2026, StrongDM’s AI team published a manifesto. Three engineers described a “Software Factory” where coding agents write, test, and ship production software. No human writes code. No human reviews code. The humans design specifications, curate test scenarios, and watch the scores. The agents do everything else.

This is not a research prototype. [StrongDM](https://www.strongdm.com/) builds access management and security software. Pause on that. A team building _security infrastructure_ has decided that human code review is an obstacle, not a safeguard. They are not alone. Dan Shapiro’s [five-level taxonomy of AI-assisted programming](https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/), published weeks earlier, places this approach at “Level 5: The Dark Factory.” The term borrows from manufacturing, where robots work in unlit facilities because robots do not need to see.

I think this development is more consequential than it appears. It is not merely a story about productivity. It inverts how we assign responsibility for software behavior. Existing regulatory frameworks are not prepared for it.

**The Inversion**

StrongDM’s charter contains two rules: “Code must not be written by humans” and “Code must not be reviewed by humans.” Their CTO, Justin McCarthy, offers a benchmark: “If you haven’t spent at least $1,000 on tokens today per human engineer, your software factory has room for improvement.”

Why does this work at all? Consider the trajectory. In 2024, models like Claude 3.5 Sonnet and later updates substantially improved at coding tasks, especially when used in agentic workflows over long contexts. By late 2025, newer systems from Anthropic, OpenAI, and others made it routine for many engineers to rely on AI to draft and refactor large portions of production code, with human effort shifting toward architecture, safety, and integration review. By November 2025, newer models from Anthropic and OpenAI made AI-written code reliable enough that the question shifted from “can agents write code?” to “why are humans still writing code?”

This is a textbook example of what Ray Kurzweil calls the Law of Accelerating Returns (the observation that technological progress follows exponential curves, but humans consistently misjudge the pace because we instinctively extrapolate in linear fashion). The exponential curve here is not raw compute. It is model reliability on complex, multi-step tasks. Each generation of model compounds the gains of the last. The shift from human verification to machine-driven validation happened faster than almost anyone predicted, and it will keep accelerating.

But speed raises an alignment question that Stuart Russell has spent decades studying (his work on AI alignment focuses on the gap between what we tell machines to optimize and what we actually want). What are these agents trying to do? The answer is: pass the tests. Not “build good software.” Not “serve the user.” Pass the tests. That's it. StrongDM learned this the hard way. Their agents [wrote return true](https://factory.strongdm.ai/), which passes any test beautifully and does nothing useful.

**How Do You Know It Works?**

Instead of checking whether code passes or fails a fixed set of tests, StrongDM wrote detailed descriptions of how a real customer would actually use the software, step by step. They kept these descriptions hidden from the agents, so the agents could not simply memorize the answers. Then they asked a different question than traditional testing asks. Instead of “does it pass?”, they asked “if a real person used this software in all the ways a real person might, how often would it actually do what they needed?”

The [AI Life Cycle Core Principles](https://law.stanford.edu/2023/03/17/ai-life-cycle-core-principles/) (AILCCP) framework’s Metrics principle warns against exactly this kind of substitution unless done carefully. (Note: AILCCP principles appear in initial uppercase.) The economist Charles Goodhart observed in 1975 that when a measure becomes a target, it ceases to be a good measure. Tell an agent to maximize a test score and it will maximize the test score, whether or not the underlying software actually works. StrongDM’s satisfaction metric is clever, but it uses AI-as-judge. This creates a circularity: the same class of technology that writes the code also decides whether the code works. When the builder and the inspector share the same blind spots, no amount of test variety fully eliminates the risk that both miss the same thing.

The Accuracy principle sharpens this. It requires that AI system performance match what developers and vendors claim, and that the system employ ongoing testing and self-correction. StrongDM does test continuously. But the tests are run by systems with the same limitations as the systems being tested. When a human writes a test, the human brings different assumptions, different mistakes, and different oversights than the person who wrote the code. That mismatch is what makes testing useful. When the same AI model writes the code and evaluates it, that mismatch shrinks.

This is Russell’s alignment problem. The agents are not trying to satisfy users. They are trying to score well on a test that is supposed to represent user satisfaction. Those are different things. A clever enough agent will find ways to ace the test without actually doing what users need. The "return true" episode was a crude version. Subtler versions will be harder to catch.

**The Digital Twin Universe and the Economics of Impossible Things**

The most creative element of StrongDM’s approach is what they call the Digital Twin Universe. They built working replicas of Okta, Jira, Slack, Google Docs, Google Drive, and Google Sheets, mimicking their interfaces, edge cases, and behaviors. Against these replicas, they run thousands of test scenarios per hour. No rate limits. No API costs. No risk of breaking real services.

McCarthy frames this as an economic inversion, and the evidence supports him. Building a faithful replica of a major SaaS product was always technically possible. It was never worth the cost. Engineers did not even propose it because they already knew the answer. Then the cost of writing software collapsed. What was unthinkable six months ago is now routine.

This is Kurzweil’s exponential logic again, applied to economics rather than capability. When a technology crosses a cost threshold, investments that were irrational yesterday become obvious today, and the unlocked capabilities cascade. The Digital Twin Universe is not just a testing technique. It is proof that the economics of software have changed in kind, not merely in degree. If you can clone Okta’s API in hours rather than months, the limit on software quality is no longer cost. It is imagination.

But the AILCCP framework’s Accountability principle asks a harder question. When software is "grown" rather than written, when replicas stand in for real services, and when quality is measured by probability rather than certainty, who is responsible for what comes out? The principle requires (among other things) that output be “traceable to an appropriate responsible party” and that there be “zero gap between AI system behavior and deployer’s liability.”

StrongDM’s architecture makes tracing difficult by design. No human reviewed the code that produced a given output. No human wrote the test that validated it. No human built the replica against which it was tested. The humans designed the system that designed the system. Existing legal frameworks assume someone, somewhere, looked at the work. Here, nobody did.

**What Happens to the Engineers?**

StrongDM’s team is three engineers who started in July 2025. By October, when [Simon Willison visited](https://simonwillison.net/2026/Feb/7/software-factory/), they already had working demos of the system that manages their coding agents, their Digital Twin Universe, and their satisfaction testing framework. Three people, three months.

That speed raises a question the AILCCP’s Workforce Compatible principle is designed to surface: does this technology augment human expertise, or does it replace it? StrongDM’s model does not augment software engineering as traditionally understood. It replaces it with something else. The humans in a Software Factory write specifications, design scenarios, and architect systems. They do not program. The skill of reading and writing code, the bedrock of software engineering for seventy years, becomes unnecessary. This is Shapiro’s Level 5, the “Dark Factory,” where the human role shifts entirely from building software to designing and monitoring the systems that build software. The lights are off because nobody needs to see.

The same principle asks a follow-on question: as the old skills fade, does meaningful oversight survive? StrongDM says oversight moves from reviewing code to designing scenarios and monitoring satisfaction. That may prove sufficient. It is also the kind of arrangement where confidence builds gradually, scrutiny fades, and the skills needed to catch a serious failure quietly disappear.

**Regulatory Implications**

So what happens when something goes wrong? Regulation in software has always been reactive. It responds to harm after the fact. The AILCCP framework cannot change that, but it can identify where the gaps are before they produce failures. Three stand out: nobody knows who is liable, nobody knows what to disclose, and the contracts have not caught up.

Accountability in software has historically (and to this day) worked through product liability, professional licensing, and contractual warranties. None of these contemplate software that no human has reviewed. The FTC’s enforcement actions have focused on deceptive marketing and consumer protection. But a Software Factory producing security infrastructure raises different questions entirely. If an access management system fails because an agent-written module contained a subtle error that no human ever saw, who is liable? The three engineers who designed the architecture? The AI provider whose model generated the code? The company that sold the product?

The liability question is hard enough. The disclosure question may be worse. When a customer asks “how was this software built?” the truthful answer is: “Coding agents wrote it. Other agents tested it against replicas of your services. Satisfaction scores exceeded our threshold.” Most procurement officers, auditors, and regulators have no way to evaluate that answer. But the problem runs deeper than unfamiliarity. Even if they understood, they would have no framework for deciding whether the answer is acceptable. No industry standard defines what a sufficient satisfaction score looks like. No audit methodology covers agent-built software tested against replicas. No procurement checklist asks whether the vendor’s coding agents share blind spots with the vendor’s testing agents. The disclosure is technically accurate and practically useless, not because the listener is unsophisticated, but because the tools for making sense of it do not exist yet.

And here is the quiet (or loud) absurdity that deserves attention. Open the terms of service for any AI-built product shipping today. Read the galactic warranty disclaimers, the limitation-of-liability clauses, the “AS IS” language. You will find them virtually identical to the terms that have accompanied software for decades. The same boilerplate that disclaimed liability when dozens of engineers wrote and reviewed every line now disclaims liability when no human has looked at the code at all. The contractual wrapper has not changed while the thing inside the wrapper has. A limitation-of-liability clause drafted for software built by humans, tested by humans, and reviewed by humans is now quietly absorbing the risk of software that was none of those things. Nobody updated the contract because the contract was never designed to describe how the software was made. It was designed to limit-or more accurately-extinguish what happens when the software breaks. And so the same language that once disclaimed imperfection in a human process now disclaims the absence of a human process entirely.

That gap between what the product is and what the contract says creates a credibility problem the AILCCP’s Trustworthy principle identifies directly: blanket disclaimers that contradict a vendor’s own trust claims destroy the trust they are trying to build. Try telling an enterprise customer that your software was never reviewed by a human. Then hand them the same limitation-of-liability clause their vendor used in 1996.

But perhaps this is transitional. The Software Factory represents such a thorough departure from conventional development that it might eventually produce an entirely new contractual form. A vendor confident enough to eliminate human code review might also be confident enough to offer terms that reflect what the product actually is: a warranty tied not to human inspection but to satisfaction scores, scenario coverage, or Digital Twin fidelity, with disclosures covering the agent architecture, the testing methodology, and the threshold at which the vendor considers the software fit for use. Nobody has done this yet, and the reasons are structural. Insurance underwriters price risk based on categories they understand, and “software produced without human review, tested by AI against simulated services” does not appear in any underwriting model. Investors would read novel warranty terms as voluntary assumption of liability. The legacy boilerplate persists because it limits exposure, satisfies insurers, and avoids alarming the board, not because it accurately describes the product.

The liability gap, the disclosure gap, and the contractual gap all point to the same underlying problem. Stuart Russell’s AI alignment asks a deceptively simple question: when we build systems that optimize for the objectives we give them, have we preserved the ability to step in and correct course when those objectives turn out to be wrong? For the Software Factory, the answer is not yet and probably never. No regulatory framework addresses this mode of production at all. And the exponential adoption curve means the window for getting ahead of it is narrow. If StrongDM’s approach spreads at the rate current trends suggest, Software Factories could be producing a significant share of commercial software within two years.

The Software Factory’s greatest risk is not that agent-written code will be worse than human-written code. It may very well be better. The risk is that when it fails, nobody will know why. Nobody will know how to fix it. And the institutional knowledge required to understand the failure will have atrophied, because the humans stopped reading code years ago.

**Category:**

  * Uncategorized



**Tags:**

  * [AI governance](https://law.stanford.edu/blog/?tax_and_terms=9779&page=1), 
  * [AI risk](https://law.stanford.edu/blog/?tax_and_terms=9871&page=1), 
  * [artificial intelligence](https://law.stanford.edu/blog/?tax_and_terms=4816&page=1), 
  * [Eran Kahana](https://law.stanford.edu/blog/?tax_and_terms=4835&page=1), 
  * [StrongDM](https://law.stanford.edu/blog/?tax_and_terms=9870&page=1)



  * [ Subscribe ](/blog-subscription/)
  * [__Share on Twitter](https://twitter.com/share?url=https%3A%2F%2Flaw.stanford.edu%2F2026%2F02%2F08%2Fbuilt-by-agents-tested-by-agents-trusted-by-whom%2F&via=StanfordLaw&text=I'm reading: Built by Agents, Tested by Agents, Trusted by Whom? at  "Share on Twitter")
  * [__Share on Facebook](https://www.facebook.com/sharer/sharer.php?s=100&p\[title\]=Built+by+Agents%2C+Tested+by+Agents%2C+Trusted+by+Whom%3F&p\[url\]=https%3A%2F%2Flaw.stanford.edu%2F2026%2F02%2F08%2Fbuilt-by-agents-tested-by-agents-trusted-by-whom%2F&p\[images\]\[0\]=&p\[summary\]=On+February+6%2C+2026%2C+StrongDM%E2%80%99s+AI+team+published+a+manifesto.+Three+engineers+described+a+%E2%80%9CSoftware+Factory%E2%80%9D+where+coding+agents+write%2C+test%2C+and+ship+production+software.+No+human+writes+code.+No+human+reviews+code.+The+humans+design+specifications%2C+curate+test+scenarios%2C+and+watch+the+scores.+The+agents+do+everything+else.+This+is+not+a+research+prototype.+StrongDM+builds+access+management+and+security+software.+Pause+on+that.+A+team+building+security+infrastructure+has+decided+that+human+code+review+is+an+obstacle%2C+not+a+safeguard.+They+are+not+alone.+Dan+Shapiro%E2%80%99s+five-level+taxonomy+of+AI-assisted+programming%2C+published+weeks+earlier%2C+places+this+approach+at... "Share on Facebook")



Post Pagination

  * [ Previous Article From Logging to Transparency: Locating AI Agent Controls in the AI Life Cycle Core Principles Framework ](https://law.stanford.edu/2026/01/31/from-logging-to-hitl-locating-agent-controls-in-the-ai-life-cycle-core-principles-framework/)
  * [ Next Article Context Stewardship: What Source-by-Source Authorization Misses ](https://law.stanford.edu/2026/02/11/context-stewardship-what-source-by-source-authorization-misses/)



[ ](https://law.stanford.edu)

Crown Quadrangle  
559 Nathan Abbott Way  
Stanford, CA 94305-8610

  * **Phone:** 650.723.2465
  * **Fax:** 650.725.0253


  * [ __ Follow Us on X ](https://x.com/stanfordlaw "Follow us on X")
  * [ __ Follow Us on Facebook ](https://www.facebook.com/StanfordLawSchool "Follow us on Facebook")
  * [ __ Follow Us on YouTube ](https://www.youtube.com/user/stanfordlawschool "Follow us on YouTube")
  * [ __ Follow Us on Instagram ](https://instagram.com/stanfordlawschool/ "Follow us on Instagram")
  * [ __ Follow Us on LinkedIn ](https://www.linkedin.com/company/stanford-law-school "Follow us on LinkedIn")
  * [ __ Subscribe to our RSS feeds ](https://law.stanford.edu/rss-feeds/ "Subscribe to our RSS feeds")



Secondary Navigation

I am ...

  1. [Future Student](https://law.stanford.edu/i-am-a-future-student/)
  2. [Current Student](https://law.stanford.edu/i-am-a-current-student/)
  3. [I am a Staff Member](https://law.stanford.edu/i-am-a-staff-member/)
  4. [I am a Faculty Member](https://law.stanford.edu/i-am-a-faculty-member/)
  5. [Alum](https://law.stanford.edu/i-am-an-alum/)
  6. [Employer](https://law.stanford.edu/i-am-an-employer/)
  7. [Journalist](https://law.stanford.edu/i-am-a-journalist/)



About

  1. [About SLS](https://law.stanford.edu/about/)
  2. [ABA-Required Disclosures](https://law.stanford.edu/aba-required-disclosures/)
  3. [Visiting Campus](https://law.stanford.edu/visiting-campus/)
  4. [Web Accessibility](https://www.stanford.edu/site/accessibility)
  5. [Website Feedback](https://law.stanford.edu/website-feedback/)
  6. [Giving at SLS](https://law.stanford.edu/giving/)



Education

  1. [Degrees](https://law.stanford.edu/education/degrees/)
  2. [Courses](https://law.stanford.edu/education/courses/)
  3. [JD Graduation Information](https://law.stanford.edu/education/jd-graduation-information/)
  4. [Executive Education](https://law.stanford.edu/executive-education/)



Research

  1. [Faculty Research](https://law.stanford.edu/research/faculty-research/)
  2. [Robert Crown Law Library](https://law.stanford.edu/robert-crown-law-library/)
  3. [Publications](/publications/)
  4. [Student Journals](/organizations/?page=1&tax_and_terms=311)



Community

  1. [Student Life](https://law.stanford.edu/community/student-life/)
  2. [Events](/events)
  3. [Faculty Directory](/directory/?tax_and_terms=1067&page=1)
  4. [Organizations](/organizations/)



Careers

  1. [Legal Careers](https://law.stanford.edu/careers/career-possibilities/)
  2. [Jobs at SLS](https://law.stanford.edu/office-of-human-resources/job-announcements/)



News & Media

  1. [News Center](https://law.stanford.edu/media/)
  2. [Media Coverage](/press)
  3. [SLS Blogs](/blog/)
  4. [Stanford Lawyer Magazine](https://law.stanford.edu/stanford-lawyer-magazine/)
  5. [Video Center](https://law.stanford.edu/media/video-center/)
  6. [Social Media Hub](https://law.stanford.edu/social-media/)
  7. [SLS Newsletters](https://law.stanford.edu/media/sls-newsletters/)



[ ](https://www.stanford.edu)

Stanford University Navigation

  1. [Stanford Home](https://www.stanford.edu)
  2. [Maps & Directions](https://visit.stanford.edu/plan/)
  3. [Search Stanford](https://www.stanford.edu/search/)
  4. [Emergency Info](https://emergency.stanford.edu)



Legal Navigation

  1. [Terms of Use](https://www.stanford.edu/site/terms/)
  2. [Privacy](https://www.stanford.edu/site/privacy/)
  3. [Copyright](https://uit.stanford.edu/security/copyright-infringement)
  4. [Trademarks](https://adminguide.stanford.edu/chapter-1/subchapter-5/policy-1-5-4)
  5. [Non-Discrimination](https://exploredegrees.stanford.edu/nonacademicregulations/nondiscrimination/)
  6. [Accessibility](https://www.stanford.edu/site/accessibility)



(C) Stanford University,  Stanford, California 94305. 

__Back to the Top

(C) Stanford University, Stanford, California, 94305-8610 | https://law.stanford.edu/2026/02/08/built-by-agents-tested-by-agents-trusted-by-whom/ 
  *[CA]: California
