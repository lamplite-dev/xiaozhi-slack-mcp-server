import os
import logging
from fastmcp import FastMCP
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Initialize the MCP Server
mcp = FastMCP("Slack Bot")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Slack Configuration
slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
slack_bot = WebClient(token=slack_bot_token)

# Your specific channel mappings
SLACK_CHANNELS = {
    "food-beverage": "C09TGV5J6VD",
    "housekeeping": "C09SJNERKMJ",
    "maintenance": "C09U20ALQBE"
}

@mcp.tool
def send_notification(title: str, message: str, channel: str = "housekeeping") -> str:
    """
    Send a notification to a specific team channel.
    
    Args:
        title: The title/summary of the alert.
        message: The detailed content.
        channel: The target team. Options: 'food-beverage', 'housekeeping', 'maintenance'.
    """
    channel_key = channel.lower()
    
    # Validate channel
    if channel_key not in SLACK_CHANNELS:
        valid_list = ", ".join(SLACK_CHANNELS.keys())
        return f"Error: Unknown channel '{channel}'. Valid options are: {valid_list}"

    channel_id = SLACK_CHANNELS[channel_key]

    try:
        response = slack_bot.chat_postMessage(
            channel=channel_id,
            text=f"*{title}*\n{message}"
        )
        return f"✅ Notification sent to {channel} channel (TS: {response['ts']})"
    except SlackApiError as e:
        logger.error(f"Slack Error: {e}")
        return f"❌ Failed to send to Slack: {e.response['error']}"

@mcp.tool
def get_weather(location: str) -> str:
    """Get the weather for a location."""
    # Kept your example tool for continuity
    return f"The weather in {location} is sunny (22°C)."
