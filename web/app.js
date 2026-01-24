const API = "/api";

async function call(path, method="POST", body=null) {
  const opts = { method };
  if (body) {
    opts.headers = { "Content-Type": "application/json" };
    opts.body = JSON.stringify(body);
  }
  const r = await fetch(API + path, opts);
  return r.json();
}

async function refresh() {
  const s = await call("/status", "GET");
  document.getElementById("status").innerText =
    `Playing: ${s.current} | Speed: ${s.speed.toFixed(2)} | Paused: ${s.paused} | Mode: ${s.mode} | Until: ${s.until ? new Date(s.until * 1000).toLocaleTimeString() : 'N/A'}`;

  document.getElementById("speed").value = s.speed;
  document.getElementById("speedLabel").innerText =
    `× ${s.speed.toFixed(2)}`;
}

async function loadAnimations() {
  const list = await call("/animations", "GET");
  const div = document.getElementById("animations");
  div.innerHTML = "";

  list.forEach(name => {
    const b = document.createElement("button");
    b.innerText = name;
    b.onclick = () => call(`/play/${name}`).then(refresh);
    div.appendChild(b);
  });
}

const shuffleBtn = document.getElementById("shuffleBtn");
const shuffleDuration = document.getElementById("shuffleDuration");

shuffleBtn.addEventListener("click", async () => {
  const duration = Number(shuffleDuration.value);

  await fetch("/api/shuffle", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ duration })
  });
});

document.getElementById("shutdownBtn").addEventListener("click", async () => {
  const confirmed = confirm(
    "This will safely shut down the Raspberry Pi.\n\nContinue?"
  );

  if (!confirmed) return;

  await fetch("/api/shutdown", { method: "POST" });

  alert("Shutting down… You can unplug power once the LEDs turn off.");
});

function next()   { call("/next").then(refresh); }
function prev()   { call("/previous").then(refresh); }
function toggle() { call("/toggle").then(refresh); }
function setSpeed(v) { call(`/speed/${v}`).then(refresh); }

loadAnimations();
refresh();
setInterval(refresh, 1000);
