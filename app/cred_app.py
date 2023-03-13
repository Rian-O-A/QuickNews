import os
from dotenv import load_dotenv

load_dotenv()

pacote = {"key_api":os.environ["key_api"],"model_engine": os.environ["model_engine"],
            "bbc":{"url":os.environ["bbc_url"],
                    "time_class":os.environ["bbc_time_class"],
                    "a_class":os.environ["bbc_a_class"]}
}
