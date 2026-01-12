const providerModal = document.getElementById("providerModal");
const modelModal = document.getElementById("modelModal");

const openModalButton = document.getElementById("openModal");
const closeModalButton = document.getElementById("closeModal");
const cancelModalButton = document.getElementById("cancelModal");
const closeModelModalButton = document.getElementById("closeModelModal");

const apiKeyInput = document.getElementById("apiKey");
const baseUrlInput = document.getElementById("baseUrl");
const modelInput = document.getElementById("model");
const toggleKeyButton = document.getElementById("toggleKey");
const saveConfigButton = document.getElementById("saveConfig");
const downloadConfigButton = document.getElementById("downloadConfig");
const uploadConfigInput = document.getElementById("uploadConfig");
const testKeyButton = document.getElementById("testKey");

const STORAGE_KEY = "provider-config";

const defaultConfig = {
  base_url: "https://x666.me/v1",
  api_key: "",
  model: "gemini-3-flash-preview",
  timeout_s: 120,
};

function loadConfig() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return { ...defaultConfig };
  try {
    return { ...defaultConfig, ...JSON.parse(raw) };
  } catch (error) {
    console.warn("Failed to parse config", error);
    return { ...defaultConfig };
  }
}

function syncForm(config) {
  apiKeyInput.value = config.api_key || "";
  baseUrlInput.value = config.base_url || "";
  modelInput.value = config.model || "";
}

function readForm() {
  return {
    base_url: baseUrlInput.value.trim(),
    api_key: apiKeyInput.value.trim(),
    model: modelInput.value.trim(),
    timeout_s: 120,
  };
}

function saveConfig() {
  const config = readForm();
  localStorage.setItem(STORAGE_KEY, JSON.stringify(config));
  alert("已保存到浏览器（可导出为 provider.json）");
}

function downloadConfig() {
  const config = readForm();
  const blob = new Blob([JSON.stringify(config, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "provider.json";
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function uploadConfig(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const parsed = JSON.parse(reader.result);
      const config = { ...defaultConfig, ...parsed };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(config));
      syncForm(config);
      alert("已导入配置");
    } catch (error) {
      alert("配置文件解析失败");
    }
  };
  reader.readAsText(file);
}

testKeyButton.addEventListener("click", () => {
  testKeyButton.textContent = "检测中...";
  setTimeout(() => {
    testKeyButton.textContent = "检测";
    alert("已发送测试请求（示意）");
  }, 800);
});

saveConfigButton.addEventListener("click", saveConfig);
downloadConfigButton.addEventListener("click", downloadConfig);
uploadConfigInput.addEventListener("change", uploadConfig);

toggleKeyButton.addEventListener("click", () => {
  apiKeyInput.type = apiKeyInput.type === "password" ? "text" : "password";
});

openModalButton.addEventListener("click", () => {
  modelModal.classList.add("open");
  modelModal.setAttribute("aria-hidden", "false");
});

[closeModalButton, cancelModalButton].forEach((button) => {
  button.addEventListener("click", () => {
    providerModal.classList.remove("open");
    providerModal.setAttribute("aria-hidden", "true");
  });
});

closeModelModalButton.addEventListener("click", () => {
  modelModal.classList.remove("open");
  modelModal.setAttribute("aria-hidden", "true");
});

window.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    providerModal.classList.remove("open");
    modelModal.classList.remove("open");
    providerModal.setAttribute("aria-hidden", "true");
    modelModal.setAttribute("aria-hidden", "true");
  }
});

syncForm(loadConfig());
