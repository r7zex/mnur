const toast = document.getElementById("toast");
const modal = document.getElementById("modal");
const modalTitle = document.getElementById("modal-title");
const modalBody = document.getElementById("modal-body");
const modalCancel = document.getElementById("modal-cancel");
const modalConfirm = document.getElementById("modal-confirm");
const badge = document.getElementById("notification-badge");
const notificationList = document.getElementById("notification-list");
const mapImage = document.getElementById("map-image");
const alarmMapImage = document.getElementById("alarm-map");
const alarmMapViewport = document.querySelector(".map-zoom-viewport");
const crestLogo = document.getElementById("crest-logo");
const crestEmoji = document.getElementById("crest-emoji");
const statusText = document.getElementById("status-text");
const calendarAlertDot = document.getElementById("calendar-alert-dot");

const appConfig = window.APP_CONFIG || {};
const alarmEnabled = Boolean(appConfig.alarm);

const bagProgressValue = document.getElementById("bag-progress-value");
const bagProgressBar = document.getElementById("bag-progress-bar");

const envConfig = {
  MAP_IMAGE_PATH: "",
  MINISTRY_LOGO_PATH: "",
};

const state = {
  notifications: [
    {
      title: "Новый маршрут",
      message: "Опубликован безопасный маршрут к укрытию №24.",
      time: "сегодня, 09:15",
      icon: "🗺️",
      tone: "info",
    },
    {
      title: "Обновление погоды",
      message: "Ожидается сильный ветер после 18:00.",
      time: "сегодня, 07:45",
      icon: "🌬️",
      tone: "warning",
    },
  ],
};

function parseEnvValue(value) {
  const trimmed = value.trim();
  if (
    (trimmed.startsWith('"') && trimmed.endsWith('"')) ||
    (trimmed.startsWith("'") && trimmed.endsWith("'"))
  ) {
    return trimmed.slice(1, -1);
  }
  return trimmed;
}

function applyEnvConfig() {
  if (mapImage && envConfig.MAP_IMAGE_PATH) {
    mapImage.src = envConfig.MAP_IMAGE_PATH;
  }
  if (crestLogo && envConfig.MINISTRY_LOGO_PATH) {
    crestLogo.src = envConfig.MINISTRY_LOGO_PATH;
    crestLogo.hidden = false;
    crestEmoji?.classList.add("is-hidden");
  }
}

async function loadEnvConfig() {
  try {
    const response = await fetch(".env", { cache: "no-store" });
    if (!response.ok) {
      applyEnvConfig();
      return;
    }
    const text = await response.text();
    text.split(/\r?\n/).forEach((line) => {
      const cleaned = line.trim();
      if (!cleaned || cleaned.startsWith("#")) {
        return;
      }
      const separatorIndex = cleaned.indexOf("=");
      if (separatorIndex === -1) {
        return;
      }
      const key = cleaned.slice(0, separatorIndex).trim();
      const value = parseEnvValue(cleaned.slice(separatorIndex + 1));
      if (key in envConfig) {
        envConfig[key] = value;
      }
    });
  } catch (error) {
    console.warn("Не удалось загрузить .env файл.", error);
  }
  applyEnvConfig();
}

function applyAlarmMode() {
  if (!alarmEnabled) {
    return;
  }
  document.body.classList.add("alarm");
  if (mapImage) {
    mapImage.src = "assets/street_alarm.png";
  }
  if (statusText) {
    statusText.textContent = "ВНИМАНИЕ! ПРОИСШЕСТВИЕ В ВАШЕМ РАЙОНЕ!";
  }
  if (calendarAlertDot) {
    calendarAlertDot.classList.remove("safe");
    calendarAlertDot.classList.add("danger");
  }
}

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  window.clearTimeout(showToast.timeout);
  showToast.timeout = window.setTimeout(() => toast.classList.remove("show"), 2400);
}

function showModal({ title, message, onConfirm, confirmText = "Подтвердить" }) {
  modalTitle.textContent = title;
  modalBody.textContent = message;
  modalConfirm.textContent = confirmText;
  modal.classList.add("show");
  modal.setAttribute("aria-hidden", "false");
  modalConfirm.onclick = () => {
    onConfirm?.();
    hideModal();
  };
}

function hideModal() {
  modal.classList.remove("show");
  modal.setAttribute("aria-hidden", "true");
}

modalCancel.addEventListener("click", hideModal);
modal.addEventListener("click", (event) => {
  if (event.target === modal) {
    hideModal();
  }
});

function updateBadge() {
  const count = state.notifications.length;
  badge.textContent = count;
  badge.style.display = count > 0 ? "inline-flex" : "none";
}

function renderNotifications() {
  notificationList.innerHTML = "";
  if (state.notifications.length === 0) {
    const empty = document.createElement("p");
    empty.textContent = "Нет новых уведомлений.";
    notificationList.appendChild(empty);
    return;
  }

  state.notifications.forEach((item) => {
    const card = document.createElement("div");
    card.className = "notification-card";
    card.innerHTML = `
      <div class="notification-icon ${item.tone}">${item.icon}</div>
      <div class="notification-content">
        <h4>${item.title}</h4>
        <p>${item.message}</p>
        <span class="notification-time">${item.time}</span>
      </div>
    `;
    notificationList.appendChild(card);
  });
}

let mapZoomLevel = 1;
let mapOffset = { x: 0, y: 0 };
let isMapPanning = false;
let mapPanStart = { x: 0, y: 0 };
let mapPanOrigin = { x: 0, y: 0 };
const MAP_ZOOM_MIN = 1;
const MAP_ZOOM_MAX = 3;

function clampMapOffset() {
  if (!alarmMapImage || !alarmMapViewport) {
    return;
  }
  const viewportRect = alarmMapViewport.getBoundingClientRect();
  const maxOffsetX = Math.max(0, (viewportRect.width * mapZoomLevel - viewportRect.width) / 2);
  const maxOffsetY = Math.max(0, (viewportRect.height * mapZoomLevel - viewportRect.height) / 2);
  mapOffset.x = Math.min(maxOffsetX, Math.max(-maxOffsetX, mapOffset.x));
  mapOffset.y = Math.min(maxOffsetY, Math.max(-maxOffsetY, mapOffset.y));
}

function updateMapTransform() {
  if (!alarmMapImage) {
    return;
  }
  clampMapOffset();
  alarmMapImage.style.transform = `translate(${mapOffset.x}px, ${mapOffset.y}px) scale(${mapZoomLevel})`;
}

function setMapZoom(level) {
  if (!alarmMapImage) {
    return;
  }
  mapZoomLevel = Math.min(MAP_ZOOM_MAX, Math.max(MAP_ZOOM_MIN, level));
  updateMapTransform();
}

function resetMapZoom() {
  mapZoomLevel = 1;
  mapOffset = { x: 0, y: 0 };
  updateMapTransform();
}

function setupMapZoomControls() {
  if (!alarmMapImage) {
    return;
  }
  document.querySelectorAll("[data-map-zoom]").forEach((button) => {
    button.addEventListener("click", () => {
      const direction = button.dataset.mapZoom;
      const delta = direction === "in" ? 0.2 : -0.2;
      setMapZoom(mapZoomLevel + delta);
    });
  });
}

function setupMapPanZoom() {
  if (!alarmMapImage || !alarmMapViewport) {
    return;
  }

  alarmMapImage.setAttribute("draggable", "false");
  alarmMapImage.addEventListener("dragstart", (event) => event.preventDefault());

  alarmMapViewport.addEventListener(
    "wheel",
    (event) => {
      event.preventDefault();
      const delta = event.deltaY > 0 ? -0.15 : 0.15;
      setMapZoom(mapZoomLevel + delta);
    },
    { passive: false }
  );

  alarmMapViewport.addEventListener("pointerdown", (event) => {
    isMapPanning = true;
    mapPanStart = { x: event.clientX, y: event.clientY };
    mapPanOrigin = { ...mapOffset };
    alarmMapViewport.classList.add("is-panning");
    alarmMapViewport.setPointerCapture(event.pointerId);
  });

  alarmMapViewport.addEventListener("pointermove", (event) => {
    if (!isMapPanning) {
      return;
    }
    const deltaX = event.clientX - mapPanStart.x;
    const deltaY = event.clientY - mapPanStart.y;
    mapOffset = { x: mapPanOrigin.x + deltaX, y: mapPanOrigin.y + deltaY };
    updateMapTransform();
  });

  const stopPanning = (event) => {
    if (!isMapPanning) {
      return;
    }
    isMapPanning = false;
    alarmMapViewport.classList.remove("is-panning");
    if (event?.pointerId != null) {
      alarmMapViewport.releasePointerCapture(event.pointerId);
    }
  };

  alarmMapViewport.addEventListener("pointerup", stopPanning);
  alarmMapViewport.addEventListener("pointerleave", stopPanning);
  alarmMapViewport.addEventListener("pointercancel", stopPanning);
}

function updateBagProgress() {
  const items = document.querySelectorAll(".bag-check");
  if (!items.length) {
    return;
  }
  const checked = Array.from(items).filter((item) => item.checked).length;
  const percent = Math.round((checked / items.length) * 100);
  if (bagProgressValue) {
    bagProgressValue.textContent = `${percent}%`;
  }
  if (bagProgressBar) {
    bagProgressBar.style.width = `${percent}%`;
  }
}

function showScreen(name) {
  document.querySelectorAll(".app-content").forEach((screen) => {
    screen.classList.toggle("is-active", screen.dataset.screen === name);
    if (screen.dataset.screen === name) {
      screen.scrollTop = 0;
    }
  });
  document.querySelectorAll(".nav-item").forEach((item) => {
    item.classList.toggle("active", item.dataset.action === name);
  });
  if (name === "map") {
    resetMapZoom();
  }
}

function handleAction(action) {
  switch (action) {
    case "home":
      showScreen("home");
      break;
    case "instructions":
      showScreen("instructions");
      break;
    case "risks":
      showScreen("risks");
      break;
    case "notifications":
      showScreen("notifications");
      break;
    case "profile":
      showScreen("profile");
      break;
    case "back-home":
      showScreen("home");
      break;
    case "open-map":
      showScreen("map");
      break;
    case "submit-claim":
      showScreen("claim");
      break;
    case "calendar":
      showScreen("calendar");
      break;
    case "go-bag":
      showScreen("go-bag");
      break;
    case "shelters":
      showScreen("shelters");
      break;
    case "safety":
      showScreen("safety");
      break;
    case "support":
      showScreen("support");
      break;
    case "plan-complete":
      showScreen("plan-complete");
      break;
    case "call-112":
      showScreen("call-112");
      break;
    case "risk-plan":
      showScreen("risk-plan");
      break;
    case "edit-profile":
      showScreen("edit-profile");
      break;
    default:
      showToast("Действие выполнено.");
  }
}

function setupActions() {
  document.querySelectorAll("[data-action]").forEach((button) => {
    button.addEventListener("click", () => {
      const action = button.dataset.action;
      if (button.classList.contains("nav-item")) {
        document.querySelectorAll(".nav-item").forEach((item) => {
          item.classList.remove("active");
        });
        button.classList.add("active");
      }
      handleAction(action);
    });
  });

  document
    .getElementById("notifications-button")
    .addEventListener("click", () => handleAction("notifications"));

  document.querySelectorAll(".bag-check").forEach((item) => {
    item.addEventListener("change", updateBagProgress);
  });
}

renderNotifications();
updateBadge();
setupActions();
loadEnvConfig();
updateBagProgress();
applyAlarmMode();
setupMapZoomControls();
setupMapPanZoom();
