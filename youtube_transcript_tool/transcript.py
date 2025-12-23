"""YouTube transcript download and formatting utilities.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import re
from typing import Any

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import (
    JSONFormatter,
    SRTFormatter,
    WebVTTFormatter,
)

from youtube_transcript_tool.logging_config import get_logger

logger = get_logger(__name__)

SUPPORTED_FORMATS = ["text", "json", "srt", "webvtt"]


def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from URL.

    Args:
        url: YouTube video URL

    Returns:
        Video ID string

    Raises:
        ValueError: If URL format is invalid
    """
    # Handle various YouTube URL formats
    patterns = [
        r"(?:youtube\.com\/watch\?v=)([^&\n]+)",
        r"(?:youtu\.be\/)([^&\n]+)",
        r"(?:youtube\.com\/embed\/)([^&\n]+)",
        r"(?:youtube\.com\/v\/)([^&\n]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            logger.debug("Extracted video ID: %s", video_id)
            return video_id

    raise ValueError(f"Could not extract video ID from URL: {url}")


def format_transcript_to_markdown(transcript: list[dict[str, Any]]) -> str:
    """Format transcript entries to markdown text.

    Args:
        transcript: List of transcript entries with 'text', 'start', 'duration' keys

    Returns:
        Formatted markdown string
    """
    logger.debug("Formatting %d transcript entries to markdown", len(transcript))

    # Combine all text entries with proper spacing
    text_parts = []
    for entry in transcript:
        text = entry["text"].strip()
        if text:
            text_parts.append(text)

    # Join with spaces and clean up
    markdown_text = " ".join(text_parts)

    # Clean up excessive whitespace
    markdown_text = re.sub(r"\s+", " ", markdown_text)

    logger.info("Formatted transcript: %d characters", len(markdown_text))
    return markdown_text


def format_transcript(fetched_transcript: Any, output_format: str = "text") -> str:
    """Format transcript with specified output format.

    Args:
        fetched_transcript: FetchedTranscript object from youtube_transcript_api
        output_format: Output format (text, json, srt, webvtt)

    Returns:
        Formatted transcript string

    Raises:
        ValueError: If format is not supported
    """
    if output_format not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format: {output_format}")

    logger.debug("Formatting transcript as %s", output_format)

    if output_format == "text":
        # Convert to list of dicts for text formatting
        transcript = [
            {"text": snippet.text, "start": snippet.start, "duration": snippet.duration}
            for snippet in fetched_transcript.snippets
        ]
        return format_transcript_to_markdown(transcript)
    elif output_format == "json":
        json_formatter = JSONFormatter()
        return json_formatter.format_transcript(fetched_transcript)
    elif output_format == "srt":
        srt_formatter = SRTFormatter()
        return srt_formatter.format_transcript(fetched_transcript)
    elif output_format == "webvtt":
        webvtt_formatter = WebVTTFormatter()
        return webvtt_formatter.format_transcript(fetched_transcript)

    # Default to text
    transcript = [
        {"text": snippet.text, "start": snippet.start, "duration": snippet.duration}
        for snippet in fetched_transcript.snippets
    ]
    return format_transcript_to_markdown(transcript)


def list_transcripts(url: str) -> list[dict[str, Any]]:
    """List all available transcripts for a video.

    Args:
        url: YouTube video URL

    Returns:
        List of transcript metadata dictionaries

    Raises:
        ValueError: If URL is invalid or transcripts unavailable
    """
    logger.info("Listing transcripts for: %s", url)
    video_id = extract_video_id(url)

    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        results = []
        for transcript in transcript_list:
            results.append(
                {
                    "language": transcript.language,
                    "language_code": transcript.language_code,
                    "is_generated": transcript.is_generated,
                    "is_translatable": transcript.is_translatable,
                }
            )

        logger.info("Found %d transcripts", len(results))
        return results
    except Exception as e:
        logger.error("Failed to list transcripts: %s", str(e))
        logger.debug("Full traceback:", exc_info=True)
        raise ValueError(f"Could not list transcripts: {e}") from e


def download_transcript(url: str, language: str | None = None, output_format: str = "text") -> str:
    """Download YouTube transcript with specified language and format.

    Args:
        url: YouTube video URL
        language: Preferred language code (e.g., 'en', 'de', 'es')
        output_format: Output format (text, json, srt, webvtt)

    Returns:
        Formatted transcript text

    Raises:
        ValueError: If URL is invalid or transcript unavailable
    """
    logger.info("Downloading transcript from: %s", url)

    video_id = extract_video_id(url)

    try:
        api = YouTubeTranscriptApi()

        # Fetch transcript with optional language preference
        if language:
            logger.debug("Requesting transcript in language: %s", language)
            fetched_transcript = api.fetch(video_id, languages=[language])
        else:
            fetched_transcript = api.fetch(video_id)

        logger.info("Retrieved %d transcript entries", len(fetched_transcript.snippets))
    except Exception as e:
        logger.error("Failed to download transcript: %s", str(e))
        logger.debug("Full traceback:", exc_info=True)
        raise ValueError(f"Could not retrieve transcript: {e}") from e

    return format_transcript(fetched_transcript, output_format)


def translate_transcript(url: str, target_language: str, output_format: str = "text") -> str:
    """Download and translate YouTube transcript to target language.

    Args:
        url: YouTube video URL
        target_language: Target language code (e.g., 'en', 'de', 'es')
        output_format: Output format (text, json, srt, webvtt)

    Returns:
        Translated and formatted transcript text

    Raises:
        ValueError: If URL is invalid, transcript unavailable, or translation fails
    """
    logger.info("Translating transcript from %s to: %s", url, target_language)

    video_id = extract_video_id(url)

    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        # Find a translatable transcript
        for transcript in transcript_list:
            if transcript.is_translatable:
                logger.debug(
                    "Found translatable transcript in %s, translating to %s",
                    transcript.language_code,
                    target_language,
                )
                translated = transcript.translate(target_language)
                fetched_transcript = translated.fetch()

                logger.info("Retrieved %d translated entries", len(fetched_transcript.snippets))
                return format_transcript(fetched_transcript, output_format)

        raise ValueError("No translatable transcript found for this video")

    except Exception as e:
        logger.error("Failed to translate transcript: %s", str(e))
        logger.debug("Full traceback:", exc_info=True)
        raise ValueError(f"Could not translate transcript: {e}") from e
