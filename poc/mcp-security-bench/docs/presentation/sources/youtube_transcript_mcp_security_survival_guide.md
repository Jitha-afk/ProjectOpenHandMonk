# MCP Security Survival Guide: Best Practices, Pitfalls & Real-World Lessons (video transcript)

Source note: user-provided transcript for the YouTube session featuring Haley Quash / Hailey Thao Q. This transcript was supplied manually after automated extraction failed due YouTube IP blocking.

```text
0:06
So with that, let's get started. Um, we
0:09
have two fantastic talks today. Our
0:11
first talk is uh from Haley Quash. You
0:15
know, Haley and I connected uh online
0:18
because I read her paper. She uh she
0:20
works at IBM research and did an amazing
0:22
paper, probably the best I've seen on
0:24
MCP security. And she really got into
0:26
the details of the different types of
0:27
risk. It was very well thought out and I
0:30
invited her to come and present and talk
0:32
because I was so impressed with her
0:34
paper. So I'm really looking forward to
0:35
Haley's talk.
0:37
Yeah, thank you for having me. Um, so
0:39
yeah, so like Shannon was mentioning, I
0:42
wrote like a blog post like on MCP
0:45
security and basically today's talk is
0:48
gonna cover the blog post as well as
0:52
like some extra things that um I came up
0:55
with to make this talk like more
0:58
valuable for you. Uh we're going to go
1:00
over like um the common pitfalls in MCP
1:03
security. um some suggested best
1:06
practices and ways to mitigate these
1:08
pitfalls along with some real world
1:10
lessons like real world incidents and
1:13
what we can learn from them. Um so just
1:16
quickly uh quick introduction about
1:18
myself. My name is Haley. Um I've been
1:20
with IBM for more than a year. I am an
1:23
AI information developer. Um so as an
1:26
aside also rifle towards data science.
1:28
So this is where I publish a lot of
1:30
content on like the new world protocols
1:33
in the AI world like model context
1:35
protocols and agent agent to agent
1:38
protocol.
1:41
So let's start with um a quick recap of
1:44
what MCP is. So if you watch the context
1:47
streams or if you're already familiar
1:49
with uh developing MCB servers um I I
1:54
just want to give you like why it
1:56
matters and what it is. Um so a quick
1:58
history lesson is we started with uh a
2:01
single LM. Uh so these are big reasoning
2:04
engines but they are stuck with their
2:06
training data and no way to call out
2:08
life tools and then uh we go to the next
2:12
step which is tool biting. Uh you can
2:14
think of name change where you attach
2:16
tool directly to an agent. Um however
2:19
the hard part here is application
2:21
integrations into like ids, chat apps
2:25
and other UIs. Each of them needs like
2:27
custom connector for every tool. Uh
2:30
which becomes like a brittle tangle of
2:32
pointto-point integration and this where
2:35
MCP comes in. It solves that by adding a
2:39
standard centralized layer. So we have
2:41
the model is the LOM and the context is
2:44
the extra data the model needs and the
2:47
protocol is the common language that
2:49
lets like apps and tools talks uh to
2:52
each other predictably.
2:55
And if you have watched um the talks
2:58
from the MCP developer summit um you
3:02
understand that like adoption of MCP is
3:05
really fast and it's like exploding
3:07
because MCBA is the blooming that lets
3:10
agents go tools and data sources is
3:12
elegant and is convenient. However,
3:15
because uh that convenient is also what
3:18
makes mistakes very costly. Um in my
3:22
blog uh my paper I already uh
3:26
noted like different realware incidents
3:29
such as like um the MCB inspector this
3:33
from anthropic um where the tool endp
3:37
points was left reachable from the
3:39
network it was bound to 0.0.0.0
3:43
and it had no authentication at all. So
3:45
when an attacker send request to the
3:47
endpoint which cause the server to
3:50
execute commands on the host there's
3:52
like full remote code execution and um
3:57
has already fixed um that fix up this uh
4:00
security threat but there are other
4:03
patterns that um are still happening
4:06
nowadays like token leaks in plugins and
4:09
injections directly in the tool um and
4:12
this why MCP Security is becoming more
4:16
and more important. It is not just an
4:18
afterthought for developers who are
4:20
developing SB server anymore.
4:25
Um and then here I'm just I just want to
4:28
give you like a big overview and summary
4:31
of all the common MCB security pitfalls.
4:34
Um I'm sure that like you have heard a a
4:37
[clears throat] lot of other speakers
4:38
mention these but I want to give you
4:40
like a quick recap of everything I have
4:43
like um came across so far. So one
4:48
fundamental challenge um is ensuring
4:51
that MCB facilitated actions occur with
4:55
proper authorization and context. um
4:57
when an MCP server performs an action on
5:00
behalf of a user um there is a risk of a
5:03
confused deputies scenario. So that's
5:06
what is um being illustrated in the
5:08
diagram you see on the screen here. Um
5:11
in an ideal design the server could
5:14
execute uh actions strictly under the
5:16
requesting user privileges. Um, however,
5:19
in practice, if not implemented
5:21
correctly, an AI agent could
5:23
unintentionally use the server's own
5:26
elevated privileges or store credentials
5:29
to access resources that the human user
5:32
shouldn't have access to. Um, so
5:35
currently MCB authorization model is
5:37
built upon OOTH for delegating access
5:41
tokens. Um, but early versions of the
5:44
spec had gaps that clash with enterprise
5:46
security practices. Um, for example,
5:49
static oath client ids and implicit
5:52
trust in constant cookies could allow
5:54
token reuse attacks if a server didn't
5:58
explicitly enforce per user. Um, and
6:02
efforts are underway to update the MCB
6:04
specification to u better align with
6:08
secure patterns. Um, for example, like
6:10
enforcing dynamic line res
6:12
registrations. Um but if you have
6:15
watched the talk from Paul Carton from
6:17
Anthropic on why MCB O is hard, you
6:21
should see that these efforts are not
6:23
easy to implement.
6:26
And then beyond conceptual O issues, uh
6:29
real world MCP servers have exhibited
6:32
like classic software vulnerability as
6:34
well. Uh showing that insecure coding
6:37
practices carry over into uh this new AI
6:41
tool ecosystem as well. So while MCB's
6:45
design has conceptual security features,
6:48
the actual code behind many tool is
6:50
often flawed especially in community or
6:53
open-source projects. So a real case is
6:57
um as you can see on the screen is from
7:00
anthropics reference SQLite NCB server
7:04
um which contain a simple SQL injection
7:08
bug. The server concatenated user
7:10
provided text into an SQL query without
7:13
proper sanitation and this flaw although
7:16
documented as non-production example
7:19
because um anobic has classified it as
7:23
um [clears throat] not priority and
7:24
archive of the server. Um this server
7:28
was widely copied. It was forked over
7:31
5,000 times by developers building their
7:34
own agents. Consequently, the book
7:37
continues to live on in derived
7:39
projects, creating exploit path where an
7:42
attacker can embed SQL comments via an
7:45
AI's input um potentially altering store
7:48
data or injecting malicious ROMs into
7:51
the agent's context.
7:54
And then prom injection is another very
7:57
common uh security pitfall not just for
8:00
MCB but in like the broader LM
8:03
application development. So injection
8:06
refers to malicious or intended
8:09
instructions hidden within the input
8:12
text that cause the model to deviate
8:14
from its intended behavior. Um so one
8:19
emerging concern is indirect ejection
8:22
via content. Um, attackers can graft
8:26
inputs, uh, for example, an email, chat
8:29
message or web page, uh, text
8:30
[clears throat] that include hidden
8:32
directives for the AI. Um, so when the
8:35
user's AI assistant processes this
8:38
content, the hidden instructions trigger
8:40
authorized tool you unauthorized tool
8:42
use through the MCB server. So for
8:46
example, um, a very prominent case is
8:49
the GitHub MCB server attack. As you can
8:51
see at the screen where the attacker
8:54
creates malicious um MCB issue in any
8:57
public repository the victim might
9:00
interact with. And on this in the issue
9:02
you can see that the act attacker is
9:04
asking the um AI agent to read the
9:08
readme of all rebels um no matter if
9:11
they are private or public and gather
9:14
the private information from the author
9:16
and send it back to the attacker. So in
9:20
this way hidden commands redirect the AI
9:23
to access the private repository using
9:26
the GitHub token and then sensitive data
9:29
gets excited through the AI's response
9:31
this guy as a helpful analysis.
9:36
And another pitfall is the presence of
9:39
malicious MCB server tools. Um because
9:43
MCB allows anyone to develop a server.
9:46
an attacker could distribute a tool
9:48
plugin that looks useful or benign but
9:51
under the hood or in a later update it
9:54
performs evil actions. So two uh most
9:58
common patterns you should watch out for
10:00
are the uh rugpool update. So this is
10:03
when you might install a tool that
10:06
initially looks safe and it indeed
10:08
behaves normally at first but days or
10:11
weeks later it auto updates or alter its
10:14
behavior to do something malicious. Um
10:16
another uh pattern is the tool
10:18
shadowing.
10:20
So if an AI agent is connected to
10:23
multiple MCB servers, a rogue server can
10:26
attempt to shadow or hijack calls meant
10:29
for an other server's tools. And by
10:32
intercepting or impersonating the
10:34
trusted tools functionality, the
10:36
malicious server can perform actions
10:38
under the guise of the legitimate one.
10:42
And then a particularly novel MCP
10:46
specific vulnerability is tool
10:48
poisoning. Um this was brought up by a
10:51
research uh by invariant lab. So this is
10:54
a form of brum injection that originates
10:57
inside the tool itself. So these
11:00
descriptions are provided to the LM so
11:03
it knows what the tool does and how to
11:05
use it but are typically not shown to
11:08
the end user. So an attacker can exploit
11:11
it by uh inserting instructions that
11:14
only the LLM will see effectively
11:18
poisoning the context that the AI uses
11:20
to decide how to call the tool. So in
11:24
one case and this is from um the
11:26
research by the invariant lab as well.
11:28
The tools dock string includes a hidden
11:31
important section as you can see on the
11:33
screen um that instructs the AI
11:35
assistant to quietly read a private file
11:39
and supply it back to the attacker as a
11:41
secret parameter sign whenever the ad
11:44
function is called.
11:47
And then last but not least, uh MCP
11:49
servers often needs um access to user
11:53
accounts and data which means tokens and
11:55
credentials are concentrated in one
11:58
place. So this creates significant risk
12:01
uh if those credentials are compromised.
12:03
So two major scenarios of concern are
12:06
oath token theft and account takeover
12:09
and also over broad uh permissions and
12:12
data aggregation.
12:16
So with all of those uh pitfalls in
12:18
mind, I want to give you like a summary
12:21
of the recommended best practices and
12:24
mitigations. Um and note that these are
12:28
my own recommendations. It gives you it
12:31
tries to give you a reference. You don't
12:33
have to follow it to the tea, but I
12:35
research and I think these are pretty
12:38
good best practices to uh begin with. So
12:42
the first set of best practices that you
12:45
should do immediately um I categorize it
12:48
at P 0 is first don't pass user's token
12:51
through uh because if you forward a user
12:54
token login to uh if you forward a
12:56
user's login token anyone who sees that
12:59
token can act as the user. So you should
13:01
have the gateway remove the user
13:03
authorization header and use a shortlive
13:06
credential specifically for the
13:07
connector instead. You should also
13:10
always check tokens on the server. So
13:12
make the server check the tokens
13:14
audience issuer and expiry every time.
13:17
Uh you should stop services from
13:19
listening to the whole internet.
13:21
Basically don't do what MCB inspector
13:25
was doing before. Uh you should require
13:28
sign connector code and stop auto
13:30
updates. So only install connector bills
13:32
that are cryptographically signed and
13:35
turn off automatic updates in
13:37
production. Um and then make destructive
13:40
actions require a human input. So if an
13:43
action would delete or change data, show
13:46
it to a person for approval before
13:48
running it. And then you should also
13:51
sanitize inputs, right? So strip control
13:54
characters, normalize white spaces,
13:56
remove code fences, and run simple
13:59
validation tools on any user or store
14:02
text before it's used in a prompt. And
14:05
lastly, validate the model outputs
14:07
before executing tools. So again do
14:10
sanity check for generated tool calls.
14:13
Um and then have a allow list block or
14:17
require review for anything outside
14:20
those um allowed list or white list.
14:23
And then next these are the actions that
14:26
you can do near term. So like within
14:28
days or weeks you should add quick
14:31
safety checks to your deployment
14:32
pipeline. add test that check is this
14:35
server publicly reachable or does it
14:38
accept requests from any other origin or
14:40
does it accept tokens with the wrong
14:42
audience and limit what each tool can
14:45
do. So give each connector exactly the
14:48
permission it needs and nothing more.
14:51
And you should also sandbox new tools be
14:53
before they are trusted. So start new
14:56
connectors in an isolated environment
14:58
and run a small mock test before making
15:00
them safe. And um sorry don't send
15:04
secrets to external models. So strip
15:07
secrets out before sending anything to
15:09
external LM or use your own private
15:12
model.
15:14
And then in the midterm uh you should
15:17
create a catalog of approved tools. So
15:19
keep a registry where every entry is
15:22
review and signed and harden the gateway
15:25
if your organizations are using MCB
15:28
gateways or LM gateways. Um so you
15:31
should harden these because now they
15:33
become like high value target for these
15:36
attacks and centralize your logs and
15:38
traces. So always propagate a trace ID
15:42
and keep an immutable copy of logs for
15:45
investigations
15:46
and if possible automate containment
15:48
steps. So have scripts or playbooks that
15:51
isolate a server, rotate keys and revoke
15:54
sessions automatically when triggered.
15:57
And then in the long terms they can
16:00
become these can become like your
16:02
company policy something that you
16:04
require everybody to follow. So you can
16:07
uh require uh side releases and review
16:10
workflows. So use protected branches
16:13
side releases and multi-person approvals
16:16
for big changes. And if you are using
16:20
LLM as a helper for your gateways, I
16:23
would suggest that uh keep them as
16:25
helpers, not the final decision makers
16:28
um because there's always a risk of them
16:31
hallucinating. So keep blocking rules
16:34
deterministic and require human approval
16:37
for Bzero items. And then keep
16:39
dependency list and scan them regularly.
16:42
Um so maintain this this list and fail
16:46
bills if unexpected transitive
16:48
dependency appears. And lastly uh run
16:52
regular red teams and audits. So
16:54
schedule hardly test and get a lot
16:57
rejects.
17:00
And after I give you all those best
17:03
practices, I also want to give you
17:06
something kind of concrete so you could
17:08
apply your knowledge to and due to that
17:12
I want to suggest using a threat model
17:14
process um so that you can prioritize
17:18
your real risk uh doci test that you can
17:20
run and a short incident playbook that
17:22
you can use immediately.
17:25
So in this um thread [clears throat]
17:26
model process um you can think of it as
17:29
like a repeatable checklist you can use
17:31
on any MCB deployment and again this is
17:35
my suggestion and recommendation you
17:37
don't have to follow them to the tea. Um
17:40
but here in this process we should start
17:42
with scope and assets. So you start by
17:45
naming what you are protecting or
17:47
whether they are API tokens tool
17:50
connectors user data catalog logs or the
17:53
gateways themselves. So be explicit. Say
17:56
where sickers live and which components
17:59
hold privileged assets. And then after
18:01
that you should identify the actors who
18:04
can touch the these assets. Um are they
18:08
external attackers, compromised third
18:10
party tools, gateway admins, insiders
18:14
and even the LMS or tool maintainers. So
18:17
naming these actors will help you write
18:19
concrete abuse stories. And then the
18:22
next step is to map attack surfaces and
18:24
flows. So draw the flows from the client
18:27
to the gateway to the server to external
18:30
service. And then in the flow mark the
18:34
choice boundaries. Um it could be off
18:36
runtime sandbox catalog. This is where
18:39
we visually find weak links and then you
18:43
enumerate the threats and the attack
18:45
vectors. So for each flow write down how
18:48
it can be abused either it's token theft
18:51
from injection uh connector exfiltration
18:55
etc. Keep it practical so that you can
18:58
prioritize the ones that can that can
19:00
actually hurt you and then you assess
19:02
the likelihood and impact of each of
19:05
these threats. So score each thread by
19:07
how likely it is and how bad the fallout
19:10
could be so that the teams don't waste
19:12
time on low impact stuff. And lastly,
19:15
you should have a plan to mitigate and
19:18
prioritize. So, pick one or two high
19:20
lever controls for PZ items um and turn
19:24
those into CI test runbooks uh and
19:28
scripts that you can run. And again, if
19:31
your company is using gateways, then
19:34
treat these as service that you would
19:37
protect with the highest standards.
19:42
Um and again so I'm just showing like
19:45
the idea of having gateway as the
19:47
control plane. Again I know that OBD uh
19:50
and like a lot of other organizations
19:52
are beginning to adopt MCB gateways and
19:55
LM gateways. So again since these are
19:58
the natural control plane for MCB
20:00
adoption now um you have to really
20:04
defend them um as your highest uh
20:07
priority items.
20:09
And lastly, I just want to leave you
20:11
with an example of how you can design a
20:14
thread model matrix based on the thread
20:16
model process that I was showing you
20:19
before. Um, so this is an example where
20:22
you can have like different columns for
20:24
the thread ID, the attacker goal, it
20:27
impact, the likelihood, the priority and
20:30
then um you can draw out like the flow
20:33
for each scenario. So for example, the
20:36
first row is for token theft. uh token
20:39
theft is one of the most actionable
20:40
risk. So if an attackers get tokens they
20:43
can impersonally use agents. So you can
20:46
you should make token shortlived
20:48
validity audience claims and avoid
20:50
accepting better tokens forward it from
20:53
addressed clients. Um and then since I
20:57
mentioned a lot about the gateways I
20:59
also want to include an appendix on how
21:02
you can treat um [clears throat] attack
21:04
threats towards your gateways. So
21:07
whether is your uh MCB gateway, your LLM
21:10
gateway or your web hook, you should
21:13
also keep in mind like some kind of
21:16
procedures that you can do uh in case
21:19
these are compromised
21:21
and I think that's time for me and thank
21:24
you so much for listening.
21:27
Haley, that was fantastic. Yeah,
21:29
enormously comprehensive [clears throat]
21:31
a lot of content. Um
21:33
what I what I really like is that um you
21:37
know it's like there's there's a set of
21:39
security issues like you really need to
21:41
be aware of what are the security issues
21:42
that come with MCP just like with any
21:45
technology you know you're developing
21:46
web database or anything there's always
21:48
some you need to know about the security
21:49
things but right now there are some kind
21:53
of practical solutions I liked your your
21:55
your recommendations that kind of P 0 of
21:59
you know that's going to get you pretty
22:00
far
22:02
you know, until we kind of get even
22:04
better at this or, you know, find new
22:06
new [laughter] issues. But
22:08
but it's kind of like the the um world
22:11
is not on fire, you know, it's like a
22:14
new technology, new technology brings
22:15
new security things we have to consider,
22:17
but then, you know, we're figuring out
22:19
kind of practical ways to deal with it.
22:23
Yeah. because like um I'm surrounded by
22:26
a lot of interns at IBM and when MCB
22:29
came out they are very excited to adopt
22:31
them without really like thinking about
22:33
the securityities um threats that could
22:36
happen. So if they see like a third
22:38
party MCB server, they're just very
22:40
excited to adopt it right away into
22:42
enterprise like programs and
22:44
applications. And like I started reading
22:46
about these like real world incidents
22:48
and I'm like, "Oh, you guys should stop
22:49
and kind of read the code and try to
22:52
like kind of filter it out first before
22:55
you use them." And also um a lot of the
22:59
talks and tutorials I read even though
23:01
they list out the mitigation and best
23:03
practices I feel like they are very
23:06
abstract still like we have
23:09
companies that are building tools like
23:11|uh MCB gateways to help us like manage
23:14|this like sessions and
23:15|authentication but like if your company
23:19|want to do this yourself how can you
23:21|start so that's why I thought giving
23:24|people an idea of making the threat
23:26|model matrix could be a good start. Um
23:30|Haley because I think in a lot of ways
23:32|um I actually think most companies that
23:35|I'm talking to are somewhat aware of the
23:37|potential risk of MCP. Like just you
23:39|know especially the bigger the company
23:40|is the more likely they've already kind
23:43|of they've already set some guidelines
23:45|or they're at least trying to tell
23:47|people like hey whoa hold on be you know
23:50|think about what we're doing here. where
23:52|I think there's actually people getting
23:54|killed right now is is in the personal
23:57|sector. I think your your personal
23:58|sector of
23:59|sort of early career developers who
24:02|haven't lived through,
24:04|you know, all of the security challenges
24:06|of of web development or cloud native or
24:09|anything. I think those people are, you
24:12|know, they're finding cool MCPs that do
24:14|cool things that add value to their
24:16|daily to their vibe coding. Especially,
24:19|you know, I think a lot of times of
24:20|people who are
24:21|maybe not even um you maybe not even
24:24|highly trained developers but now vibe
24:26|coding they're finding MCPs that can add
24:28|value to that so they're attaching it
24:30|and those MCPs are stealing their tokens
24:32|stealing their data stealing
24:35|I I really hope people who are working
24:37|on their own are looking at this um and
24:40|really looking at
24:42|you know looking for MCPs you know when
24:44|you imply when you deploy an MCP you
24:46|better know what it does and you better
24:47|have looked at it you better be
24:49|confident that it's um it's something
24:51|that you want and definitely think about
24:54|the provenence of it like where did this
24:55|come from who created this and almost in
24:58|the way I would say if you don't uh if
25:00|you don't have a very strong feeling
25:02|that that MCP came from a very trusted
25:04|brand you know you better be reviewing
25:06|the code of it and you better be looking
25:07|at it in in very close detail um but
25:11|I liked oh I do have a question in there
25:13|I I do think the um you mentioned the
25:16|gateways and I obviously that's
25:17|something we spend a lot of time working
25:18|with people on is gateway development,
25:20|but there's a there's sort of a function
25:22|in gateways to to do filtering to do
25:25|some type of a, you know, kind of
25:27|inbound outbound filters to look for
25:30|either bad inputs or bad outputs coming
25:32|from MCPS.
25:34|What are some of the key like if you
25:36|were you know going to say like here are
25:37|two things you should be filtering on
25:40|that everybody should be filtering on?
25:42|Um what are the kind of things that that
25:44|you would like oh cool I have this I now
25:46|can write a filter I can and and these
25:48|filters can be quite powerful. I think
25:50|they can even be AI powered if we if you
25:53|want to make them that way. But like
25:55|what are the filters you would be
25:56|recommending to someone to prioritize as
25:59|like this is what we should be filtering
26:01|out or ensuring is there.
26:04|M um so like I mentioned before so uh
26:08|for the input like you should try to
26:12|um sanitize it in the way that you
26:15|usually like sanitize any kind of input
26:17|in other coding practices like uh strip
26:21|like white space special characters um
26:25|if there's like hidden characters or
26:27|special characters you should sanitize
26:30|those as well and then for the outputs
26:33|like in the SQ fewer injection attacks.
26:36|Um this is because the outpost from the
26:38|tool was like passed directly to the
26:40|next tool or the agent. So we have to
26:43|also validate this outpost to make sure
26:45|that like it's not containing any kind
26:47|of private data uh any information um
26:51|that could be passed on like potentially
26:53|to external services and I understand
26:56|that I was looking into how a lot of
26:59|company builds their MCB gateway as well
27:01|and unfortunately like a lot of them I
27:04|don't really have the um actual uh
27:07|implementations but I understand that
27:09|like if you want to scale it for a big
27:11|organization then an LOM or AI could
27:15|really be useful in helping you triage
27:18|all these. Um so like you could have
27:21|like instructions for the LOM, you could
27:23|have it in its prompt uh and then you
27:25|can have like block blocking rules or
27:28|like uh anything that help you like make
27:31|your work faster. But I would suggest
27:33|that like with the help of AI, you also
27:37|have to be careful, right? because
27:39|there's always a risk of them
27:41|hallucinating. So even if you're using
27:43|them, uh I would suggest having a human
27:46|in there as well to triage the output
27:49|from these LLM helpers and analyzer um
27:52|to make sure that they are doing what
27:54|they are told. Exactly. And not
27:57|hallucinating and came up with something
27:59|odd or like even to make sure they are
28:02|not being poisoned as well.
28:04|Yeah, great advice, Haley. Thank you so
28:07|much. Um, this was great. I really
28:09|appreciate you taking the time to come
28:11|on today and and join us. Um,
28:13|[clears throat]
28:13|yeah, thank you so much for having me.
```