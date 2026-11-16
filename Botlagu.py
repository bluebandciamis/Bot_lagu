import asyncio, re, time, json, os
from datetime import datetime, timezone
from urllib.parse import quote_plus
from urllib.request import urlopen, Request
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager

os.system("")  # aktifin warna ANSI di terminal Windows

HIJAU, ABU, RESET, BOLD = "\033[38;5;213m", "\033[90m", "\033[0m", "\033[1m"


def bersih(t):
    t = re.sub(r"\(.*?\)|\[.*?\]", "", t)
    t = re.sub(r"(?i)\b(official|lyrics?|lyric video|video|audio|hd|mv)\b", "", t)
    return re.sub(r"\s+", " ", t).strip(" -|")


def api(url):
    req = Request(url, headers={"User-Agent": "BotLagu/1.0"})
    with urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))


def parse_lrc(teks):
    out = []
    for baris in teks.splitlines():
        m = re.match(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)", baris)
        if m:
            out.append((int(m.group(1)) * 60 + float(m.group(2)), m.group(3).strip()))
    return out


def cari_lirik(artis, judul, durasi=0):
    q = quote_plus(f"{artis} {judul}".strip())
    hasil = api(f"https://lrclib.net/api/search?q={q}")

    def selisih(h):
        return abs((h.get("duration") or 0) - durasi) if durasi else 0

    sinkron = sorted((h for h in hasil if h.get("syncedLyrics")), key=selisih)
    if sinkron:
        return parse_lrc(sinkron[0]["syncedLyrics"]), True
    biasa = sorted((h for h in hasil if h.get("plainLyrics")), key=selisih)
    if biasa:
        return [(0, b) for b in biasa[0]["plainLyrics"].splitlines()], False
    return [], False


def nama_sumber(app_id):
    a = (app_id or "").lower()
    if "spotify" in a:
        return "Spotify"
    if any(x in a for x in ("chrome", "msedge", "firefox", "brave", "opera")):
        return "Browser (YouTube)"
    return app_id or "?"


async def ambil_status():
    manager = await MediaManager.request_async()
    sesi = manager.get_current_session()
    if not sesi:
        return None
    info = await sesi.try_get_media_properties_async()
    tl = sesi.get_timeline_properties()
    main = sesi.get_playback_info().playback_status == 4
    sumber = nama_sumber(sesi.source_app_user_model_id)

    judul, artis = info.title or "", (info.artist or "").replace(" - Topic", "")
    if "Browser" in sumber and " - " in judul:  # judul YouTube: "Artis - Lagu"
        artis, judul = judul.split(" - ", 1)

    pos = tl.position.total_seconds()
    punya_posisi = tl.end_time.total_seconds() > 0
    if punya_posisi and main:
        try:
            pos += (datetime.now(timezone.utc) - tl.last_updated_time).total_seconds()
        except Exception:
            pass

    durasi = tl.end_time.total_seconds() - tl.start_time.total_seconds()
    m = re.search(r"(\d+)\s*min", info.title or "", re.I)
    if durasi <= 0 and m:  # kalau Windows nggak kasih durasi, tebak dari judul
        durasi = int(m.group(1)) * 60

    return dict(judul=bersih(judul), artis=bersih(artis), main=main,
                sumber=sumber, pos=pos, punya_posisi=punya_posisi, durasi=durasi)


def tampil(s, lirik, sinkron, pos):
    print("\033[H\033[J", end="")
    print(f"{BOLD}{s['artis']} - {s['judul']}{RESET}")
    print(f"{ABU}Sumber: {s['sumber']} | {'sinkron' if sinkron else 'lirik biasa'} | durasi terdeteksi: {int(s['durasi'])} detik{RESET}\n")
    if not lirik:
        print("Lirik nggak ketemu untuk lagu ini.")
        return
    if not sinkron:
        for _, b in lirik[:30]:
            print(b)
        return
    idx = max((i for i, (t, _) in enumerate(lirik) if t <= pos), default=0)
    for i in range(max(0, idx - 3), min(len(lirik), idx + 8)):
        b = lirik[i][1] or "♪"
        print(f"{HIJAU}{BOLD}> {b}{RESET}" if i == idx else f"{ABU}  {b}{RESET}")


lagu_lama, lirik, sinkron = None, [], False
timer, tick = 0.0, time.time()

while True:
    try:
        s = asyncio.run(ambil_status())
        if not s or not s["judul"]:
            print("\033[H\033[JMenunggu lagu diputar...")
            time.sleep(1)
            continue
        kunci = (s["artis"], s["judul"])
        sekarang = time.time()
        if kunci != lagu_lama:
            lagu_lama = kunci
            timer = 0.0
            print("\033[H\033[JMencari lirik...")
            try:
                lirik, sinkron = cari_lirik(*kunci, s["durasi"])
            except Exception as e:
                lirik, sinkron = [], False
                print("Gagal ambil lirik:", e)
        if s["main"]:
            timer += sekarang - tick
        tick = sekarang
        pos = s["pos"] if s["punya_posisi"] else timer 
        tampil(s, lirik, sinkron, pos)
    except Exception as e:
        print("Error:", e)
    time.sleep(0.4)
