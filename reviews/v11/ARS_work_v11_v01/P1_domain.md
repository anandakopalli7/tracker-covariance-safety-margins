## Contract Paraphrase

D1 (methodology_rigor): This dimension asks whether the empirical work is built and reported well enough that a specialist could trust and repeat it: the experimental design isolates the effect being claimed, data and runs are handled without selective reporting, variability and uncertainty in the results are quantified with appropriate statistics, and enough configuration detail is disclosed to rebuild the experiments. From a domain-accuracy standpoint, the field's norms for simulation-based studies of automated driving (stated simulator and software versions, scenario parameters, random seeds, number of repetitions, and how estimator settings were chosen) define what adequate looks like, but scoring this dimension belongs to the methodology seat, not to me.

D2 (domain_accuracy): This is the dimension I own. It asks whether what the work says about its field is correct: technical statements about state estimation, uncertainty propagation, probabilistic safety margins, and safety evaluation of automated vehicles must agree with established theory and current evidence; earlier studies must be summarised faithfully rather than strawmanned or overstated; the closest competing approaches must be acknowledged; and specialised vocabulary and reported quantities must carry their accepted meanings, so that the claimed advance is real relative to what the literature already shows.

D3 (argumentative_coherence): This dimension asks whether the central thesis holds together as an argument: each main claim follows from the evidence offered, there are no logical gaps or fallacies that the conclusion rests on, and no load-bearing assumption is left unstated or unsupported, including assumptions about who gains from a proposed safety mechanism, who absorbs its costs (for example in comfort, throughput, or conservatism), and who is excluded from the analysis. Domain errors can feed into incoherence, but the devil's-advocate and methodology seats score this dimension.

D4 (cross_disciplinary_relevance): This dimension asks whether readers from neighbouring communities, such as control engineering, robotics, human factors, traffic engineering, or safety assurance and regulation, can follow the framing, definitions, and implications without insider knowledge, and whether any claim that reaches into those neighbouring fields is backed by evidence rather than asserted. It is scored by the perspective seat.

D5 (writing_and_structure): This dimension asks whether the manuscript is organised logically, explains its ideas clearly, presents figures and tables that are legible and informative, and follows the formatting and reporting conventions of the target outlet. It is scored by the editor-in-chief seat.

D6 (venue_fit_and_contribution): This dimension asks whether the work belongs in the configured venue and whether it adds something original and significant for that venue's readers. Domain accuracy bears on whether a claimed contribution is genuinely new, but the fit and significance judgement belongs to the editor-in-chief seat, and I make no venue-alignment claim in this commitment.

## Scoring Plan

### D2: domain_accuracy
dimension_id: D2
what_to_look_for: Technical correctness of every statement about recursive state estimation and its noise and covariance assumptions, uncertainty-aware or chance-constrained safety margins, longitudinal safety and surrogate-safety metrics, and simulator-based perception-in-the-loop evaluation; faithful representation of cited prior work in multi-object tracking, uncertainty-aware motion planning, and automated-vehicle safety evaluation; acknowledgement of the closest competing approaches; use of field terminology with its accepted meaning; and positioning of the claimed advance against the current state of the art.
what_triggers_block: A material but repairable domain error that a central claim relies on, such as a misstated property of a standard estimator, consistency notion, or risk bound, a directly competing method that is omitted or mischaracterised in a way that changes how the contribution should be judged, or a domain metric or term used with a non-standard meaning that distorts the reported conclusions, each correctable in revision without discarding the core result.
what_triggers_warn: Localised domain inaccuracies that do not carry a central claim, such as imprecise or inconsistent terminology, a missing or outdated citation for a supporting statement, prior work summarised loosely but not wrongly, or a generalisation that reaches modestly beyond the evaluated conditions.
what_triggers_fatal: The central contribution rests on a domain-level error that revision cannot cure without redoing the core work, such as a claimed safety or probabilistic guarantee that contradicts established estimation or risk theory, a headline finding that is already established prior work presented as new, or a misrepresentation of cited evidence on which the main conclusion depends.

criteria_binding_unavailable

[CONTRACT-ACKNOWLEDGED]
