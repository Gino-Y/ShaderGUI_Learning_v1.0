# 2026-05-06 Visual Execution Optimization Plan

## Context

The current course visuals remain weak even after multiple storyboard upgrades. The project diagnosis is that the storyboard/design contracts are richer than the Vue renderers' current consumption ability.

## Decision

Visual quality work must shift from "upgrade storyboard prose" to an executable rendering loop:

```text
storyboard/design intent
-> visual tokens
-> Vue renderer implementation
-> screenshot visual audit
-> delivery report
```

## Deliverable

The executable optimization plan has been written to:

```text
.agent/reports/visual-execution-optimization-plan.md
```

## Execution Principle

Do not continue optimizing storyboard descriptions alone. The next effective implementation step is to introduce `visual-tokens.json`, `VisualCompilerMCP`, renderer capability mapping, and screenshot-based visual audit so that p00/p01 visibly diverge based on concrete visual contracts.

## DAG Impact

The proposed next DAG shape is:

```text
StoryboardMCP -> DesignMCP -> VisualCompilerMCP -> visual-tokens.json -> Vue renderers -> VisualAuditMCP
```

The current DAG is not changed by this memory entry; the plan defines the next executable change set.
