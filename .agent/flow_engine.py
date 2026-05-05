"""
Executable skill-chain flow engine for ShaderGUI_Learning_v1.0.

This is the project-level equivalent of the Git_learning_v4.0 skill chain:
FlowState + CorePipeline + MCP nodes + runtime guard.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.append(str(Path(__file__).resolve().parent))
from mcp_servers.adp_mcp import ADPMCP
from mcp_servers.app_mcp import AppMCP
from mcp_servers.audit_mcp import AuditMCP
from mcp_servers.build_mcp import BuildMCP
from mcp_servers.course_mcp import CourseMCP
from mcp_servers.design_mcp import DesignMCP
from mcp_servers.mvp_mcp import MVPMCP
from mcp_servers.design_mcp import DesignMCP
from mcp_servers.storyboard_mcp import StoryboardMCP
from mcp_servers.stitch_mcp import StitchMCP
from mcp_servers.v0_mcp import V0MCP
from mcp_servers.voice_mcp import VoiceMCP
from run_guard import TEST_STAGES, assert_workspace, clear_stage_outputs, expand_targets


@dataclass
class FlowState:
    module: str = "Module_01"
    phase: str = "PREREQ"
    status: str = "IDLE"
    v0_log: str | None = None
    v0_prototype_file: str | None = None
    v0_prototype_brief: str | None = None
    v0_chat_url: str | None = None
    mvp_log: str | None = None
    course_file: str | None = None
    slides_file: str | None = None
    transcript_count: int = 0
    audio_log: str | None = None
    stitch_file: str | None = None
    verify_log: str | None = None
    build_log: str | None = None
    audit_log: str | None = None
    last_error: str | None = None
    design_file: str | None = None
    design_brief: str | None = None
    storyboard_file: str | None = None
    storyboard_brief: str | None = None
    contract_check_retries: int = 0
    visual_ref_check_retries: int = 0
    max_retries: int = 3
    contract_check_errors: list = field(default_factory=list)
    visual_ref_check_errors: list = field(default_factory=list)
    design_diagnostics: str | None = None
    visual_spec_file: str | None = None


class CorePipeline:
    def __init__(self, workspace: str | Path):
        self.workspace = assert_workspace(Path(workspace))

    def _fail(self, state: FlowState, message: str) -> FlowState:
        state.status = "FAILED"
        state.last_error = message
        print(f"[PIPELINE FAILED] {message}")
        return state

    def _require_success(self, state: FlowState, response: dict, next_status: str) -> FlowState:
        if response.get("status") != "success":
            return self._fail(state, response.get("message", "未知错误"))
        state.status = next_status
        return state

    def run(self, state: FlowState, stop_after_stage: str = "post", mode: str = "mvp") -> FlowState:
        print("============== ShaderGUI Course DAG Runner ==============")
        print(f"[Task] module={state.module}")

        if state.status == "IDLE":
            print("-> [Prereq 1/3] 检查源材料与 .agent 规则...")
            res = CourseMCP.check_source_material(self.workspace)
            state = self._require_success(state, res, "SOURCE_READY")
            if state.status == "FAILED":
                return state
            print("[Prereq 1/3 OK]")

        if state.status == "SOURCE_READY":
            print("-> [Prereq 2/4] 验证 v0 API Key...")
            res = V0MCP.validate_api_key(self.workspace)
            state = self._require_success(state, res, "V0_READY")
            if state.status == "FAILED":
                return state
            state.v0_log = f"endpoint={res.get('endpoint')}; remaining={res.get('remaining')}; limit={res.get('limit')}"
            print("[Prereq 2/4 OK] v0 API reachable")

        if state.status == "V0_READY":
            if mode == "adp":
                print("-> [Prereq 3/4] CLEANUP_BEFORE_ADP：清理旧产物（ADP scope）...")
                deleted = ADPMCP._clean_adp_products(self.workspace, state.module)
            else:
                print("-> [Prereq 3/4] CLEANUP_BEFORE_MVP：清理旧产物...")
                deleted = clear_stage_outputs(self.workspace, "mvp", state.module)
            print(f"[Prereq 3/4 OK] cleaned={len(deleted)}")
            state.status = "CLEANUP_BEFORE_MVP_READY"

        if state.status == "CLEANUP_BEFORE_MVP_READY":
            print("-> [Prereq 3/3] 生成产物（CourseApp / CourseContent / scripts）...")
            if mode == "adp":
                res = ADPMCP.generate_products(self.workspace, state.module)
                print(f"[ADP] 使用 ADPMCP 生成完整产物")
            else:
                res = MVPMCP.generate_products(self.workspace, state.module)
            state = self._require_success(state, res, "MVP_PRODUCTS_READY")
            if state.status == "FAILED":
                return state
            state.mvp_log = f"app={res.get('app')}; content={res.get('content')}; scripts={res.get('scripts')}"
            print("[Prereq 3/3 OK]")

        if state.status == "MVP_PRODUCTS_READY":
            print("-> [Prereq 3/3] 检查课程 manifest...")
            res = CourseMCP.ensure_course_manifest(self.workspace)
            state = self._require_success(state, res, "MANIFEST_READY")
            if state.status == "FAILED":
                return state
            state.course_file = res.get("course_file")
            state.slides_file = res.get("slides_file")
            print(f"[Prereq 3/3 OK] slides={res.get('slide_count')}")
            if stop_after_stage == "prereq" or stop_after_stage == "cleanup":
                return state

        if state.status == "MANIFEST_READY":
            print("-> [Storyboard 0/1] Preparing narrative storyboard contract...")
            res = StoryboardMCP.prepare_storyboard_contract(self.workspace, state.module)
            state = self._require_success(state, res, "STORYBOARD_READY")
            if state.status == "FAILED":
                return state
            state.storyboard_file = res.get("storyboard_file")
            state.storyboard_brief = res.get("brief_file")
            state.visual_spec_file = state.storyboard_file
            val_res = StoryboardMCP.validate_storyboard_contract(
                self.workspace, state.module, state.storyboard_file
            )
            state = self._require_success(state, val_res, "STORYBOARD_READY")
            if state.status == "FAILED":
                return state
            print(f"[Storyboard 0/1 OK] storyboard_slides={res.get('slide_count')}")

        if state.status == "STORYBOARD_READY":
            print("-> [v0 Design 1/1] 创建 v0 React 原型与设计规则...")
            res = V0MCP.generate_react_prototype(self.workspace, state.module)
            state = self._require_success(state, res, "V0_PROTOTYPE_READY")
            if state.status == "FAILED":
                return state
            state.v0_prototype_file = res.get("prototype_file")
            state.v0_prototype_brief = res.get("brief_file")
            state.v0_chat_url = res.get("chat_url")
            print(f"[v0 Design 1/1 OK] chat={res.get('chat_id')}")

        if state.status == "V0_PROTOTYPE_READY":
            print("-> [Design 0/2] Preparing design contract...")
            res = DesignMCP.prepare_design_contract(self.workspace, state.module)
            state = self._require_success(state, res, "DESIGN_READY")
            if state.status == "FAILED":
                return state
            state.design_file = res.get("design_file")
            state.design_brief = res.get("brief_file")
            print(f"[Design 0/2 OK] design_slides={res.get('slide_count')}")

        if state.status == "DESIGN_READY":
            print("-> [Design 1/2] 契约完整性循环自检...")

            for attempt in range(1, state.max_retries + 1):
                state.contract_check_retries = attempt
                res = DesignMCP.validate_design_contract(
                    self.workspace, state.module, state.design_file
                )
                if res.get("status") == "success":
                    print(f"[Design 1/2 OK] 契约验证通过 (attempt {attempt})")
                    break
                fix_res = DesignMCP.auto_fix_design_contract(
                    self.workspace, state.module, state.design_file, res.get("errors", [])
                )
                if fix_res.get("fixed"):
                    print(f"[Design 1/2 FIX] 自动修正 {len(fix_res.get('fixed', []))} 项，重新验证...")
                else:
                    print(f"[Design 1/2 RETRY] attempt {attempt}/{state.max_retries}: {res.get('message')}")
                state.contract_check_errors = res.get("errors", [])

            if res.get("status") != "success":
                diag_path = DesignMCP.generate_diagnostic_report(
                    self.workspace, state.module, "contract",
                    state.contract_check_errors, state.contract_check_retries,
                    state.max_retries,
                )
                state.design_diagnostics = diag_path
                return self._fail(state, f"契约完整性自检失败 ({state.max_retries} 次)。诊断: {diag_path}")

            print("-> [Design 2/2] 视觉参考循环自检...")

            for attempt in range(1, state.max_retries + 1):
                state.visual_ref_check_retries = attempt
                gen_res = DesignMCP.generate_visual_refs(
                    self.workspace, state.module, state.design_file
                )
                if gen_res.get("status") != "success":
                    print(f"[Design 2/2 RETRY] 生成失败 attempt {attempt}: {gen_res.get('message')}")
                    state.visual_ref_check_errors = gen_res.get("errors", [])
                    continue
                val_res = DesignMCP.validate_visual_refs(
                    self.workspace, state.module, state.design_file
                )
                if val_res.get("status") == "success":
                    print(f"[Design 2/2 OK] 视觉参考验证通过 (attempt {attempt})")
                    break
                print(f"[Design 2/2 RETRY] 验证失败 attempt {attempt}: {val_res.get('message')}")
                state.visual_ref_check_errors = val_res.get("errors", [])

            if val_res.get("status") != "success":
                diag_path = DesignMCP.generate_diagnostic_report(
                    self.workspace, state.module, "visual_ref",
                    state.visual_ref_check_errors, state.visual_ref_check_retries,
                    state.max_retries,
                )
                state.design_diagnostics = diag_path
                return self._fail(state, f"视觉参考自检失败 ({state.max_retries} 次)。诊断: {diag_path}")

            state.status = "TRANSCRIPTS_READY"

        if state.status == "TRANSCRIPTS_READY":
            print("-> [Dev 1/2] 检查逐字稿...")
            res = CourseMCP.ensure_transcripts(self.workspace)
            state = self._require_success(state, res, "TRANSCRIPTS_CHECKED")
            if state.status == "FAILED":
                return state
            state.transcript_count = res.get("transcript_count", 0)
            print(f"[Dev 1/2 OK] transcripts={state.transcript_count}")

        if state.status == "TRANSCRIPTS_CHECKED":
            print("-> [Dev 2/2] 生成讲解音频...")
            res = VoiceMCP.generate_audio(self.workspace, state.module)
            state = self._require_success(state, res, "AUDIO_READY")
            if state.status == "FAILED":
                return state
            state.audio_log = res.get("log")
            print("[Dev 2/2 OK]")
            if stop_after_stage == "dev":
                return state

        if state.status == "AUDIO_READY":
            print("-> [Dev 3/3] Stitch 音频、字幕与播放器运行时...")
            res = StitchMCP.stitch_runtime(self.workspace, state.module)
            state = self._require_success(state, res, "STITCHED")
            if state.status == "FAILED":
                return state
            state.stitch_file = res.get("file")
            print(f"[Dev 3/3 OK] stitched={res.get('slide_count')}")

        if state.status == "STITCHED":
            print("-> [Verify] 课程内容验证...")
            res = AppMCP.verify_course(self.workspace)
            state = self._require_success(state, res, "BUILD_READY")
            if state.status == "FAILED":
                return state
            state.verify_log = res.get("log")
            print("[Verify OK]")

        if state.status == "BUILD_READY":
            print("-> [Build] Vue SPA 构建...")
            res = BuildMCP.build_app(self.workspace)
            state = self._require_success(state, res, "AUDIT_PASSED")
            if state.status == "FAILED":
                return state
            state.build_log = res.get("log")
            print("[Build OK]")

        if state.status == "AUDIT_PASSED":
            print("-> [Audit] npm audit...")
            res = AuditMCP.audit_app(self.workspace)
            state = self._require_success(state, res, "DEPLOY_READY")
            if state.status == "FAILED":
                return state
            state.audit_log = res.get("log")
            print("[Audit OK]")

        print("=========== PIPELINE DEPLOY_READY ===========")
        return state


def main() -> int:
    parser = argparse.ArgumentParser(description="ShaderGUI course skill-chain runner.")
    parser.add_argument("--mode", choices=["test", "production"], required=True)
    parser.add_argument("--stage", choices=sorted(TEST_STAGES), help="test 模式可用：audio / verify / mvp")
    parser.add_argument("--scope", choices=["module", "all-content"], required=True)
    parser.add_argument("--module", default="Module_01")
    parser.add_argument("--basedir", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--max-retries", type=int, default=3, help="自检最大重试次数 (默认 3)")
    parser.add_argument("--adp", action="store_true", help="使用 ADPMCP 生成完整产物（非 MVP）")
    args = parser.parse_args()

    workspace = assert_workspace(Path(args.basedir))
    targets = expand_targets(workspace, args.scope, args.module)
    mode = "adp" if args.adp else "mvp"

    if args.mode == "test" and args.stage:
        for module in targets:
            deleted = clear_stage_outputs(workspace, args.stage, module)
            print(f"[TEST CLEANUP] {module}/{args.stage}: deleted={len(deleted)}")
    elif args.mode == "production" and args.stage:
        parser.error("production 模式不允许提供 --stage")

    failed = []
    engine = CorePipeline(workspace)
    for module in targets:
        final_state = engine.run(FlowState(module=module, max_retries=args.max_retries), stop_after_stage="post", mode=mode)
        print(f"[MODULE {module} END_STATE] {final_state.status}")
        if final_state.status == "FAILED":
            failed.append(module)

    if failed:
        print("[RUN FAILED] " + "、".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
