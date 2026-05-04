# Local URL Delivery Rule

- User feedback: they should not need to ask for the URL after MVP/frontend work.
- Judgment: This changes delivery behavior and should be captured in project rules.
- Rule added to `.agent/rules.md` and `.agent/SKILL.md`: whenever a local dev server is started, restarted, confirmed reachable, or already serving the current app, the final response must include the clickable URL.
- Default URL recorded: `http://localhost:5173/`.
