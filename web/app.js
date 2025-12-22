const toast = document.getElementById("toast");
const modal = document.getElementById("modal");
const modalTitle = document.getElementById("modal-title");
const modalBody = document.getElementById("modal-body");
const modalCancel = document.getElementById("modal-cancel");
const modalConfirm = document.getElementById("modal-confirm");
const badge = document.getElementById("notification-badge");

const state = {
  notifications: [
    {
      title: "Новое уведомление",
      message: "Опубликован безопасный маршрут к укрытию №24.",
    },
  ],
};

const notificationPanel = {
  title: "Уведомления",
  message: "Доступно 1 новое уведомление. Открыть список?",
};

const dayHighlights = new Set([14, 20, 21, 27, 28]);

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  window.clearTimeout(showToast.timeout);
  showToast.timeout = window.setTimeout(() => toast.classList.remove("show"), 2400);
}

function showModal({ title, message, onConfirm }) {
  modalTitle.textContent = title;
  modalBody.textContent = message;
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

function createCalendar() {
  const grid = document.getElementById("calendar-grid");
  for (let i = 0; i < 3; i += 1) {
    const empty = document.createElement("div");
    empty.className = "day";
    empty.textContent = "";
    grid.appendChild(empty);
  }

  for (let day = 1; day <= 30; day += 1) {
    const cell = document.createElement("div");
    cell.className = "day";
    cell.textContent = day;
    if (dayHighlights.has(day)) {
      cell.classList.add("highlight");
    }
    cell.addEventListener("click", () => {
      document.querySelectorAll(".day.active").forEach((active) => {
        active.classList.remove("active");
      });
      cell.classList.add("active");
      showToast(`Выбран день: ${day} апреля`);
    });
    grid.appendChild(cell);
  }
}

function handleAction(action) {
  switch (action) {
    case "emergency":
      showModal({
        title: "Экстренное сопровождение",
        message:
          "Вы отправляете запрос в диспетчерскую службу. Подтвердите отправку?",
        onConfirm: () => {
          state.notifications.push({
            title: "Запрос отправлен",
            message: "Оператор свяжется с вами в течение 2 минут.",
          });
          updateBadge();
          showToast("Запрос отправлен. Ожидайте звонка.");
        },
      });
      break;
    case "instructions":
      showToast("Открыт персональный список инструкций.");
      break;
    case "risks":
      showToast("Показан реестр текущих рисков по району.");
      break;
    case "weather":
      showToast("Загрузка прогноза погоды и предупреждений.");
      break;
    case "open-map":
      showModal({
        title: "Маршрут на карте",
        message:
          "Построить маршрут до ближайшего безопасного пункта?",
        onConfirm: () => showToast("Маршрут построен и сохранён в навигации."),
      });
      break;
    case "submit-claim":
      showModal({
        title: "Заявление о компенсации",
        message:
          "Новая заявка будет создана на основе вашего профиля. Продолжить?",
        onConfirm: () => showToast("Черновик заявления сохранён."),
      });
      break;
    case "calendar-settings":
      showToast("Фильтры календаря обновлены.");
      break;
    case "home":
      showToast("Вы находитесь на главном экране.");
      break;
    case "profile":
      showToast("Переход в профиль пользователя.");
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

  document.getElementById("notifications-button").addEventListener("click", () => {
    showModal({
      title: notificationPanel.title,
      message: notificationPanel.message,
      onConfirm: () => {
        const last = state.notifications[state.notifications.length - 1];
        showToast(last ? last.message : "Нет новых уведомлений.");
        state.notifications = [];
        updateBadge();
      },
    });
  });
}

createCalendar();
updateBadge();
setupActions();
