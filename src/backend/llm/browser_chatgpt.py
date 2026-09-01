import sys
import os
import json
import traceback
from typing import Dict, Any, Optional
from pathlib import Path

# Insert BrowserAPIFree to path
browser_api_path = "/run/media/irxchand/Projects/Python/BrowserAPIFree"
if browser_api_path not in sys.path:
    sys.path.insert(0, browser_api_path)

try:
    from framework.adapter_loader import load_adapter
    from framework.browser_session import BrowserSession
    from framework.chat_runtime import ChatRuntime
    from framework.response_collector import ResponseCollector
except ImportError as e:
    print(f"[BROWSER LLM IMPORT WARNING] {e}")

from .base import BaseLLMProvider, LLMReasoningOutput


DEDICATED_CHATGPT_URL = os.getenv(
    "CHATGPT_LEVEL_C_URL",
    "https://chatgpt.com/c/6a92fff8-d234-83e9-988e-5e04ab074efb"
)


class BrowserChatGPTProvider(BaseLLMProvider):
    """
    Live Browser-based ChatGPT Provider connected to dedicated reasoning agent.
    
    Target URL: https://chatgpt.com/c/6a92fff8-d234-83e9-988e-5e04ab074efb
    """

    def __init__(self, prompt_file: Optional[str] = None, chat_url: Optional[str] = None):
        super().__init__(prompt_file or "src/backend/prompts/chatgpt_level_c_system_prompt.txt")
        self.cookies_path = "/run/media/irxchand/Projects/Python/BrowserAPIFree/cookies.json"
        self.chat_url = chat_url or DEDICATED_CHATGPT_URL

    def build_request_prompt(self, context: Dict[str, Any]) -> str:
        """Formats the exact structured prompt according to Level C requirements."""
        level_b_data = {
            "segmentation": context.get("segmentation"),
            "segmentation_confidence": context.get("segmentation_confidence"),
            "feature_information": context.get("feature_information"),
            "classical_result": context.get("classical_result"),
            "quantum_result": context.get("quantum_result"),
            "activation_maps": context.get("activation_maps"),
            "existing_evidence": context.get("existing_evidence"),
            "metadata": context.get("metadata")
        }
        level_b_str = json.dumps(level_b_data, indent=2)
        experiment_str = json.dumps(context.get("experiment_information", {}), indent=2)

        return (
            f"{self.system_prompt}\n\n"
            f"=== CURRENT IMAGE ===\n"
            f"The attached image is the current chest X-ray under analysis.\n\n"
            f"=== LEVEL-B EVIDENCE ===\n"
            f"{level_b_str}\n\n"
            f"=== CURRENT EXPERIMENT CONTEXT ===\n"
            f"{experiment_str}\n\n"
            f"=== TASK ===\n"
            f"Inspect the attached X-ray together with the supplied Level-B evidence.\n"
            f"Determine what the prototype application should display for this specific image.\n"
            f"Return ONLY valid JSON matching the required Level-C schema.\n"
            f"Do not reuse fixed scores or annotations from previous cases."
        )

    def analyze(self, image_path: str, context: Dict[str, Any]) -> LLMReasoningOutput:
        """
        Dispatches actual image + Level B context directly to dedicated ChatGPT conversation.
        """
        img_path = Path(image_path).resolve()
        if not img_path.exists():
            raise FileNotFoundError(f"X-ray image not found at path: {img_path}")

        full_prompt = self.build_request_prompt(context)
        adapter = load_adapter("chatgpt")
        
        # Default to visible window (headless=False) so user can see the browser window live
        is_headless = os.getenv("CHATGPT_HEADLESS", "false").lower() in ("true", "1")
        if "DISPLAY" not in os.environ:
            os.environ["DISPLAY"] = ":0"

        session = BrowserSession("level_c_active_session", headless=is_headless, hidden_headful=False)
        
        try:
            page = session.start()
            chat = ChatRuntime(page, adapter)
            print(f"[BROWSER CHATGPT] Navigating to dedicated chat: {self.chat_url}")
            chat.open_chat(self.chat_url)
            
            # Wait for input box to mount and become visible
            page.locator("div#prompt-textarea, [id*='prompt'], div[contenteditable='true']").first.wait_for(state="visible", timeout=20000)

            # Send prompt WITH actual image attachment
            print(f"[BROWSER CHATGPT] Attaching actual image {img_path} and submitting prompt...")
            chat.send_message(full_prompt, [str(img_path)])

            collector = ResponseCollector(page, adapter)
            raw_response, metrics = collector.wait_and_collect()
            print(f"[BROWSER CHATGPT] Live response received from dedicated agent (streaming {metrics.get('t_streaming', 0):.1f}ms).")

            # Validate and parse strict JSON
            output = self.validate_and_parse_response(raw_response)
            output.provenance = "LLM_ASSISTED_PROTOTYPE"
            return output

        except Exception as e:
            traceback.print_exc()
            raise RuntimeError(f"Dedicated Browser ChatGPT analysis failed: {str(e)}")
        finally:
            session.stop()
