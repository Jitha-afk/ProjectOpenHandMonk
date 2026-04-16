# Structured notes from user-provided transcript

## 00:06-01:41 — Intro, Haley intro, talk scope, and what the session will cover

Summary:
- Key thematic segment from the talk.

Transcript excerpt:
- 0:06 So with that, let's get started. Um, we
- 0:09 have two fantastic talks today. Our
- 0:11 first talk is uh from Haley Quash. You
- 0:15 know, Haley and I connected uh online
- 0:18 because I read her paper. She uh she
- 0:20 works at IBM research and did an amazing
- 0:22 paper, probably the best I've seen on
- 0:24 MCP security. And she really got into
- 0:26 the details of the different types of
- 0:27 risk. It was very well thought out and I
- 0:30 invited her to come and present and talk
- 0:32 because I was so impressed with her
- 0:34 paper. So I'm really looking forward to
- 0:35 Haley's talk.
- 0:37 Yeah, thank you for having me. Um, so
- 0:39 yeah, so like Shannon was mentioning, I
- 0:42 wrote like a blog post like on MCP
- 0:45 security and basically today's talk is
- 0:48 gonna cover the blog post as well as
- 0:52 like some extra things that um I came up
- ... (19 more timestamped lines in this segment)

## 01:41-04:20 — MCP recap, why adoption is exploding, and why convenience makes mistakes costly

Summary:
- Highlights the MCP Inspector-style incident: endpoint bound to 0.0.0.0, no authentication, remote code execution risk.

Transcript excerpt:
- 1:41 So let's start with um a quick recap of
- 1:44 what MCP is. So if you watch the context
- 1:47 streams or if you're already familiar
- 1:49 with uh developing MCB servers um I I
- 1:54 just want to give you like why it
- 1:56 matters and what it is. Um so a quick
- 1:58 history lesson is we started with uh a
- 2:01 single LM. Uh so these are big reasoning
- 2:04 engines but they are stuck with their
- 2:06 training data and no way to call out
- 2:08 life tools and then uh we go to the next
- 2:12 step which is tool biting. Uh you can
- 2:14 think of name change where you attach
- 2:16 tool directly to an agent. Um however
- 2:19 the hard part here is application
- 2:21 integrations into like ids, chat apps
- 2:25 and other UIs. Each of them needs like
- 2:27 custom connector for every tool. Uh
- 2:30 which becomes like a brittle tangle of
- 2:32 pointto-point integration and this where
- ... (36 more timestamped lines in this segment)

## 04:25-06:23 — Confused deputy / authorization context problem and OAuth-spec gaps

Summary:
- Key thematic segment from the talk.

Transcript excerpt:
- 4:25 Um and then here I'm just I just want to
- 4:28 give you like a big overview and summary
- 4:31 of all the common MCB security pitfalls.
- 4:34 Um I'm sure that like you have heard a a
- 4:37 [clears throat] lot of other speakers
- 4:38 mention these but I want to give you
- 4:40 like a quick recap of everything I have
- 4:43 like um came across so far. So one
- 4:48 fundamental challenge um is ensuring
- 4:51 that MCB facilitated actions occur with
- 4:55 proper authorization and context. um
- 4:57 when an MCP server performs an action on
- 5:00 behalf of a user um there is a risk of a
- 5:03 confused deputies scenario. So that's
- 5:06 what is um being illustrated in the
- 5:08 diagram you see on the screen here. Um
- 5:11 in an ideal design the server could
- 5:14 execute uh actions strictly under the
- 5:16 requesting user privileges. Um, however,
- 5:19 in practice, if not implemented
- ... (23 more timestamped lines in this segment)

## 06:26-07:51 — Classic software flaws in MCP servers, especially SQLite reference-server SQL injection

Summary:
- Cites Anthropic reference SQLite MCP server SQL injection and notes that a non-production example was widely forked, extending risk downstream.

Transcript excerpt:
- 6:26 And then beyond conceptual O issues, uh
- 6:29 real world MCP servers have exhibited
- 6:32 like classic software vulnerability as
- 6:34 well. Uh showing that insecure coding
- 6:37 practices carry over into uh this new AI
- 6:41 tool ecosystem as well. So while MCB's
- 6:45 design has conceptual security features,
- 6:48 the actual code behind many tool is
- 6:50 often flawed especially in community or
- 6:53 open-source projects. So a real case is
- 6:57 um as you can see on the screen is from
- 7:00 anthropics reference SQLite NCB server
- 7:04 um which contain a simple SQL injection
- 7:08 bug. The server concatenated user
- 7:10 provided text into an SQL query without
- 7:13 proper sanitation and this flaw although
- 7:16 documented as non-production example
- 7:19 because um anobic has classified it as
- 7:23 um [clears throat] not priority and
- 7:24 archive of the server. Um this server
- ... (9 more timestamped lines in this segment)

## 07:54-09:31 — Prompt injection and indirect injection, including the GitHub MCP issue example

Summary:
- Explains indirect prompt injection through malicious GitHub issues that trick an agent into accessing private repos and exfiltrating information.

Transcript excerpt:
- 7:54 And then prom injection is another very
- 7:57 common uh security pitfall not just for
- 8:00 MCB but in like the broader LM
- 8:03 application development. So injection
- 8:06 refers to malicious or intended
- 8:09 instructions hidden within the input
- 8:12 text that cause the model to deviate
- 8:14 from its intended behavior. Um so one
- 8:19 emerging concern is indirect ejection
- 8:22 via content. Um, attackers can graft
- 8:26 inputs, uh, for example, an email, chat
- 8:29 message or web page, uh, text
- 8:30 [clears throat] that include hidden
- 8:32 directives for the AI. Um, so when the
- 8:35 user's AI assistant processes this
- 8:38 content, the hidden instructions trigger
- 8:40 authorized tool you unauthorized tool
- 8:42 use through the MCB server. So for
- 8:46 example, um, a very prominent case is
- 8:49 the GitHub MCB server attack. As you can
- ... (15 more timestamped lines in this segment)

## 09:36-12:12 — Malicious tools, rug pulls, tool shadowing, tool poisoning, token concentration

Summary:
- Covers malicious-tool patterns: rug pulls, tool shadowing, and tool poisoning in hidden tool descriptions.

Transcript excerpt:
- 9:36 And another pitfall is the presence of
- 9:39 malicious MCB server tools. Um because
- 9:43 MCB allows anyone to develop a server.
- 9:46 an attacker could distribute a tool
- 9:48 plugin that looks useful or benign but
- 9:51 under the hood or in a later update it
- 9:54 performs evil actions. So two uh most
- 9:58 common patterns you should watch out for
- 10:00 are the uh rugpool update. So this is
- 10:03 when you might install a tool that
- 10:06 initially looks safe and it indeed
- 10:08 behaves normally at first but days or
- 10:11 weeks later it auto updates or alter its
- 10:14 behavior to do something malicious. Um
- 10:16 another uh pattern is the tool
- 10:18 shadowing.
- 10:20 So if an AI agent is connected to
- 10:23 multiple MCB servers, a rogue server can
- 10:26 attempt to shadow or hijack calls meant
- 10:29 for an other server's tools. And by
- ... (37 more timestamped lines in this segment)

## 12:16-14:20 — Immediate/P0 best practices

Summary:
- Provides immediate/P0 controls such as stripping user auth headers, validating tokens, disabling public exposure, requiring signed connectors, sanitizing inputs, and validating model outputs.
- Q&A recommends filtering both inputs and outputs, including hidden/special characters and potential leakage in tool output before passing to the next tool or agent.

Transcript excerpt:
- 12:16 So with all of those uh pitfalls in
- 12:18 mind, I want to give you like a summary
- 12:21 of the recommended best practices and
- 12:24 mitigations. Um and note that these are
- 12:28 my own recommendations. It gives you it
- 12:31 tries to give you a reference. You don't
- 12:33 have to follow it to the tea, but I
- 12:35 research and I think these are pretty
- 12:38 good best practices to uh begin with. So
- 12:42 the first set of best practices that you
- 12:45 should do immediately um I categorize it
- 12:48 at P 0 is first don't pass user's token
- 12:51 through uh because if you forward a user
- 12:54 token login to uh if you forward a
- 12:56 user's login token anyone who sees that
- 12:59 token can act as the user. So you should
- 13:01 have the gateway remove the user
- 13:03 authorization header and use a shortlive
- 13:06 credential specifically for the
- 13:07 connector instead. You should also
- ... (27 more timestamped lines in this segment)

## 14:23-16:57 — Near-term, mid-term, and long-term measures

Summary:
- Adds near-term, mid-term, and long-term rollout guidance, including approved-tool catalogs, hardened gateways, centralized traces, automated containment, signed releases, and regular red teaming.

Transcript excerpt:
- 14:23 And then next these are the actions that
- 14:26 you can do near term. So like within
- 14:28 days or weeks you should add quick
- 14:31 safety checks to your deployment
- 14:32 pipeline. add test that check is this
- 14:35 server publicly reachable or does it
- 14:38 accept requests from any other origin or
- 14:40 does it accept tokens with the wrong
- 14:42 audience and limit what each tool can
- 14:45 do. So give each connector exactly the
- 14:48 permission it needs and nothing more.
- 14:51 And you should also sandbox new tools be
- 14:53 before they are trusted. So start new
- 14:56 connectors in an isolated environment
- 14:58 and run a small mock test before making
- 15:00 them safe. And um sorry don't send
- 15:04 secrets to external models. So strip
- 15:07 secrets out before sending anything to
- 15:09 external LM or use your own private
- 15:12 model.
- ... (38 more timestamped lines in this segment)

## 17:00-21:21 — Threat-modeling process, gateway as control plane, and threat-model matrix

Summary:
- Provides a practical threat-modeling process: assets, actors, flows, threats, likelihood/impact, and prioritized mitigations.
- Provides immediate/P0 controls such as stripping user auth headers, validating tokens, disabling public exposure, requiring signed connectors, sanitizing inputs, and validating model outputs.

Transcript excerpt:
- 17:00 And after I give you all those best
- 17:03 practices, I also want to give you
- 17:06 something kind of concrete so you could
- 17:08 apply your knowledge to and due to that
- 17:12 I want to suggest using a threat model
- 17:14 process um so that you can prioritize
- 17:18 your real risk uh doci test that you can
- 17:20 run and a short incident playbook that
- 17:22 you can use immediately.
- 17:25 So in this um thread [clears throat]
- 17:26 model process um you can think of it as
- 17:29 like a repeatable checklist you can use
- 17:31 on any MCB deployment and again this is
- 17:35 my suggestion and recommendation you
- 17:37 don't have to follow them to the tea. Um
- 17:40 but here in this process we should start
- 17:42 with scope and assets. So you start by
- 17:45 naming what you are protecting or
- 17:47 whether they are API tokens tool
- 17:50 connectors user data catalog logs or the
- ... (75 more timestamped lines in this segment)

## 21:27-28:13 — Q&A: practical takeaways, personal-sector risk, provenance, gateway filtering, AI-assisted filtering with human in the loop

Summary:
- Provides immediate/P0 controls such as stripping user auth headers, validating tokens, disabling public exposure, requiring signed connectors, sanitizing inputs, and validating model outputs.
- Q&A emphasizes personal-sector / early-career developer risk: people adopt third-party MCPs too quickly without code review or provenance checks.
- Q&A recommends filtering both inputs and outputs, including hidden/special characters and potential leakage in tool output before passing to the next tool or agent.

Transcript excerpt:
- 21:27 Haley, that was fantastic. Yeah,
- 21:29 enormously comprehensive [clears throat]
- 21:31 a lot of content. Um
- 21:33 what I what I really like is that um you
- 21:37 know it's like there's there's a set of
- 21:39 security issues like you really need to
- 21:41 be aware of what are the security issues
- 21:42 that come with MCP just like with any
- 21:45 technology you know you're developing
- 21:46 web database or anything there's always
- 21:48 some you need to know about the security
- 21:49 things but right now there are some kind
- 21:53 of practical solutions I liked your your
- 21:55 your recommendations that kind of P 0 of
- 21:59 you know that's going to get you pretty
- 22:00 far
- 22:02 you know, until we kind of get even
- 22:04 better at this or, you know, find new
- 22:06 new [laughter] issues. But
- 22:08 but it's kind of like the the um world
- ... (25 more timestamped lines in this segment)
