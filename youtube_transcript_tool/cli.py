"""CLI entry point for youtube-transcript-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from youtube_transcript_tool.completion import completion_command
from youtube_transcript_tool.logging_config import get_logger, setup_logging
from youtube_transcript_tool.transcript import (
    SUPPORTED_FORMATS,
    download_transcript,
    list_transcripts,
    translate_transcript,
)

logger = get_logger(__name__)


@click.group()
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
@click.version_option(version="0.1.0")
@click.pass_context
def main(ctx: click.Context, verbose: int) -> None:
    """YouTube transcript downloader with multiple output formats.

    Download, list, and translate YouTube video transcripts in various formats
    including plain text, JSON, SRT, and WebVTT.

    \b
    Quick Start:
        # Download transcript
        youtube-transcript-tool download "https://www.youtube.com/watch?v=VIDEO_ID"

        # List available languages
        youtube-transcript-tool list "URL"

        # Translate to Spanish
        youtube-transcript-tool translate "URL" --to es

        # Show available formats
        youtube-transcript-tool formats

    \b
    Verbosity Levels:
        -v      Show high-level operations (INFO)
        -vv     Show detailed debugging (DEBUG)
        -vvv    Show HTTP requests and library internals (TRACE)
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    setup_logging(verbose)


@main.command("download", context_settings={"ignore_unknown_options": True})
@click.argument("url")
@click.option(
    "-f",
    "--format",
    "output_format",
    type=click.Choice(SUPPORTED_FORMATS, case_sensitive=False),
    default="text",
    help="Output format (default: text)",
)
@click.option(
    "-l",
    "--language",
    help="Preferred language code (e.g., en, de, es)",
)
@click.pass_context
def download_command(
    ctx: click.Context,
    url: str,
    output_format: str,
    language: str | None,
) -> None:
    """Download YouTube video transcript with optional format and language.

    \b
    Examples:
        # Download English transcript as plain text
        youtube-transcript-tool download "https://www.youtube.com/watch?v=VIDEO_ID"

        # Download German transcript
        youtube-transcript-tool download "URL" --language de

        # Download as JSON format
        youtube-transcript-tool download "URL" --format json

        # Download German transcript as SRT subtitles
        youtube-transcript-tool download "URL" -l de -f srt

        # With verbose logging
        youtube-transcript-tool -v download "URL"
    """
    verbose = ctx.obj.get("verbose", 0)
    setup_logging(verbose)

    logger.info("youtube-transcript-tool started")
    logger.debug("Running with verbose level: %d", verbose)

    try:
        transcript = download_transcript(url, language=language, output_format=output_format)
        click.echo(transcript)
        logger.info("youtube-transcript-tool completed")
    except ValueError as e:
        logger.error("Error: %s", str(e))
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@main.command("list")
@click.argument("url")
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
def list_command(url: str, verbose: int) -> None:
    """List all available transcripts (languages and types) for a YouTube video.

    Shows language codes, whether manually created or auto-generated, and
    whether the transcript is translatable to other languages.

    \b
    Examples:
        # List all available transcripts
        youtube-transcript-tool list "https://www.youtube.com/watch?v=VIDEO_ID"

        # With verbose logging
        youtube-transcript-tool -v list "URL"

    \b
    Output includes:
        - Language name and code (e.g., "English (en)")
        - Type: Manual or Auto-generated
        - Translatable: Yes or No
    """
    setup_logging(verbose)
    logger.info("Listing transcripts")

    try:
        transcripts = list_transcripts(url)

        if not transcripts:
            click.echo("No transcripts found for this video")
            return

        click.echo(f"Found {len(transcripts)} transcript(s):\n")

        for idx, transcript in enumerate(transcripts, 1):
            generated = "Auto-generated" if transcript["is_generated"] else "Manual"
            translatable = "Yes" if transcript["is_translatable"] else "No"

            click.echo(f"{idx}. {transcript['language']} ({transcript['language_code']})")
            click.echo(f"   Type: {generated}")
            click.echo(f"   Translatable: {translatable}")
            click.echo()

        logger.info("List completed")
    except ValueError as e:
        logger.error("Error: %s", str(e))
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@main.command("translate")
@click.argument("url")
@click.option(
    "--to",
    "target_language",
    required=True,
    help="Target language code (e.g., en, de, es)",
)
@click.option(
    "-f",
    "--format",
    "output_format",
    type=click.Choice(SUPPORTED_FORMATS, case_sensitive=False),
    default="text",
    help="Output format (default: text)",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
def translate_command(url: str, target_language: str, output_format: str, verbose: int) -> None:
    """Translate YouTube video transcript to target language using YouTube's translation.

    Finds a translatable transcript and uses YouTube's automatic translation
    to convert it to the target language.

    \b
    Examples:
        # Translate to Spanish
        youtube-transcript-tool translate "https://www.youtube.com/watch?v=VIDEO_ID" --to es

        # Translate to German as SRT subtitles
        youtube-transcript-tool translate "URL" --to de --format srt

        # Translate to French as JSON
        youtube-transcript-tool translate "URL" --to fr -f json

        # With verbose logging
        youtube-transcript-tool -v translate "URL" --to ja

    \b
    Common language codes:
        en (English), de (German), es (Spanish), fr (French),
        it (Italian), pt (Portuguese), ja (Japanese), zh (Chinese)
    """
    setup_logging(verbose)
    logger.info("Translating transcript")

    try:
        transcript = translate_transcript(url, target_language, output_format=output_format)
        click.echo(transcript)
        logger.info("Translation completed")
    except ValueError as e:
        logger.error("Error: %s", str(e))
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@main.command("formats")
def formats_command() -> None:
    """List all supported output formats with descriptions.

    \b
    Shows available formats:
        - text: Plain text (default, markdown-style)
        - json: JSON format with timestamps
        - srt: SubRip subtitle format (.srt)
        - webvtt: WebVTT subtitle format (.vtt)

    \b
    Example:
        youtube-transcript-tool formats
    """
    click.echo("Supported output formats:\n")

    formats_info = {
        "text": "Plain text (default, markdown-style)",
        "json": "JSON format with timestamps",
        "srt": "SubRip subtitle format (.srt)",
        "webvtt": "WebVTT subtitle format (.vtt)",
    }

    for fmt in SUPPORTED_FORMATS:
        click.echo(f"  {fmt:<10} - {formats_info.get(fmt, 'Unknown format')}")

    click.echo("\nUsage: youtube-transcript-tool <URL> --format <FORMAT>")


# Add completion subcommand
main.add_command(completion_command)


if __name__ == "__main__":
    main()
