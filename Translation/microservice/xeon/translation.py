# Copyright (c) 2024 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import os

from comps import DocSumGateway, MicroService, ServiceOrchestrator, ServiceType

SERVICE_HOST_IP = os.getenv("MEGA_SERVICE_HOST_IP", "0.0.0.0")


class TranslationService:
    def __init__(self, port=8000):
        self.port = port
        self.megaservice = ServiceOrchestrator()

    def add_remote_service(self):
        llm = MicroService(
            name="llm",
            host=SERVICE_HOST_IP,
            port=9000,
            endpoint="/v1/chat/completions",
            use_remote_service=True,
            service_type=ServiceType.LLM,
        )
        self.megaservice.add(llm)
        self.gateway = DocSumGateway(megaservice=self.megaservice, host="0.0.0.0", port=self.port)

    async def schedule(self):
        await self.megaservice.schedule(
            initial_inputs={"query": "Translate this from Chinese to English:\nChinese: 我爱机器翻译。\nEnglish:"}
        )
        result_dict = self.megaservice.result_dict
        print(result_dict)


if __name__ == "__main__":
    docsum = TranslationService(port=8888)
    docsum.add_remote_service()
    asyncio.run(docsum.schedule())
