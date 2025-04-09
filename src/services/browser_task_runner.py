import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use.browser.browser import Browser, BrowserConfig
from services.config_manager import ConfigManager
import logging
from datetime import datetime
from browser_use import Agent

logger = logging.getLogger(__name__)

class BrowserTaskExecutionError(Exception):
    pass

class BrowserTaskRunner:
    def __init__(self):
        load_dotenv(find_dotenv(), override=True)
        self.history_folder = Path(__file__).parent.parent.parent / 'history'
        os.environ['HISTORY_DIR'] = str(self.history_folder)
        self.config_manager = ConfigManager()
        browser_config = self._get_browser_config()
        self.browser = Browser(config=browser_config)

    def _get_browser_config(self) -> BrowserConfig:
        browser_type = self.config_manager.get_config('BROWSER_TYPE', 'local').lower()
        cloud_provider = self.config_manager.get_config('BROWSER_CLOUD_PROVIDER', '').lower()
        headless_mode = self.config_manager.get_config('BROWSER_HEADLESS', 'true').lower() == 'true'

        config_params = {
            'headless': headless_mode,
            'disable_security': True
        }

        if browser_type == 'remote':
            config_params.pop('headless', None)
            config_params.pop('disable_security', None)

            api_key = ''
            if cloud_provider == 'browserbase':
                api_key = self.config_manager.get_config('BROWSERBASE_API_KEY')
                config_params['cdp_url'] = f"wss://connect.browserbase.com?apiKey={api_key}"
            elif cloud_provider == 'steeldev':
                api_key = self.config_manager.get_config('STEELDEV_API_KEY')
                config_params['cdp_url'] = f"wss://connect.steel.dev?apiKey={api_key}"
            elif cloud_provider == 'browserless':
                api_key = self.config_manager.get_config('BROWSERLESS_API_KEY')
                config_params['wss_url'] = f"wss://production-sfo.browserless.io/chromium/playwright?token={api_key}"
            elif cloud_provider == 'lightpanda':
                api_key = self.config_manager.get_config('LIGHTPANDA_API_KEY')
                config_params['cdp_url'] = f"wss://cloud.lightpanda.io/ws?token={api_key}"
            else:
                raise ValueError(f"Unsupported cloud provider: {cloud_provider}")

        return BrowserConfig(**config_params)

    def get_llm(self):
        provider = self.config_manager.get_config('MODEL_PROVIDER', 'openai').lower()
        model = self.config_manager.get_config('MODEL_NAME', 'gpt-4')

        if provider == 'anthropic':
            return ChatAnthropic(
                model=model,
                anthropic_api_key=self.config_manager.get_config('ANTHROPIC_API_KEY'),
                temperature=0.7
            )
        elif provider == 'azure':
            return AzureChatOpenAI(
                api_version=self.config_manager.get_config('AZURE_OPENAI_API_VERSION', '2024-08-01-preview'),
                azure_deployment=self.config_manager.get_config('AZURE_DEPLOYMENT_NAME'),
                azure_endpoint=self.config_manager.get_config('AZURE_OPENAI_ENDPOINT'),
                api_key=self.config_manager.get_config('AZURE_OPENAI_API_KEY'),
                temperature=0.7,
                model_name=self.config_manager.get_config('AZURE_DEPLOYMENT_NAME')
            )
        elif provider == 'deepseek':
            return ChatOpenAI(
                model=model,
                api_key=self.config_manager.get_config('DEEPSEEK_API_KEY'),
                openai_api_base="https://api.deepseek.com/v1",
                temperature=0.7
            )
        elif provider == 'groq':
            return ChatGroq(
                model=model,
                api_key=self.config_manager.get_config('GROQ_API_KEY'),
                temperature=0.7
            )
        elif provider == 'google':
            return ChatGoogleGenerativeAI(
                model=model,
                google_api_key=self.config_manager.get_config('GOOGLE_API_KEY'),
                temperature=0.7
            )
        else:
            return ChatOpenAI(
                model=model,
                api_key=self.config_manager.get_config('OPENAI_API_KEY'),
                temperature=0.7
            )

    async def execute_task(self, task: str) -> tuple[str, str]:
        use_vision = self.config_manager.get_config('USE_VISION', 'false').lower() == 'true'
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        timestamp_folder = self.history_folder / timestamp
        timestamp_folder.mkdir(parents=True, exist_ok=True)
        history_path = timestamp_folder / f'history_{timestamp}.json'

        agent = Agent(
            task=task,
            llm=self.get_llm(),
            use_vision=use_vision,
            browser=self.browser
        )

        try:
            await agent.run(max_steps=50)
            agent.save_history(str(history_path))
            return str(history_path), timestamp
        except Exception as e:
            raise BrowserTaskExecutionError(f"Task execution failed: {str(e)}")
        finally:
            await self.browser.close()

    async def close(self):
        await self.browser.close()
