import chainlit as cl
import vertexai
from uuid import uuid4
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import asyncio

load_dotenv()
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = os.environ["GOOGLE_CLOUD_LOCATION"]
agent_resource_name = os.environ["AGENT_RESOURCE_NAME"]  ## Added by Nov05
bucket_name = f"gs://{project_id}-bucket"

client = vertexai.Client(
    project=project_id,
    location=location,
)

agent = client.agent_engines.get(name=agent_resource_name)

def convert_img_tags_to_chainlit_images(msg):
    img_list = []
    if not msg.content:
        return msg
        
    soup = BeautifulSoup(msg.content, "html.parser")
    print("Converting img tags to chainlit images")
    
    found_imgs = soup.find_all("img")
    for img_tag in found_imgs:
        if img_tag.has_attr("src"):
            img = cl.Image(url=img_tag["src"], name="swatch", display="inline")
            img_list.append(img)
            # Remove the tag so it doesn't appear as a broken image in text
            img_tag.decompose()
            
    msg.elements = img_list
    # Only update content if there's actual text left, otherwise keep original
    # logic or a space to ensure msg.content isn't 'falsy' if elements exist
    cleaned_text = soup.get_text().strip()
    if cleaned_text:
        msg.content = cleaned_text
    elif img_list:
        # If we have images but no text, provide a small spacer so Chainlit displays it
        msg.content = " "
    return msg


@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Painting Project Help",
            message="Tell me about Cymbal Shops' interior paints.",
            icon="/public/swatches.svg",
        )
    ]


@cl.on_chat_start
async def on_chat_start():
    print("A new chat session has started!")
    user_id = "user"
    
    try:
        # Use make_async to avoid blocking the event loop during session creation
        session_details = await cl.make_async(agent.create_session)(user_id=user_id)
        cl.user_session.set("user_id", user_id)
        cl.user_session.set("session_id", session_details["id"])
        cl.user_session.set(
            "message_history",
            [{"role": "system", "content": "You are a helpful assistant."}],
        )
        
    except Exception as e:
        print(f"Error starting chat: {e}")
        await cl.Message(content="Failed to initialize agent session. Please refresh the page.").send()


@cl.on_message
async def main(message: cl.Message):
    # Ensure session is ready, wait slightly if it's currently initializing
    for _ in range(10):
        user_id = cl.user_session.get("user_id")
        session_id = cl.user_session.get("session_id")
        if session_id:
            break
        await asyncio.sleep(0.5)
    else:
        await cl.Message(content="Session initialization is taking longer than expected. Please refresh.").send()
        return

    message_history = cl.user_session.get("message_history")

    message_history.append({"role": "user", "content": message.content})
    msg = cl.Message(content="")

    try:
        async_stream = agent.async_stream_query(
            user_id=user_id,
            session_id=session_id,
            message=message.content,
        )

        # Use the native async generator provided by ADK
        async for event in async_stream:
            print(f"DEBUG: Received event: {event}")
            
            # Check if the stream returned an explicit backend error
            if isinstance(event, dict):
                if "error" in event:
                    await cl.Message(content=f"Agent Engine Error: {event['error']}").send()
                    return
                # Handle payload errors like "code: 498, Event loop is closed" silently
                if "code" in event and "message" in event:
                    print(f"Agent Backend Notification (Code {event.get('code')}): {event.get('message')}")
                    continue

            # Check for standard content and parts
            if "content" in event and "parts" in event["content"]:
                for part in event["content"]["parts"]:
                    if "text" in part:
                        await msg.stream_token(part["text"])

        # Post-process message
        convert_img_tags_to_chainlit_images(msg)
        
        # Check if we have content OR elements (images)
        actual_content = msg.content.strip() if msg.content else ""
        if actual_content or msg.elements:
            message_history.append({"role": "assistant", "content": msg.content})
            await msg.update()
        else:
            # If the stream finished completely empty, optionally clean up the empty message
            await msg.remove()

    except Exception as e:
        print(f"Error querying agent: {e}")
        await cl.Message(content=f"An error occurred: {str(e)}").send()
