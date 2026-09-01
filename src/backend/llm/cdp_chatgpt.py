import sys
import os
import json
import time
import traceback
from typing import Dict, Any, Optional
from pathlib import Path
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

from .base import BaseLLMProvider, LLMReasoningOutput
from src.backend.prompt_builder import build_clinical_reasoning_prompt, build_edge_case_prompt

DEDICATED_CHATGPT_URL = os.getenv(
    "CHATGPT_LEVEL_C_URL",
    "https://chatgpt.com/c/6a92fff8-d234-83e9-988e-5e04ab074efb"
)
CDP_ENDPOINT_URL = os.getenv("CDP_ENDPOINT_URL", "http://127.0.0.1:9222")


class CDPChatGPTProvider(BaseLLMProvider):
    """
    Connects directly to your active Google Chrome browser session via CDP
    on http://127.0.0.1:9222 and operates inside your open ChatGPT conversation tab.
    """

    def __init__(self, prompt_file: Optional[str] = None, cdp_url: Optional[str] = None, chat_url: Optional[str] = None):
        super().__init__(prompt_file or "src/backend/prompts/chatgpt_level_c_system_prompt.txt")
        self.cdp_url = cdp_url or CDP_ENDPOINT_URL
        self.chat_url = chat_url or DEDICATED_CHATGPT_URL

    def build_request_prompt(self, context: Dict[str, Any]) -> str:
        """
        Uses the prompt builder to construct either a KNOWN benchmark prompt
        or an UNKNOWN judge prompt for the dedicated ChatGPT agent.
        """
        image_path = context.get("image_path", "")
        available_evidence = {
            "image_info": context.get("image_info", {}),
            "segmentation": context.get("segmentation"),
            "segmentation_confidence": context.get("segmentation_confidence"),
            "feature_information": context.get("feature_information"),
            "classical_result": context.get("classical_result"),
            "quantum_result": context.get("quantum_result"),
            "activation_maps": context.get("activation_maps"),
            "existing_evidence": context.get("existing_evidence")
        }
        experiment_context = context.get("experiment_context") or context.get("experiment_information", {})
        metadata = context.get("metadata", {})
        is_known = bool(context.get("is_known"))
        known_data = context.get("known_data", {})

        return build_clinical_reasoning_prompt(
            image_path=image_path,
            available_evidence=available_evidence,
            experiment_context=experiment_context,
            metadata=metadata,
            is_known=is_known,
            known_data=known_data
        )

    def analyze(self, image_path: str, context: Dict[str, Any]) -> LLMReasoningOutput:
        img_path = Path(image_path).resolve()
        if not img_path.exists():
            raise FileNotFoundError(f"Image not found at {img_path}")

        context["image_path"] = str(img_path)
        prompt_text = self.build_request_prompt(context)
        case_id = context.get("case_id", "UNKNOWN_JUDGE_CASE")

        print("==================================================")
        print(f"[EDGE CASE REASONING] CASE ID: {case_id}")
        print(f"[EDGE CASE REASONING] IMAGE: {img_path.name} ({img_path})")
        print(f"[EDGE CASE REASONING] AVAILABLE EVIDENCE: seg={bool(context.get('segmentation'))}, feat={bool(context.get('feature_information'))}, classical={context.get('classical_result')}, quantum={context.get('quantum_result')}")
        print(f"[EDGE CASE REASONING] TRAINING DATA CONTEXT: {context.get('experiment_context', {}).get('training_data_fraction', '10%')}")
        print(f"[EDGE CASE REASONING] CHATGPT TARGET: {self.chat_url}")
        print("==================================================")

        if sync_playwright is None:
            raise RuntimeError("Playwright is not installed. Please install playwright to use CDPChatGPTProvider.")

        with sync_playwright() as p:
            try:
                browser = p.chromium.connect_over_cdp(self.cdp_url)
            except Exception as e:
                raise RuntimeError(
                    f"Could not connect to existing Chrome instance on {self.cdp_url}. "
                    f"Make sure Chrome is running with --remote-debugging-port=9222. Details: {e}"
                )

            # Find matching ChatGPT page by URL
            target_page = None
            for ctx in browser.contexts:
                for page in ctx.pages:
                    if "6a92fff8-d234-83e9-988e-5e04ab074efb" in page.url or "chatgpt.com/c/" in page.url:
                        target_page = page
                        break
                if target_page:
                    break

            if not target_page:
                for ctx in browser.contexts:
                    for page in ctx.pages:
                        if "chatgpt.com" in page.url:
                            target_page = page
                            break
                    if target_page:
                        break

            # If no ChatGPT tab is open at all, open a new page and navigate to chat_url
            if not target_page:
                print(f"[EDGE CASE REASONING] No active ChatGPT tab found. Opening {self.chat_url}...")
                ctx = browser.contexts[0] if browser.contexts else browser.new_context()
                target_page = ctx.new_page()
                target_page.goto(self.chat_url)
                target_page.wait_for_load_state("domcontentloaded")
                time.sleep(2.0)

            # Keep execution in the background without stealing focus or popping up the window

            print(f"[EDGE CASE REASONING] Connected to tab: {target_page.url}")

            # 1. Attach Actual Image File
            print("[EDGE CASE REASONING] IMAGE ATTACHMENT START")
            file_input_selector = "input[type='file']"
            try:
                target_page.wait_for_selector(file_input_selector, timeout=8000, state="attached")
                target_page.set_input_files(file_input_selector, [str(img_path)])
                print("[EDGE CASE REASONING] IMAGE ATTACHED SUCCESSFULLY")
                time.sleep(1.8)
            except Exception as e:
                print(f"[EDGE CASE REASONING] Image attachment warning: {e}")

            # Clean any overlay artifacts
            try:
                target_page.evaluate("""
                    () => {
                        const overlays = document.querySelectorAll('div[data-state="open"], div[class*="backdrop"], div[class*="overlay"]');
                        overlays.forEach(el => {
                            if (el.textContent.includes('Drop any file') || el.textContent.includes('Add anything')) {
                                el.remove();
                            }
                        });
                    }
                """)
            except Exception:
                pass

            # 2. Submit Edge-Case Prompt
            prompt_selector = "div#prompt-textarea, textarea[placeholder*='Message']"
            target_page.wait_for_selector(prompt_selector, timeout=12000)

            # Record assistant messages count before submission
            assistant_selector = "div[data-message-author-role='assistant']"
            existing_messages = target_page.locator(assistant_selector).count()

            print("[EDGE CASE REASONING] PROMPT SUBMISSION START")
            # Record last assistant text before sending
            assistant_nodes = target_page.locator(assistant_selector)
            prev_last_text = ""
            if assistant_nodes.count() > 0:
                prev_last_text = assistant_nodes.last.inner_text().strip()

            prompt_input = target_page.locator(prompt_selector).first
            prompt_input.click()
            prompt_input.fill(prompt_text)
            time.sleep(0.4)

            # Click send button
            send_clicked = False
            send_btn_selectors = [
                "button[data-testid='send-button']",
                "button[aria-label*='Send prompt']",
                "button[aria-label*='Send message']",
                "button[aria-label*='Send']",
                "button[data-testid='composer-speech-button'] + button",
                "form button:has(svg)"
            ]
            for sel in send_btn_selectors:
                try:
                    btn = target_page.locator(sel).first
                    if btn.is_visible() and btn.is_enabled():
                        btn.click(timeout=2000)
                        send_clicked = True
                        print(f"[EDGE CASE REASONING] Clicked send button using selector: {sel}")
                        break
                except Exception:
                    pass

            if not send_clicked:
                # Fallback JS click
                try:
                    js_clicked = target_page.evaluate("""
                        () => {
                            const btn = document.querySelector('button[data-testid="send-button"], button[aria-label*="Send"], button:has(svg)');
                            if (btn && !btn.disabled) {
                                btn.click();
                                return true;
                            }
                            return false;
                        }
                    """)
                    if js_clicked:
                        send_clicked = True
                        print("[EDGE CASE REASONING] Clicked send button via JS evaluation.")
                except Exception:
                    pass

            if not send_clicked:
                print("[EDGE CASE REASONING] Dispatching Enter key to prompt input.")
                target_page.keyboard.press("Enter")

            print("[EDGE CASE REASONING] MESSAGE SENT")

            # 3. Fast streaming detection for complete JSON
            print("[EDGE CASE REASONING] WAITING FOR CHATGPT RESPONSE...")
            time.sleep(2.0)

            raw_text = ""
            start_poll = time.time()
            max_wait_seconds = 180.0

            while time.time() - start_poll < max_wait_seconds:
                assistant_nodes = target_page.locator(assistant_selector)
                if assistant_nodes.count() > 0:
                    current_text = assistant_nodes.last.inner_text().strip()
                    
                    # Ensure this is a new response, not the previous turn
                    if current_text != prev_last_text:
                        # Check if JSON closing bracket and valid JSON has arrived
                        if "}" in current_text:
                            try:
                                import re
                                json_match = re.search(r'\{.*\}', current_text, re.DOTALL)
                                if json_match:
                                    json_candidate = json_match.group(0)
                                    json.loads(json_candidate)
                                    raw_text = current_text
                                    print(f"[EDGE CASE REASONING] FAST STREAM CAPTURED IN {time.time() - start_poll:.2f}s")
                                    break
                            except Exception:
                                pass
                time.sleep(0.5)

            if not raw_text:
                raise TimeoutError("ChatGPT response timed out after 180s without completing valid JSON response.")

            print("[EDGE CASE REASONING] RESPONSE RECEIVED")

            # Validate and Parse JSON using base class validator
            import re
            cleaned_text = raw_text.strip()
            # Extract JSON substring if wrapped in text or backticks
            json_match = re.search(r'\{.*\}', cleaned_text, re.DOTALL)
            if json_match:
                cleaned_text = json_match.group(0)

            output: LLMReasoningOutput = self.validate_and_parse_response(cleaned_text)

            print("[EDGE CASE REASONING] JSON VALIDATED SUCCESSFULLY")
            print(f"[EDGE CASE REASONING] RESULT RENDERED (Provenance: LLM_ASSISTED_PROTOTYPE)")
            print(f"  Prediction: {output.prediction}")
            print(f"  Classical: {output.classical_score:.3f} | Quantum: {output.quantum_score:.3f}")

            return output
