const toast = document.getElementById("toast");
const modal = document.getElementById("modal");
const modalTitle = document.getElementById("modal-title");
const modalBody = document.getElementById("modal-body");
const modalCancel = document.getElementById("modal-cancel");
const modalConfirm = document.getElementById("modal-confirm");
const badge = document.getElementById("notification-badge");
const notificationList = document.getElementById("notification-list");
const mapImage = document.getElementById("map-image");
const crestLogo = document.getElementById("crest-logo");
const crestEmoji = document.getElementById("crest-emoji");

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
    },
    {
      title: "Обновление погоды",
      message: "Ожидается сильный ветер после 18:00.",
      time: "сегодня, 07:45",
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
      <h4>${item.title}</h4>
      <p>${item.message}</p>
      <span class="notification-time">${item.time}</span>
    `;
    notificationList.appendChild(card);
  });
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
      state.notifications = [];
      updateBadge();
      renderNotifications();
      break;
    case "profile":
      showScreen("profile");
      break;
    case "back-home":
      showScreen("home");
      break;
    case "open-map":
      showModal({
        title: "Маршрут на карте",
        message: "Построить маршрут до ближайшего безопасного пункта?",
        onConfirm: () => showToast("Маршрут построен и сохранён."),
      });
      break;
    case "submit-claim":
      showModal({
        title: "Заявление о компенсации",
        message: "Новая заявка будет создана на основе вашего профиля.",
        onConfirm: () => showToast("Черновик заявления сохранён."),
      });
      break;
    case "calendar":
      showModal({
        title: "Календарь происшествий",
        message: "В календаре отмечены дни с повышенной активностью.",
        onConfirm: () => showToast("Фильтры календаря обновлены."),
      });
      break;
    case "go-bag":
      showModal({
        title: "Тревожный рюкзак",
        message: "Список собран на 80%. Обновить недостающие позиции?",
        onConfirm: () => showToast("Список рюкзака обновлён."),
        confirmText: "Обновить",
      });
      break;
    case "shelters":
      showModal({
        title: "Укрытия",
        message: "Доступно 3 укрытия в радиусе 2 км. Показать на карте?",
        onConfirm: () => showToast("Укрытия отмечены на карте."),
        confirmText: "Показать",
      });
      break;
    case "safety":
      showModal({
        title: "Безопасность",
        message: "Рекомендуется проверить комплект аптечки и фонаря.",
        onConfirm: () => showToast("Напоминание добавлено."),
        confirmText: "Добавить",
      });
      break;
    case "support":
      showModal({
        title: "Чат поддержки",
        message: "Оператор ответит в течение 2 минут. Начать диалог?",
        onConfirm: () => showToast("Диалог с оператором открыт."),
        confirmText: "Начать",
      });
      break;
    case "plan-complete":
      showModal({
        title: "План выполнен",
        message: "Отметить выполнение плана в журнале действий?",
        onConfirm: () => showToast("План отмечен как выполненный."),
      });
      break;
    case "call-112":
      showModal({
        title: "Экстренный вызов",
        message: "Позвонить в службу 112 прямо сейчас?",
        onConfirm: () => showToast("Инициирован вызов 112."),
        confirmText: "Позвонить",
      });
      break;
    case "risk-plan":
      showModal({
        title: "План действий",
        message: "Открыть подробный план реагирования на текущие риски?",
        onConfirm: () => showToast("План действий открыт."),
      });
      break;
    case "edit-profile":
      showModal({
        title: "Профиль",
        message: "Открыть режим редактирования профиля?",
        onConfirm: () => showToast("Режим редактирования включён."),
      });
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
}

renderNotifications();
updateBadge();
setupActions();
loadEnvConfig();
