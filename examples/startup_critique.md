# Example: Startup Idea Critique (Destroy Mode)

**Command:**
```bash
reversebottom --mode destroy "We're building an AI-powered app that matches people with therapists based on their personality type and communication style. We'll use MBTI and DISC assessments to create better matches than existing platforms."
```

---

**Output:**

```
FATAL FLAWS
───────────
1. MBTI and DISC have no validated predictive relationship with therapeutic
   outcomes. The American Psychological Association does not recognize MBTI
   as a clinically valid instrument. A 2021 meta-analysis in Psychological
   Bulletin found that therapist-client alliance — the primary predictor of
   therapeutic success — is formed through in-session interaction, not
   pre-session profiling. You are optimizing for a signal that the research
   literature treats as noise.

2. The matching frame assumes the problem is fit. The actual problem is
   access. In the US, median wait time for a first therapy appointment is
   25 days. In the UK, NHS wait times exceed 18 weeks for most conditions.
   No matching algorithm changes the supply constraint. You are improving
   the queue experience without shortening the queue.

3. Therapists do not want to be matched. Most licensed therapists in
   private practice manage their own intake. They have waiting lists.
   They do not need a matching platform to send them clients — they need
   fewer administrative hours per client. You have not solved a problem
   they have; you have created a new dependency for them.

MARKET / LOGIC REALITY CHECK
─────────────────────────────
BetterHelp — the market leader in therapist matching — has processed
millions of matches using simpler preference-based systems. In 2023 the
FTC required BetterHelp to pay $7.8M in refunds for misleading users about
therapist qualifications. The conclusion the market should draw: the problem
with existing platforms is trust and quality verification, not match
sophistication.

Psychology Today already has 3M+ monthly users doing self-directed therapist
selection by specialty, insurance, and availability. The user's actual
behavior is "find someone who takes my insurance and has an opening."
Personality matching is a feature users request in surveys and ignore in
practice — a classic gap between stated and revealed preference.

WORST-CASE SCENARIO
───────────────────
A user with undiagnosed ADHD is matched with a therapist profiled as
"compatible" based on DISC assessment. The therapist specializes in
relationship issues and has no training in neurodevelopmental conditions.
After 6 sessions, the user reports no progress. They have now spent
$900-1,200, several months, and burned their motivation to try again.

When this pattern is investigated: the matching criteria had zero clinical
basis. You now have a legal and reputational liability with no clinical
accountability framework, no medical advisory board, and no defensible
methodology.

WHAT YOU MISSED
───────────────
You assumed "better matching" is a meaningful concept in therapy. You did
not ask what "better" means clinically, what evidence exists that matching
improves outcomes, or who in the clinical community has endorsed this
framework.

You also assumed therapists are a commodity to be matched against. They are
professionals with their own client selection criteria, specializations,
and ethical obligations. The platform model treats them as supply. That
framing will cause friction at every point of therapist acquisition.

The HIPAA-adjacent nature of mental health data is not mentioned in your
concept. You are proposing to collect personality assessments tied to
mental health service-seeking. The regulatory surface area of this data
is significant and appears to be unplanned for.

VERDICT
───────
You built a personality quiz frontend for a therapist directory that already
exists, added no clinical validity, and called it a matching engine.
```
