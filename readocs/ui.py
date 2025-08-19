from rich.panel import Panel
from rich.text import Text
from rich import print

try:
  from pyfiglet import Figlet  
except Exception:  
  Figlet = None  

def _render_banner_text(text: str) -> str:
  if Figlet is None:
    return text
  try:
    # "Standard", "Slant", "Big"
    fig = Figlet(font="Standard")
    return fig.renderText(text)
  except Exception:
    return text


def print_banner(subtitle: str | None = None) -> None:
  banner = _render_banner_text("READOCS - CLI")
  title_text = Text.from_markup(f"[bold cyan]{banner}[/]")
  subtitle_text = Text(subtitle or "Gerador README e CHANGELOG baseados no seu código", style="dim")
  content = Text()
  content.append(title_text)
  if subtitle_text:
    content.append("\n")
    content.append(subtitle_text)
  print(Panel.fit(content, border_style="cyan", padding=(1, 2)))
