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
    `Playing: ${s.current} | Speed: ${s.speed.toFixed(2)} | Paused: ${s.paused}`;

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

function next()   { call("/next").then(refresh); }
function prev()   { call("/previous").then(refresh); }
function toggle() { call("/toggle").then(refresh); }
function setSpeed(v) { call(`/speed/${v}`).then(refresh); }

loadAnimations();
refresh();
setInterval(refresh, 1000);
