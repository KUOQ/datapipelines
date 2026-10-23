import json
import time
import requests
from datetime import datetime, timezone
from pathlib import Path

BASE_URL = "https://www.arbeitnow.com/api/job-board-api"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw" / "arbeitnow"
PAUSE_SECONDS = 3
MAX_PAGES = 50

def fetch_page(url: str, max_retries: int = 5) -> dict:
    """Appelle une page de l'API, en réessayant si la limite de débit est atteinte."""
    for attempt in range(1, max_retries + 1):
        response = requests.get(url, timeout=30)

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            wait = int(retry_after) if retry_after and retry_after.isdigit() else 30 * attempt
            print(f"  Limite atteinte (429), nouvelle tentative dans {wait} s...")
            time.sleep(wait)
            continue

        response.raise_for_status()
        return response.json()

    raise RuntimeError(f"Échec après {max_retries} tentatives : {url}")


def extract_all_jobs() -> list[dict]:
    """Parcourt toutes les pages en suivant les liens 'next'."""
    jobs = []
    url = BASE_URL
    page = 1

    while url and page <= MAX_PAGES:
        print(f"Page {page} : {url}")
        try:
            payload = fetch_page(url)
        except (requests.RequestException, RuntimeError) as error:
            print(f"Erreur sur la page {page} : {error}")
            print("Arrêt de l'extraction, sauvegarde des offres déjà récupérées.")
            break
        jobs.extend(payload["data"])
        url = payload["links"]["next"]
        page += 1
        time.sleep(PAUSE_SECONDS)

    if url:
        print(f"Attention : arrêt après {MAX_PAGES} pages, il restait des offres.")

    return jobs


def save_jobs(jobs: list[dict]) -> Path:
    """Sauvegarde les offres brutes dans un fichier JSON horodaté."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    extracted_at = datetime.now(timezone.utc)
    output_path = OUTPUT_DIR / f"jobs_{extracted_at:%Y%m%dT%H%M%SZ}.json"

    content = {"extracted_at": extracted_at.isoformat(), "jobs": jobs}
    output_path.write_text(
        json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return output_path


if __name__ == "__main__":
    jobs = extract_all_jobs()
    path = save_jobs(jobs)
    print(f"{len(jobs)} offres sauvegardées dans {path}")