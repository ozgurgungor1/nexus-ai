const baseUrl = window.location.origin;
let accessToken = null;
let currentConversationId = null;

const sections = {
  login: document.getElementById("section-login"),
  chat: document.getElementById("section-chat"),
  history: document.getElementById("section-history"),
};

const navButtons = {
  login: document.getElementById("btn-login"),
  chat: document.getElementById("btn-chat"),
  history: document.getElementById("btn-history"),
};

function showSection(name) {
  Object.keys(sections).forEach((section) => {
    sections[section].classList.toggle("visible", section === name);
    navButtons[section].classList.toggle("active", section === name);
  });
}

function setMessage(selector, text) {
  const el = document.getElementById(selector);
  el.textContent = text;
}

async function request(endpoint, method = "GET", body = null, headers = {}) {
  const defaultHeaders = { "Content-Type": "application/json" };
  const finalHeaders = { ...defaultHeaders, ...headers };
  if (accessToken) finalHeaders["Authorization"] = `Bearer ${accessToken}`;
  const response = await fetch(`${baseUrl}${endpoint}`, {
    method,
    headers: finalHeaders,
    body: body ? JSON.stringify(body) : null,
  });
  const text = await response.text();
  try {
    return JSON.parse(text);
  } catch {
    return { detail: text || response.statusText };
  }
}

async function uploadFile() {
  const fileInput = document.getElementById("file-input");
  const file = fileInput.files && fileInput.files[0];
  if (!file) {
    setMessage("upload-message", "Lütfen önce bir dosya seçin.");
    return;
  }
  if (!accessToken) {
    setMessage("upload-message", "Önce giriş yapmalısınız.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${baseUrl}/upload`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
    body: formData,
  });

  const result = await response.json();
  if (response.ok) {
    setMessage("upload-message", `Yüklendi: ${result.filename}`);
    showUploadPreview(result.path, file.type);
  } else {
    setMessage("upload-message", result.detail || "Yükleme başarısız oldu.");
  }
}

function showUploadPreview(path, mimeType) {
  const previewEl = document.getElementById("upload-preview");
  previewEl.innerHTML = "";
  const link = document.createElement("a");
  link.href = path;
  link.textContent = "Dosya bağlantısını aç";
  link.target = "_blank";
  previewEl.appendChild(link);

  if (mimeType.startsWith("image/")) {
    const img = document.createElement("img");
    img.src = path;
    img.alt = "Yüklenen görsel";
    img.style.maxWidth = "100%";
    img.style.marginTop = "12px";
    previewEl.appendChild(img);
  }

  if (mimeType.startsWith("audio/")) {
    const audio = document.createElement("audio");
    audio.controls = true;
    audio.src = path;
    audio.style.display = "block";
    audio.style.marginTop = "12px";
    previewEl.appendChild(audio);
  }

  if (mimeType.startsWith("video/")) {
    const video = document.createElement("video");
    video.controls = true;
    video.src = path;
    video.style.maxWidth = "100%";
    video.style.marginTop = "12px";
    previewEl.appendChild(video);
  }
}

async function register() {
  const name = document.getElementById("register-name").value.trim();
  const email = document.getElementById("register-email").value.trim();
  const password = document.getElementById("register-password").value.trim();
  const result = await request("/register", "POST", { email, password, full_name: name });
  setMessage("auth-message", result.detail || "Kayıt başarılı. Giriş yapabilirsiniz.");
}

async function login() {
  const email = document.getElementById("login-email").value.trim();
  const password = document.getElementById("login-password").value.trim();
  const result = await request("/login", "POST", { email, password });
  if (result.access_token) {
    accessToken = result.access_token;
    setMessage("auth-message", "Giriş başarılı.");
    showSection("chat");
  } else {
    setMessage("auth-message", result.detail || "Giriş başarısız.");
  }
}

async function sendMessage() {
  const input = document.getElementById("chat-input");
  const message = input.value.trim();
  if (!message) return;
  if (!accessToken) {
    setMessage("chat-message", "Önce giriş yapmalısınız.");
    return;
  }
  setMessage("chat-message", "Gönderiliyor...");
  const result = await request("/chat", "POST", { message, conversation_id: currentConversationId });
  if (result.response) {
    appendChat("Sen", message);
    appendChat("NEXUS AI", result.response);
    currentConversationId = result.conversation_id;
    input.value = "";
    setMessage("chat-message", "Yanıt alındı.");
  } else {
    setMessage("chat-message", result.detail || "Yanıt alınamadı.");
  }
}

function appendChat(sender, text) {
  const windowEl = document.getElementById("chat-window");
  const messageEl = document.createElement("div");
  messageEl.className = "history-item";
  messageEl.innerHTML = `<strong>${sender}</strong><p>${text}</p>`;
  windowEl.appendChild(messageEl);
  windowEl.scrollTop = windowEl.scrollHeight;
}

async function loadHistory() {
  if (!accessToken) {
    setMessage("history-message", "Önce giriş yapmalısınız.");
    return;
  }
  setMessage("history-message", "Yükleniyor...");
  const result = await request("/history", "GET");
  const historyList = document.getElementById("history-list");
  historyList.innerHTML = "";
  if (Array.isArray(result)) {
    result.forEach((item) => {
      const card = document.createElement("div");
      card.className = "history-item";
      card.innerHTML = `<strong>ID: ${item.conversation_id}</strong><p>${item.title}</p><p>${item.created_at}</p>`;
      historyList.appendChild(card);
    });
    setMessage("history-message", "Geçmiş yüklendi.");
  } else {
    setMessage("history-message", result.detail || "Geçmiş alınamadı.");
  }
}

function resetConversation() {
  currentConversationId = null;
  document.getElementById("conversation-id").textContent = "Konuşma: yeni";
  document.getElementById("chat-window").innerHTML = "";
  setMessage("chat-message", "Yeni konuşma başlatıldı.");
}

navButtons.login.addEventListener("click", () => showSection("login"));
navButtons.chat.addEventListener("click", () => showSection("chat"));
navButtons.history.addEventListener("click", async () => {
  showSection("history");
  await loadHistory();
});

document.getElementById("register-button").addEventListener("click", register);
document.getElementById("login-button").addEventListener("click", login);
document.getElementById("chat-send").addEventListener("click", sendMessage);
document.getElementById("upload-button").addEventListener("click", uploadFile);
document.getElementById("new-conversation").addEventListener("click", resetConversation);

showSection("login");
