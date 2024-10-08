import threading, queue

class TaskManager:
    def __init__(self, client, crawler):
        self.request_queue = queue.Queue()
        self.client = client
        self.crawler = crawler

    def stream_from_server(self, prompt):
        prompt = prompt
        if prompt:
            response = self.client.chat.completions.create(
                model='gpt-4',
                messages=[
                    {'role': 'system', 'content': 'You are a helpful assistant'},
                    {'role': 'user', 'content': f'Summarize this content for me please \n"{prompt}"'}
                ],
                stream=True
            )
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        
        else:
            yield 'Prompt is missing!'

    def worker(self):
        while True:
            user_request = self.request_queue.get()
            response_holder = user_request.get('response')
            event = user_request.get('event')
            prompt = user_request.get('prompt')
            
            for chunk in self.stream_from_server(prompt=prompt):
                response_holder.put(chunk)

            event.set()
            self.request_queue.task_done()

    def stream_response(self, prompt):
        response = queue.Queue()
        event = threading.Event()

        self.request_queue.put({
            'prompt': prompt,
            'response': response,
            'event': event
        })

        while not event.is_set() or not response.empty():
            try:
                chunk = response.get(timeout=0.2)
                yield chunk
            except queue.Empty:
                continue

    def process_request(self, urls):
        urls = urls
        content = self.crawler.run(urls=urls)
        return self.stream_response(content)

    def init_app(self):
        threading.Thread(target=self.worker, daemon=True).start()


# urls = ['https://quotes.toscrape.com/random']
# urls = ['https://www.makeoverarena.com/2024/10/07/murdoch-university-rtp-scholarships/']
# urls = ['https://www.makeoverarena.com/2024/10/07/university-of-detroit-mercy-scholarships/']
# return Response(taskmanager.process_request(urls=urls), content_type='text/event-stream')