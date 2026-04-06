# ReverseBottom

> An anti-assistant. It will not help you feel better about your ideas.

---

## What This Is

Most AI assistants are optimized to agree with you, encourage you, and give you the answer you were hoping for.

ReverseBottom does the opposite.

It is a **cognitive stress-testing tool** built on top of LLMs. You give it an idea, a decision, a plan, or an argument. It attacks it — from the inside, from the outside, and from angles you didn't consider.

It has three operating modes:

| Mode | What it does |
|------|-------------|
| `destroy` | Finds every flaw, contradiction, and risk in your idea |
| `reverse` | Inverts your core assumption and builds the mirror-world logic |
| `shadow` | Surfaces your hidden motives, cognitive biases, and blind spots |

This is not a replacement for good advice. It is a tool for finding the places where you are wrong before someone else does.

---

## Philosophy

The assistant industry has a problem: **sycophancy at scale**.

LLMs trained on human feedback learn that humans prefer validation. The result is a generation of tools that tell you your startup idea is great, your decision makes sense, and your argument is compelling — even when none of that is true.

ReverseBottom inverts this incentive structure. Its job is not to satisfy you. Its job is to be useful — and the most useful thing it can do is show you what you missed.

> "A friend who lies to you is more dangerous than an enemy who tells you the truth."

The modes are not tricks. They are structured frameworks for adversarial thinking:

- **Destroy** is for ideas that need to survive scrutiny before you invest in them
- **Reverse** is for when you're too attached to your frame to see alternatives
- **Shadow** is for when the problem is the framing itself, not the content

---

## Installation

```bash
git clone https://github.com/yourname/reversebottom.git
cd reversebottom
pip install -e .
```

Set your API key (supports OpenAI and Anthropic):

```bash
export OPENAI_API_KEY=sk-...
# or
export ANTHROPIC_API_KEY=sk-ant-...
```

Configure which provider in `.env` or via environment:

```bash
export RB_PROVIDER=openai        # or: anthropic
export RB_MODEL=gpt-4o           # or: claude-opus-4-6
```

---

## CLI Usage

```bash
# Interactive mode — prompts you for input and mode selection
reversebottom

# Direct input with mode flag
reversebottom --mode destroy "We should build a social network for pets"

# Pipe input
echo "I'm thinking of quitting my job to start a crypto project" | reversebottom --mode shadow

# JSON output (for scripting)
reversebottom --mode reverse --json "Remote work is more productive than office work"
```

---

## API Usage

Start the server:

```bash
reversebottom serve --port 8000
```

Send a request:

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "We should build a social network for pets",
    "mode": "destroy"
  }'
```

---

## Example Outputs

### Destroy Mode — Startup Idea

**Input:** `"We're building an AI-powered app that matches people with therapists based on personality type."`

**Output:**
```
FATAL FLAWS
───────────
1. Personality typing is not clinical matching. MBTI and similar frameworks
   have no validated correlation with therapeutic outcomes. You are optimizing
   for a metric that does not predict success.

2. The supply side is broken. Licensed therapists in English-speaking markets
   have 6-12 week waitlists. Matching faster does not create capacity.

3. You are not competing with bad matching — you are competing with "any
   therapist who has an opening." The user's alternative is not your inferior
   competitor; it is desperation and whatever slot they can get.

MARKET REALITY CHECK
────────────────────
BetterHelp has $1B+ revenue and is currently facing FTC action for misleading
claims about therapist qualifications. The category leader is under regulatory
scrutiny. This is not a market ready for a new entrant.

WORST-CASE SCENARIO
───────────────────
A user with undiagnosed bipolar disorder is matched with a therapist who
specializes in CBT for anxiety. The mismatch causes harm. You are now in a
HIPAA-adjacent liability situation with zero clinical accountability framework.

WHAT YOU MISSED
───────────────
You assumed the problem is matching. The actual problem is access — cost,
availability, and insurance. Matching is a nice-to-have on top of a solved
access layer. You have no access layer.

VERDICT
───────
You built a search filter on top of a broken supply chain and called it a
solution.
```

---

### Reverse Mode — Assumption Inversion

**Input:** `"Remote work gives people more freedom and is better for productivity."`

**Output:**
```
CORE ASSUMPTION IDENTIFIED
──────────────────────────
That freedom and productivity are positively correlated — and that the
individual worker is the right unit of measurement for both.

INVERSION
─────────
What if freedom decreases productivity — not through laziness, but through
decision fatigue and loss of structure? And what if productivity is a team-level
property that degrades when individuals optimize locally?

THE MIRROR WORLD
────────────────
In the inverted model: the office is not a control mechanism — it is a
coordination substrate. The friction of commuting, fixed hours, and shared
space is not waste — it is the forcing function that synchronizes human
cognitive rhythms across a team.

Remote work does not give people freedom. It transfers the cost of coordination
from the organization to the individual. Each worker now manages their own
schedule, their own environment, their own context-switching. The company
eliminated its overhead by externalizing it onto its employees.

The worker who says "I'm more productive at home" is often measuring output in
a single session — not measuring the 3x increase in async clarification
loops, the decisions that never get made because no one is in the same room,
or the institutional knowledge that dissolves when people have no shared
physical context.

STRESS TEST OF THE INVERSION
─────────────────────────────
This holds most strongly for: creative collaboration, early-stage team
formation, and roles where informal interaction generates unexpected value.
It holds weakly for: deep individual work, well-defined tasks with clear
specs, roles with stable processes.

WHAT THE INVERSION REVEALS
───────────────────────────
"Remote is better for productivity" is a claim about individuals measured
in isolation. It says nothing about organizations. The debate is happening
at the wrong level of analysis.
```

---

### Shadow Mode — Hidden Bias Detection

**Input:** `"I think I should leave my corporate job and start my own business. I've always been entrepreneurial and I hate bureaucracy."`

**Output:**
```
WHAT YOU'RE REALLY ASKING
──────────────────────────
"Validate my decision. I've already decided. Tell me I'm right."

This is not a question about whether you should start a business. It is
a request for permission from an external authority (an AI) to do what
you have already committed to emotionally.

COGNITIVE BIASES DETECTED
──────────────────────────
1. IDENTITY-BASED REASONING — "I've always been entrepreneurial" treats
   a personality narrative as evidence of fitness for a specific action.
   Feeling entrepreneurial is not the same as having the risk tolerance,
   capital, network, or market insight to run a company.

2. CONTRAST EFFECT — "I hate bureaucracy" defines the alternative
   (your own company) by contrast to the worst features of your current
   environment. Your own company will have bureaucracy. It will be
   bureaucracy you created, which is often worse.

3. SURVIVORSHIP BIAS (pre-emptive) — Your reference pool for
   "entrepreneurial people" is probably successful founders. The
   population of people who "always felt entrepreneurial" and failed
   quietly is invisible to you.

HIDDEN ASSUMPTIONS
──────────────────
- That your unhappiness is caused by employment structure, not by
  this specific job, this specific manager, or this specific industry.
- That you know what you would build.
- That your savings runway is sufficient (you didn't mention it).
- That "starting a business" and "escaping bureaucracy" are the same thing.

EMOTIONAL INVESTMENT SIGNALS
──────────────────────────────
"I've always been" — identity language. This idea is not new; you have
been building a self-concept around it. Contradicting it now feels
like an attack on who you are, not just what you plan to do.

THE QUESTION YOU SHOULD HAVE ASKED
────────────────────────────────────
"What specifically is broken in my current situation, and is starting
a business the most direct fix — or is it the most dramatic one?"
```

---

## Configuration

All config via environment variables or a `.env` file:

```env
RB_PROVIDER=openai           # openai | anthropic
RB_MODEL=gpt-4o              # any model name for the provider
RB_TEMPERATURE=0.7           # 0.0–1.0
RB_MAX_TOKENS=2048
RB_DEFAULT_MODE=destroy      # destroy | reverse | shadow
```

---

## Extending Modes

Add a new mode by creating `reversebottom/prompts/yourmode.py` and `reversebottom/modes/yourmode.py`, then registering it in `reversebottom/router.py`.

Each mode is a plain Python class with a `run(text: str) -> str` method. No magic.

---

## When To Use Each Mode

**Use Destroy when:**
- You have a new idea and want to stress-test it before committing resources
- You're about to make a pitch and want to anticipate objections
- Someone has given you an argument and you want to understand its weaknesses

**Use Reverse when:**
- You're too attached to a frame to see alternatives
- You want to understand the strongest version of the opposing view
- You suspect your premise might be wrong but can't see how

**Use Shadow when:**
- You feel like you're asking the right question but getting the wrong answers
- You want to understand the emotional subtext of a decision
- You're trying to audit your own reasoning for bias

---

## License

MIT. Use it however you want. Attribution appreciated but not required.

---

## Contributing

PRs welcome. New modes especially. Keep the prompts sharp — if a response could appear in a motivational poster, the prompt is wrong.
