[autogen.oai.client: 09-15 14:59:29] {184} WARNING - The API key specified is not a valid OpenAI format; it won't work with the OpenAI-hosted model.
[autogen.oai.client: 09-15 14:59:29] {184} WARNING - The API key specified is not a valid OpenAI format; it won't work with the OpenAI-hosted model.
[autogen.oai.client: 09-15 14:59:29] {184} WARNING - The API key specified is not a valid OpenAI format; it won't work with the OpenAI-hosted model.
[autogen.oai.client: 09-15 14:59:29] {184} WARNING - The API key specified is not a valid OpenAI format; it won't work with the OpenAI-hosted model.
[autogen.oai.client: 09-15 14:59:29] {184} WARNING - The API key specified is not a valid OpenAI format; it won't work with the OpenAI-hosted model.
[33mUser[0m (to Swagger_Agent):

Convert 'petstore.docx' to openapi specs.

--------------------------------------------------------------------------------
[31m
>>>>>>>> USING AUTO REPLY...[0m
^CTraceback (most recent call last):
  File "/myapp/swagger-generator.py", line 147, in <module>
    chat_result = user_proxy.initiate_chat(swagger_agent, message="Convert 'petstore.docx' to openapi specs.", max_turns = 10)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/autogen/agentchat/conversable_agent.py", line 1095, in initiate_chat
    self.send(msg2send, recipient, request_reply=True, silent=silent)
  File "/usr/local/lib/python3.11/site-packages/autogen/agentchat/conversable_agent.py", line 738, in send
    recipient.receive(message, self, request_reply, silent)
  File "/usr/local/lib/python3.11/site-packages/autogen/agentchat/conversable_agent.py", line 902, in receive
    reply = self.generate_reply(messages=self.chat_messages[sender], sender=sender)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/autogen/agentchat/conversable_agent.py", line 2056, in generate_reply
    final, reply = reply_func(self, messages=messages, sender=sender, config=reply_func_tuple["config"])
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/autogen/agentchat/conversable_agent.py", line 1424, in generate_oai_reply
    extracted_response = self._generate_oai_reply_from_client(
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/autogen/agentchat/conversable_agent.py", line 1443, in _generate_oai_reply_from_client
    response = llm_client.create(
               ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/autogen/oai/client.py", line 766, in create
    response = client.create(params)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/autogen/oai/client.py", line 340, in create
    response = completions.create(**params)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/openai/_utils/_utils.py", line 274, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/openai/resources/chat/completions.py", line 704, in create
    return self._post(
           ^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/openai/_base_client.py", line 1260, in post
    return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/openai/_base_client.py", line 937, in request
    return self._request(
           ^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/openai/_base_client.py", line 973, in _request
    response = self._client.send(
               ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 926, in send
    response = self._send_handling_auth(
               ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 954, in _send_handling_auth
    response = self._send_handling_redirects(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 991, in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 1027, in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpx/_transports/default.py", line 236, in handle_request
    resp = self._pool.handle_request(req)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpcore/_sync/connection_pool.py", line 216, in handle_request
    raise exc from None
  File "/usr/local/lib/python3.11/site-packages/httpcore/_sync/connection_pool.py", line 196, in handle_request
    response = connection.handle_request(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpcore/_sync/connection.py", line 101, in handle_request
    return self._connection.handle_request(request)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpcore/_sync/http11.py", line 143, in handle_request
    raise exc
  File "/usr/local/lib/python3.11/site-packages/httpcore/_sync/http11.py", line 113, in handle_request
    ) = self._receive_response_headers(**kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpcore/_sync/http11.py", line 186, in _receive_response_headers
    event = self._receive_event(timeout=timeout)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpcore/_sync/http11.py", line 224, in _receive_event
    data = self._network_stream.read(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpcore/_backends/sync.py", line 126, in read
    return self._sock.recv(max_bytes)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/ssl.py", line 1295, in recv
    return self.read(buflen)
           ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/ssl.py", line 1168, in read
    return self._sslobj.read(len)
           ^^^^^^^^^^^^^^^^^^^^^^
KeyboardInterrupt
