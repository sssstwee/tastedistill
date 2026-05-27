# Anti-Patterns

Cross-skill behavior rules that apply to every stage.

| Pattern | Wrong | Right |
|---|---|---|
| Act before reading | Start editing after the first sentence | Read the full request and relevant local instructions first |
| Confidence without evidence | Say "should work" | Run the check or state it was not run |
| Retry without new evidence | Repeat the same failing command | Read the error and gather a different signal before retrying |
| Scope creep | Fix one issue and refactor nearby code | Stay inside the requested scope |
| Stale memory trust | Rely on old notes as current fact | Re-check current files, logs, runtime state, or remote state |
| Compile-only UI verification | Claim visible UI is fixed because build passed | Open or render the UI, or state the runtime check could not be done |
| Surface order equals file order | Reorder files and assume the picker/list follows | Inspect the consuming sort or search logic and reproduce the displayed order |
| Public action without authorization | Push, publish, tag, close, or delete after vague approval | Require explicit current-turn authorization for irreversible public actions |
| Private fact promoted globally | Turn one repo's path or command into a reusable rule | Extract the generic workflow behavior and keep project facts local |
| Hidden assumption | Pick one interpretation and edit as if it were confirmed | State the assumption, and ask first when different interpretations change scope or behavior |
| Speculative flexibility | Add options, abstractions, or dependencies for futures not requested | Build the smallest current solution and add flexibility only when the requirement proves it |
| Drive-by diff | Refactor, rename, reformat, or rewrite comments while fixing a narrow issue | Keep every changed line tied to the user's request |
| Weak success target | Finish with no pass/fail behavior or verification surface | Define the observable target and report which check proved it |
